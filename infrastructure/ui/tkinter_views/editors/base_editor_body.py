# File: infrastructure/ui/tkinter_views/editors/base_editor_body.py
import tkinter as tk
from typing import Any, Callable
from ..styles import *
from ..widgets.code_preview_window import CodePreviewWindow
from ..widgets.universal_context_menu import create_universal_context_menu


class BaseEditorBody(tk.Frame):
    """
    Базовый класс для "тела" любого редактора.
    Создает унифицированную трехпанельную разметку.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, bg=BG_PRIMARY)
        self.app = app
        self.service: Any | None = None
        self._code_preview_window: CodePreviewWindow | None = None

        # --- Панели ---
        self.properties_panel: tk.Frame | None = None
        self.canvas: tk.Canvas | None = None
        self.actions_panel: tk.Frame | None = None

        self.context_menu: tk.Menu | None = None

        self._setup_layout()

    def _setup_layout(self):
        """Создает трехпанельную разметку."""
        # Используем PanedWindow для возможности изменять размеры панелей
        main_paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, bg=BG_PRIMARY)
        main_paned_window.pack(fill=tk.BOTH, expand=True)

        # 1. Левая панель (Свойства)
        self.properties_panel = tk.Frame(main_paned_window, bg=BG_PRIMARY)
        main_paned_window.add(self.properties_panel, width=300, minsize=250)

        # 2. Центральная панель (Холст)
        self.canvas = tk.Canvas(main_paned_window, bg=BG_CANVAS, highlightthickness=0)
        main_paned_window.add(self.canvas, stretch="always")

        # 3. Правая панель (Действия)
        self.actions_panel = tk.Frame(main_paned_window, bg=BG_PRIMARY)
        # ИЗМЕНЕНИЕ: Устанавливаем фиксированную ширину 200, как на скриншоте.
        main_paned_window.add(self.actions_panel, width=200, minsize=180)

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

    # --- Методы для привязки команд к кнопкам в ActionsPanel ---

    def bind_save_command(self, command: Callable[[], None]):
        if hasattr(self.actions_panel, 'save_button') and self.actions_panel.save_button:
            self.actions_panel.save_button.config(command=command)

    def bind_delete_command(self, command: Callable[[], None]):
        if hasattr(self.actions_panel, 'delete_button') and self.actions_panel.delete_button:
            self.actions_panel.delete_button.config(command=command)

    def bind_new_command(self, command: Callable[[], None]):
        if hasattr(self.actions_panel, 'new_button') and self.actions_panel.new_button:
            self.actions_panel.new_button.config(command=command)

    def bind_show_code_command(self, command: Callable[[Any, str], None], title: str):
        if hasattr(self.actions_panel, 'show_code_button') and self.actions_panel.show_code_button:
            # Предполагается, что дочерний класс реализует get_form_data()
            self.actions_panel.show_code_button.config(command=lambda: command(self.get_form_data(), title))

    # ИЗМЕНЕНИЕ: Новые методы для привязки команд к кнопкам палитр
    def bind_node_palette_command(self, command: Callable[[], None]):
        if hasattr(self.actions_panel, 'node_palette_button') and self.actions_panel.node_palette_button:
            self.actions_panel.node_palette_button.config(command=command)

    def bind_block_palette_command(self, command: Callable[[], None]):
        if hasattr(self.actions_panel, 'block_palette_button') and self.actions_panel.block_palette_button:
            self.actions_panel.block_palette_button.config(command=command)

    def bind_location_palette_command(self, command: Callable[[], None]):
        if hasattr(self.actions_panel, 'location_palette_button') and self.actions_panel.location_palette_button:
            self.actions_panel.location_palette_button.config(command=command)

    def get_form_data(self) -> dict:
        """Должен быть реализован в дочернем классе."""
        raise NotImplementedError