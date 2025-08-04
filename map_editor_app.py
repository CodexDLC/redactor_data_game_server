# File: map_editor_app.py
import tkinter as tk
from tkinter import ttk
import logging
from logging import LogRecord
from typing import Optional

from infrastructure.persistence.json_node_repository import JsonNodeRepository
from infrastructure.persistence.json_block_repository import JsonBlockRepository
from infrastructure.persistence.json_location_repository import JsonLocationRepository
from infrastructure.persistence.json_schema_repository import JsonSchemaRepository
from infrastructure.persistence.json_property_repository import JsonPropertyRepository
from infrastructure.persistence.json_tag_repository import JsonTagRepository  # <--- 1. НОВЫЙ ИМПОРТ
from infrastructure.ui.tkinter_views.editors.node.node_editor_view import NodeEditorView
from core.node_editor.node_editor_service import NodeEditorService
from infrastructure.ui.tkinter_views.left_panel.universal import UniversalLeftPanel
from infrastructure.ui.tkinter_views.editors.block.block_editor_view import BlockEditorView
from core.block_editor.block_editor_service import BlockEditorService
from infrastructure.ui.tkinter_views.widgets.floating_palette import FloatingPaletteWindow
from infrastructure.ui.tkinter_views.styles import *

MINIATURE_SIZE = 50
MINIATURE_PADDING = 5
DEFAULT_FONT = ("Helvetica", 10)
FRAME_WIDTH = 100


class TextWidgetHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.text_widget.config(state=tk.DISABLED)

    def emit(self, record: LogRecord):
        msg = self.format(record)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)


class MapEditorApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_PRIMARY)

        self.log_widget = None
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # --- Инициализация репозиториев ---
        self.node_repo = JsonNodeRepository()
        self.block_repo = JsonBlockRepository()
        self.location_repo = JsonLocationRepository()
        self.property_repo = JsonPropertyRepository()
        self.schema_repo = JsonSchemaRepository()
        self.tag_repo = JsonTagRepository()  # <--- 2. СОЗДАЕМ ЭКЗЕМПЛЯР РЕПОЗИТОРИЯ ТЕГОВ

        self.nodes_panel_view = None
        self.active_brush_node: Optional[dict] = None

        # --- Создание UI ---
        self.toolbar = tk.Frame(self, bg=BG_SECONDARY)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.create_toolbar()

        main_content_frame = tk.Frame(self, bg=BG_PRIMARY)
        main_content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.left_panel = UniversalLeftPanel(
            master=main_content_frame, app=self, node_repo=self.node_repo, block_repo=self.block_repo,
            location_repo=self.location_repo, miniature_size=MINIATURE_SIZE,
            miniature_padding=MINIATURE_PADDING, font=DEFAULT_FONT, frame_width=FRAME_WIDTH
        )
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        right_area_frame = tk.Frame(main_content_frame, bg=BG_PRIMARY)
        right_area_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.menu_frame = tk.Frame(right_area_frame, bg=BG_CANVAS)
        self.menu_frame.pack(fill=tk.X, side=tk.TOP)

        self.editor_container = tk.Frame(right_area_frame, bg=BG_PRIMARY)
        self.editor_container.pack(fill=tk.BOTH, expand=True)

        self.status_bar = tk.Label(self, text="Готов к работе...", bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                   bg=BG_CANVAS, fg=FG_TEXT)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.create_modes_menu()
        self.show_mode_selection_screen()

    def create_toolbar(self):
        tk.Button(self.toolbar, text="Открыть консоль логов", command=self.show_log_console, bg=BG_PRIMARY,
                  fg=FG_TEXT).pack(side=tk.LEFT, padx=5, pady=2)

    def show_log_console(self):
        if self.log_widget and self.log_widget.master.winfo_exists():
            self.log_widget.master.lift()
            return

        log_window = tk.Toplevel(self)
        log_window.title("Консоль логов")
        log_window.geometry("600x400")

        self.log_widget = tk.Text(log_window, bg=CODE_BG, fg=CODE_FG, font=CODE_FONT)
        self.log_widget.pack(fill=tk.BOTH, expand=True)

        handler = TextWidgetHandler(self.log_widget)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def set_status_message(self, message: str, is_error: bool = False):
        self.status_bar.config(text=message, fg=ERROR_COLOR if is_error else FG_TEXT)

    def create_modes_menu(self):
        tk.Button(self.menu_frame, text="Редактор Нод", command=self.show_node_editor).pack(side=tk.LEFT, padx=5,
                                                                                            pady=2)
        tk.Button(self.menu_frame, text="Редактор Блоков", command=self.show_block_editor).pack(side=tk.LEFT, padx=5,
                                                                                                pady=2)
        tk.Button(self.menu_frame, text="Редактор Локаций", command=self.show_location_editor).pack(side=tk.LEFT,
                                                                                                    padx=5, pady=2)

    def clear_editor_container(self):
        for widget in self.editor_container.winfo_children():
            widget.destroy()

    def show_mode_selection_screen(self):
        self.clear_editor_container()
        tk.Label(self.editor_container, text="Выберите режим в меню сверху", font=("Helvetica", 16), fg=FG_TEXT,
                 bg=BG_PRIMARY).pack(expand=True)

    def show_node_editor(self):
        self.clear_editor_container()
        node_schema = self.schema_repo.get_node_schema()
        # --- 3. ИЗМЕНЕНИЯ ЗДЕСЬ ---
        # Получаем список тегов для передачи в UI
        node_tags = self.tag_repo.get_tags_by_category('node_tags')

        # Передаем список тегов в NodeEditorView
        view = NodeEditorView(self.editor_container, self, schema=node_schema, available_tags=node_tags)

        # Передаем репозиторий тегов в NodeEditorService
        service = NodeEditorService(
            view=view,
            nodes_panel=self.left_panel.nodes_panel,
            repository=self.node_repo,
            tag_repository=self.tag_repo,  # <--- Передаем tag_repo
            app=self
        )
        view.pack(fill=tk.BOTH, expand=True)
        self.set_status_message("Режим: Редактор нодов")

    def show_block_editor(self):
        self.clear_editor_container()
        node_schema = self.schema_repo.get_node_schema()

        # --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
        # BlockEditorView ТРЕБУЕТ node_schema в конструкторе. Мы должны его передать.
        view = BlockEditorView(self.editor_container, self, node_schema)

        # Убеждаемся, что и сервис получает все, что ему нужно
        service = BlockEditorService(
            view=view,
            repository=self.block_repo,
            node_repo=self.node_repo,
            property_repo=self.property_repo,
            node_schema=node_schema,
            app=self
        )

        view.pack(fill=tk.BOTH, expand=True)
        self.left_panel.show_panel("blocks")
        self.set_status_message("Режим: Редактор блоков")

    def show_location_editor(self):
        self.clear_editor_container()
        tk.Label(self.editor_container, text="Редактор Локаций (в разработке)", font=("Helvetica", 16), fg=FG_TEXT,
                 bg=BG_PRIMARY).pack(expand=True)
        self.set_status_message("Режим: Редактор локаций")

    def set_active_brush_node(self, node_data: dict) -> None:
        self.active_brush_node = node_data
        node_name = node_data.get('display_name', node_data.get('node_key', 'N/A'))
        self.set_status_message(f"Активный нод-кисточка установлен: {node_name}")
        self.set_cursor_to_brush()
        logging.info(f"Активный нод-кисточка установлен: {node_name}")
        if self.left_panel.nodes_panel and self.left_panel.nodes_panel.winfo_exists():
            node_color = node_data.get('color', BG_PRIMARY)
            self.left_panel.nodes_panel.update_brush_indicator(node_color)

    def unselect_active_brush_node(self):
        self.active_brush_node = None
        self.set_cursor_to_default()
        self.set_status_message("Активная кисточка сброшена.")
        logging.info("Активная кисточка сброшена.")
        if self.left_panel.nodes_panel and self.left_panel.nodes_panel.winfo_exists():
            self.left_panel.nodes_panel.update_brush_indicator(None)

    def set_cursor_to_brush(self):
        self.master.config(cursor="dot")

    def set_cursor_to_default(self):
        self.master.config(cursor="arrow")

    def get_active_brush_node(self) -> Optional[dict]:
        return self.active_brush_node

    def open_palette(self, palette_type: str, x: int, y: int):
        if palette_type == "nodes":
            items_data = self.node_repo.get_all()
            FloatingPaletteWindow(self, title="Палитра Нодов", app=self, items_data=items_data, x=x, y=y,
                                  palette_type="nodes")
        elif palette_type == "blocks":
            # ...
            pass
        elif palette_type == "locations":
            # ...
            pass

    def get_selected_node_key(self) -> Optional[str]:
        return None