# File: map_editor_app.py
import tkinter as tk
from tkinter import ttk
import logging
from typing import Optional, Any

from infrastructure.persistence.initializer import RepositoryInitializer
from core.editor_initializer import EditorInitializer
from core.tag_filter_service import TagFilterService

from infrastructure.ui.tkinter_views.editors.block.block_editor_body import BlockEditorBody
from infrastructure.ui.tkinter_views.editors.location.location_editor_body import \
    LocationEditorBody  # ИЗМЕНЕНИЕ: Используем новый класс
from infrastructure.ui.tkinter_views.editors.prebuffer.prebuffer_editor_body import PrebufferEditorBody

from infrastructure.ui.tkinter_views.widgets.floating_palette import FloatingPaletteWindow
from infrastructure.ui.tkinter_views.widgets.log_console_window import LogConsoleWindow
from infrastructure.ui.tkinter_views.styles import *


class MapEditorApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_PRIMARY)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.repos = RepositoryInitializer()
        self.tag_filter_service = TagFilterService(self.repos.tag)
        self.editors = EditorInitializer(self)

        self.active_node_brush: Optional[dict] = None
        self.active_block_brush: Optional[dict] = None
        self.log_console_window: Optional[LogConsoleWindow] = None
        self.current_editor_body: Optional[
            BlockEditorBody | LocationEditorBody | PrebufferEditorBody] = None  # ИЗМЕНЕНИЕ: Обновили тип

        self.header: tk.Frame | None = None
        self.body_container: tk.Frame | None = None
        self.footer: tk.Label | None = None

        self.header_buttons: dict[str, tk.Button] = {}

        self._setup_layout()
        self._create_header_buttons()
        self.show_welcome_screen()

    def _setup_layout(self):
        self.header = tk.Frame(self, bg=BG_SECONDARY)
        self.header.pack(side=tk.TOP, fill=tk.X)

        self.body_container = tk.Frame(self, bg=BG_PRIMARY)
        self.body_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.footer = tk.Label(self, text="Готов к работе...", bd=1, relief=tk.SUNKEN, anchor=tk.W,
                               bg=BG_CANVAS, fg=FG_TEXT)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)

    def _create_header_buttons(self):
        tk.Button(self.header, text="Редактор Блоков", command=self.show_block_editor, bg=BG_PRIMARY,
                  fg=FG_TEXT).pack(side=tk.LEFT, padx=5, pady=2)

        tk.Button(self.header, text="Редактор Пре-буферов", command=self.show_prebuffer_editor, bg=BG_PRIMARY,
                  fg=FG_TEXT).pack(side=tk.LEFT, padx=5, pady=2)

        tk.Button(self.header, text="Редактор Локаций", command=self.show_location_editor, bg=BG_PRIMARY,
                  fg=FG_TEXT).pack(side=tk.LEFT, padx=5, pady=2)

        ttk.Separator(self.header, orient='vertical').pack(side=tk.LEFT, fill='y', padx=10, pady=2)

        tk.Button(self.header, text="Открыть консоль логов", command=self.show_log_console, bg=BG_PRIMARY,
                  fg=FG_TEXT).pack(side=tk.LEFT, padx=5, pady=2)

    def _highlight_active_button(self, editor_type: str):
        for button in self.header_buttons.values():
            button.config(bg=BG_PRIMARY)
        if editor_type in self.header_buttons:
            self.header_buttons[editor_type].config(bg=BG_HIGHLIGHT)

    def show_log_console(self):
        if self.log_console_window and self.log_console_window.winfo_exists():
            self.log_console_window.lift()
        else:
            self.log_console_window = LogConsoleWindow(self)

    def set_status_message(self, message: str, is_error: bool = False):
        self.footer.config(text=message, fg=ERROR_COLOR if is_error else FG_TEXT)

    def _clear_body_container(self):
        for widget in self.body_container.winfo_children():
            widget.destroy()
        self.current_editor_body = None
        self._highlight_active_button("")

    def show_welcome_screen(self):
        self._clear_body_container()
        tk.Label(self.body_container, text="Выберите режим в меню сверху", font=("Helvetica", 16), fg=FG_TEXT,
                 bg=BG_PRIMARY).pack(expand=True)

    def show_block_editor(self):
        self._clear_body_container()
        self.current_editor_body = self.editors.create_block_editor()
        self.current_editor_body.pack(fill=tk.BOTH, expand=True)
        self.set_status_message("Режим: Редактор Блоков")
        self._highlight_active_button("block")

    def show_location_editor(self):
        self._clear_body_container()
        # ИЗМЕНЕНИЕ: Заменяем заглушку на вызов нового редактора
        self.current_editor_body = self.editors.create_location_editor()
        self.current_editor_body.pack(fill=tk.BOTH, expand=True)
        self.set_status_message("Режим: Редактор Локаций")
        self._highlight_active_button("location")

    def show_prebuffer_editor(self):
        self._clear_body_container()
        self.current_editor_body = self.editors.create_prebuffer_editor()
        self.current_editor_body.pack(fill=tk.BOTH, expand=True)
        self.set_status_message("Режим: Редактор Пре-буферов")
        self._highlight_active_button("prebuffer")

    def set_active_brush(self, brush_data: dict, brush_type: str):
        if brush_type == "node":
            self.active_node_brush = brush_data
            self.active_block_brush = None
            name = brush_data.get('display_name', brush_data.get('node_key', 'N/A'))
            self.set_status_message(f"Кисточка (нод): {name}")
        elif brush_type == "block":
            self.active_block_brush = brush_data
            self.active_node_brush = None
            name = brush_data.get('display_name', brush_data.get('block_key', 'N/A'))
            self.set_status_message(f"Кисточка (блок): {name}")
        self.master.master.config(cursor="dot")

    def get_active_brush(self) -> Optional[tuple[str, dict]]:
        if self.active_block_brush:
            return "block", self.active_block_brush
        if self.active_node_brush:
            return "node", self.active_node_brush
        return None

    def unselect_active_brush(self):
        self.active_node_brush = None
        self.active_block_brush = None
        self.set_status_message("Активная кисточка сброшена.")
        self.master.master.config(cursor="")

    def open_palette(self, palette_type: str, x: int, y: int):
        if palette_type == "nodes":
            items_data = self.repos.node.get_all()
            FloatingPaletteWindow(self, title="Палитра Нодов", app=self, items_data=items_data, x=x, y=y)
        elif palette_type == "blocks":
            items_data = self.repos.block.get_all()
            node_data_source = self.repos.node.get_all()
            FloatingPaletteWindow(self, title="Палитра Блоков", app=self, items_data=items_data, x=x, y=y,
                                  palette_type="blocks", node_data_source=node_data_source)