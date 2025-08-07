# File: infrastructure/ui/tkinter_views/editors/base_actions_panel.py
import tkinter as tk
from typing import Any
from ..styles import *


class BaseActionsPanel(tk.Frame):
    """
    Базовый класс для новой правой панели Действий.
    Создает универсальные кнопки, общие для всех редакторов.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, bg=BG_PRIMARY, width=200, padx=5, pady=5)
        self.app = app

        # --- Виджеты ---
        self.save_button: tk.Button | None = None
        self.delete_button: tk.Button | None = None
        self.new_button: tk.Button | None = None
        self.show_code_button: tk.Button | None = None
        self.open_palette_button: tk.Button | None = None

        self._build_ui()

    def _build_ui(self):
        """Создает набор универсальных кнопок."""
        actions_frame = tk.LabelFrame(self, text="Действия", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        actions_frame.pack(fill=tk.X, side=tk.TOP)

        self.save_button = tk.Button(actions_frame, text="Сохранить", bg=BG_SECONDARY, fg=FG_TEXT)
        self.save_button.pack(fill=tk.X, pady=2)

        self.delete_button = tk.Button(actions_frame, text="Удалить", bg=BG_SECONDARY, fg=FG_TEXT)
        self.delete_button.pack(fill=tk.X, pady=2)

        self.new_button = tk.Button(actions_frame, text="Создать новый", bg=BG_SECONDARY, fg=FG_TEXT)
        self.new_button.pack(fill=tk.X, pady=2)

        self.show_code_button = tk.Button(actions_frame, text="Показать код", bg=BG_SECONDARY, fg=FG_TEXT)
        self.show_code_button.pack(fill=tk.X, pady=2)

        palette_frame = tk.LabelFrame(self, text="Палитры", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        palette_frame.pack(fill=tk.X, side=tk.TOP, pady=10)

        self.open_palette_button = tk.Button(palette_frame, text="Открыть палитру", bg=BG_SECONDARY, fg=FG_TEXT)
        self.open_palette_button.pack(fill=tk.X, pady=2)
