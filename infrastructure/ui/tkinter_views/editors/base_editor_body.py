# File: infrastructure/ui/tkinter_views/editors/base_editor_body.py
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable

from ..styles import *
from ..widgets.universal_context_menu import create_universal_context_menu
from ..widgets.code_preview_window import CodePreviewWindow


class BaseEditorBody(tk.Frame):
    def __init__(self, master, app: Any):
        super().__init__(master, bg=BG_PRIMARY)
        self.app = app
        self.service: Any | None = None
        self.properties_panel = tk.Frame(self, bg=BG_PRIMARY, width=300)
        self.actions_panel = tk.Frame(self, bg=BG_PRIMARY, width=300)

        self.canvas = tk.Canvas(self, bg=BG_CANVAS, highlightthickness=0)
        self.context_menu: tk.Menu | None = None
        self._code_preview_window: CodePreviewWindow | None = None

        self.properties_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.actions_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _create_context_menu_for_canvas(self):
        """Создает и привязывает универсальное контекстное меню к холсту."""
        if not self.canvas: return

        commands = {
            "unselect_brush": self.app.unselect_active_brush,
            "cut": lambda: self.canvas.event_generate("<<Cut>>"),
            "copy": lambda: self.canvas.event_generate("<<Copy>>"),
            "paste": lambda: self.canvas.event_generate("<<Paste>>"),
            "delete": lambda: self.canvas.event_generate("<<Clear>>"),
            "open_node_palette": lambda: self._open_palette_from_menu("nodes"),
            "open_block_palette": lambda: self._open_palette_from_menu("blocks"),
            "open_location_palette": lambda: self._open_palette_from_menu("locations"),
            "tool_1": lambda: print("Tool 1 clicked"),
            "tool_2": lambda: print("Tool 2 clicked")
        }
        self.context_menu = create_universal_context_menu(self.canvas, commands)
        self.canvas.bind("<Button-3>", self._on_right_click)

    def _on_right_click(self, event):
        """Обработчик правого клика для контекстного меню."""
        if not self.context_menu: return
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def _open_palette_from_menu(self, palette_type: str):
        """Вспомогательный метод для открытия палитры с координатами курсора."""
        x = self.master.winfo_pointerx()
        y = self.master.winfo_pointery()
        self.app.open_palette(palette_type, x, y)

    def _show_code_preview_window(self, data: dict, title: str):
        """Открывает или обновляет единое окно предпросмотр кода."""
        if self._code_preview_window and self._code_preview_window.winfo_exists():
            self._code_preview_window.update_content(data)
            self._code_preview_window.lift()
        else:
            self._code_preview_window = CodePreviewWindow(self.master, data, title)

    def bind_save_command(self, command: Callable[[], None]) -> None:
        pass

    def bind_delete_command(self, command: Callable[[], None]) -> None:
        pass

    def bind_new_command(self, command: Callable[[], None]) -> None:
        pass

    def bind_show_code_command(self, command: Callable[[Any, str], None], title: str) -> None:
        pass

    def bind_canvas_click(self, command: Callable[[Any], None]):
        pass

    def get_form_data(self) -> dict:
        raise NotImplementedError

    def draw_canvas(self):
        self.canvas.delete("all")

    def set_service(self, service):
        self.service = service