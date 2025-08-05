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
from infrastructure.persistence.json_tag_repository import JsonTagRepository  # <--- ИСПРАВЛЕНИЕ ЗДЕСЬ

from infrastructure.ui.tkinter_views.left_panel.universal import UniversalLeftPanel
from infrastructure.ui.tkinter_views.editors.block.block_editor_view import BlockEditorView
from core.block_editor.block_editor_service import BlockEditorService
from infrastructure.ui.tkinter_views.widgets.floating_palette import FloatingPaletteWindow
from infrastructure.ui.tkinter_views.widgets.log_console_window import LogConsoleWindow
from infrastructure.ui.tkinter_views.styles import *

# Определяем константы на уровне модуля
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
    """
    Класс редактора карты

    """
    def __init__(self, master):
        super().__init__(master, bg=BG_PRIMARY)

        # --- 1. Инициализация состояния и репозиториев ---
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.node_repo = JsonNodeRepository()
        self.block_repo = JsonBlockRepository()
        self.location_repo = JsonLocationRepository()
        self.schema_repo = JsonSchemaRepository()
        self.tag_repo = JsonTagRepository()
        self.property_repo = JsonPropertyRepository()

        self.active_brush_node: Optional[dict] = None
        self.log_console_window: Optional[LogConsoleWindow] = None

        # --- 2. Построение основного UI ---
        self.toolbar = tk.Frame(self, bg=BG_SECONDARY)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        main_content_frame = tk.Frame(self, bg=BG_PRIMARY)
        main_content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.left_panel = UniversalLeftPanel(
            master=main_content_frame, app=self, node_repo=self.node_repo,
            block_repo=self.block_repo, location_repo=self.location_repo,
            miniature_size=MINIATURE_SIZE, miniature_padding=MINIATURE_PADDING,
            font=DEFAULT_FONT, frame_width=FRAME_WIDTH
        )
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        right_area_frame = tk.Frame(main_content_frame, bg=BG_PRIMARY)
        right_area_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- ПАНЕЛЬ-ПОДСКАЗКА ОТСЮДА УДАЛЕНА ---

        self.editor_container = tk.Frame(right_area_frame, bg=BG_PRIMARY)
        self.editor_container.pack(fill=tk.BOTH, expand=True)

        self.status_bar = tk.Label(self, text="Готов к работе...", bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                   bg=BG_CANVAS, fg=FG_TEXT)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # --- 3. Финальная настройка ---
        self._create_toolbar()
        self.show_mode_selection_screen()

    def _create_toolbar(self):
        tk.Button(self.toolbar, text="Редактор Блоков", command=self.show_block_editor, bg=BG_PRIMARY,
                  fg=FG_TEXT).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(self.toolbar, text="Редактор Объектов", command=self.show_object_editor, bg=BG_PRIMARY,
                  fg=FG_TEXT).pack(side=tk.LEFT, padx=5, pady=2)
        ttk.Separator(self.toolbar, orient='vertical').pack(side=tk.LEFT, fill='y', padx=10, pady=2)
        tk.Button(self.toolbar, text="Открыть консоль логов", command=self.show_log_console, bg=BG_PRIMARY,
                  fg=FG_TEXT).pack(side=tk.LEFT, padx=5, pady=2)

    def show_log_console(self):
        if self.log_console_window and self.log_console_window.winfo_exists():
            self.log_console_window.lift()
        else:
            self.log_console_window = LogConsoleWindow(self)

    def set_status_message(self, message: str, is_error: bool = False):
        self.status_bar.config(text=message, fg=ERROR_COLOR if is_error else FG_TEXT)

    def clear_editor_container(self):
        for widget in self.editor_container.winfo_children():
            widget.destroy()

    def show_mode_selection_screen(self):
        self.clear_editor_container()
        tk.Label(self.editor_container, text="Выберите режим в меню сверху", font=("Helvetica", 16), fg=FG_TEXT,
                 bg=BG_PRIMARY).pack(expand=True)

    def show_block_editor(self):
        self.clear_editor_container()
        node_schema = self.schema_repo.get_node_schema()
        view = BlockEditorView(self.editor_container, self, node_schema)
        service = BlockEditorService(view=view, repository=self.block_repo, node_repo=self.node_repo, app=self)
        view.pack(fill=tk.BOTH, expand=True)
        self.left_panel.show_panel("blocks")
        self.set_status_message("Режим: Редактор Блоков (Тайлов)")

    def show_object_editor(self):
        self.clear_editor_container()
        tk.Label(self.editor_container, text="Редактор Объектов (в разработке)", font=("Helvetica", 16), fg=FG_TEXT,
                 bg=BG_PRIMARY).pack(expand=True)
        self.set_status_message("Режим: Редактор Объектов")

    def set_active_brush_node(self, node_data: dict) -> None:
        self.active_brush_node = node_data
        node_name = node_data.get('display_name', node_data.get('node_key', 'N/A'))
        self.set_status_message(f"Активный нод-кисточка установлен: {node_name}")
        self.master.config(cursor="dot")
        if hasattr(self.left_panel, 'nodes_panel') and self.left_panel.nodes_panel:
            self.left_panel.nodes_panel.update_brush_indicator(node_data.get('color', BG_PRIMARY))

    def unselect_active_brush_node(self):
        self.active_brush_node = None
        self.set_status_message("Активная кисточка сброшена.")
        self.master.config(cursor="")
        if hasattr(self.left_panel, 'nodes_panel') and self.left_panel.nodes_panel:
            self.left_panel.nodes_panel.update_brush_indicator(None)

    def get_active_brush_node(self) -> Optional[dict]:
        return self.active_brush_node

    def open_palette(self, palette_type: str, x: int, y: int):
        if palette_type == "nodes":
            items_data = self.node_repo.get_all()
            FloatingPaletteWindow(self, title="Палитра Кирпичиков", app=self, items_data=items_data, x=x, y=y)
        # TODO: Добавить логику для других палитр