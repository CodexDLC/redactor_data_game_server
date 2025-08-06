# File: infrastructure/ui/tkinter_views/base_editor_view.py
import tkinter as tk
from typing import Any, Callable
from .widgets.code_preview_window import CodePreviewWindow
from .widgets.universal_context_menu import create_universal_context_menu
from .styles import *


class BaseEditorView(tk.Frame):
    """
    Базовый класс для всех редакторов.
    Содержит общую трехпанельную компоновку,
    управление окном предпросмотр кода и контекстным меню.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, bg=BG_PRIMARY)
        self.master = master
        self.app = app
        self._code_preview_window = None
        self.main_paned_window = None
        self.center_frame = None
        self.right_frame = None
        self.controls = None
        self.context_menu = None
        self.service = None # Добавляем атрибут для сервиса

    def three_panel_layout(self):
        """Создает общую трехпанельную компоновку."""
        self.main_paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, bg=BG_PRIMARY)
        self.main_paned_window.pack(fill=tk.BOTH, expand=True)

        self.center_frame = tk.Frame(self.main_paned_window, bg=BG_PRIMARY)
        self.main_paned_window.add(self.center_frame, stretch="always")

        self.right_frame = tk.Frame(self.main_paned_window, bg=BG_PRIMARY)
        self.main_paned_window.add(self.right_frame, minsize=300)

    def _on_right_click(self, event):
        """Обработчик правого клика для контекстного меню."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def _open_palette_from_menu(self, palette_type: str):
        """Вспомогательный метод для открытия палитры с координатами курсора."""
        x = self.master.winfo_pointerx()
        y = self.master.winfo_pointery()
        self.app.open_palette(palette_type, x, y)

    def _create_context_menu_for_canvas(self, canvas: tk.Canvas):
        """Создает и привязывает универсальное контекстное меню к canvas."""
        commands = {
            # --- ИСПРАВЛЕНО: Используем правильное имя метода ---
            "unselect_brush": self.app.unselect_active_brush,
            "cut": lambda: canvas.event_generate("<<Cut>>"),
            "copy": lambda: canvas.event_generate("<<Copy>>"),
            "paste": lambda: canvas.event_generate("<<Paste>>"),
            "delete": lambda: canvas.event_generate("<<Clear>>"),
            "open_node_palette": lambda: self._open_palette_from_menu("nodes"),
            "open_block_palette": lambda: self._open_palette_from_menu("blocks"),
            "open_location_palette": lambda: self._open_palette_from_menu("locations"),
            "tool_1": lambda: print("Tool 1 clicked"),
            "tool_2": lambda: print("Tool 2 clicked")
        }
        self.context_menu = create_universal_context_menu(canvas, commands)
        canvas.bind("<Button-3>", self._on_right_click)

    def _show_code_preview_window(self, data: dict, title: str):
        """
        Открывает или обновляет единое окно предпросмотр кода.
        """
        if self._code_preview_window and self._code_preview_window.winfo_exists():
            self._code_preview_window.update_content(data)
            self._code_preview_window.lift()
        else:
            self._code_preview_window = CodePreviewWindow(self.master, data, title)

    def bind_save_command(self, command: Callable[[], None]) -> None:
        """Привязывает команду к кнопке 'Сохранить' в панели управления."""
        if self.controls and self.controls.save_button:
            self.controls.save_button.config(command=command)

    def bind_delete_command(self, command: Callable[[], None]) -> None:
        if self.controls and self.controls.delete_button:
            self.controls.delete_button.config(command=command)
        if self.context_menu:
            self.context_menu.entryconfig("Удалить", command=command)

    def bind_new_command(self, command: Callable[[], None]) -> None:
        if self.controls and self.controls.new_button:
            self.controls.new_button.config(command=command)

    def bind_show_code_command(self, command: Callable[[Any, str], None], title: str) -> None:
        if self.controls and self.controls.show_code_button:
            self.controls.show_code_button.config(command=lambda: command(self.get_form_data(), title))

    def get_form_data(self) -> dict:
        raise NotImplementedError("Дочерний класс должен реализовать этот метод.")
