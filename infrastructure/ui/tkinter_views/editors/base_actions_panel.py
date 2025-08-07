# File: infrastructure/ui/tkinter_views/editors/base_actions_panel.py
import tkinter as tk
from typing import Any, List, Optional
from ..styles import *


class BaseActionsPanel(tk.Frame):
    """
    Базовый класс для новой правой панели Действий.
    Создает универсальные кнопки, общие для всех редакторов.
    """

    def __init__(self, master, app: Any, palettes_to_show: Optional[List[str]] = None):
        super().__init__(master, bg=BG_PRIMARY, width=200, padx=5, pady=5)
        self.app = app

        # ИЗМЕНЕНИЕ: Если список палитр не передан, показываем все по умолчанию
        self.palettes_to_show = palettes_to_show if palettes_to_show is not None else ['nodes', 'blocks', 'locations']

        # --- Виджеты ---
        self.save_button: tk.Button | None = None
        self.delete_button: tk.Button | None = None
        self.new_button: tk.Button | None = None
        self.show_code_button: tk.Button | None = None

        self.node_palette_button: tk.Button | None = None
        self.block_palette_button: tk.Button | None = None
        self.location_palette_button: tk.Button | None = None

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

        # ИЗМЕНЕНИЕ: Создаем кнопки только для разрешенных палитр
        if 'nodes' in self.palettes_to_show:
            self.node_palette_button = tk.Button(palette_frame, text="Палитра Нодов", bg=BG_SECONDARY, fg=FG_TEXT,
                                                 command=lambda: self._open_palette("nodes"))
            self.node_palette_button.pack(fill=tk.X, pady=2)

        if 'blocks' in self.palettes_to_show:
            self.block_palette_button = tk.Button(palette_frame, text="Палитра Блоков", bg=BG_SECONDARY, fg=FG_TEXT,
                                                  command=lambda: self._open_palette("blocks"))
            self.block_palette_button.pack(fill=tk.X, pady=2)

        if 'locations' in self.palettes_to_show:
            self.location_palette_button = tk.Button(palette_frame, text="Палитра Локаций", bg=BG_SECONDARY, fg=FG_TEXT,
                                                     command=lambda: self._open_palette("locations"))
            self.location_palette_button.pack(fill=tk.X, pady=2)

    def _open_palette(self, palette_type: str):
        """
        Вспомогательный метод для вызова метода open_palette() в главном приложении.
        """
        x = self.app.winfo_pointerx()
        y = self.app.winfo_pointery()
        self.app.open_palette(palette_type, x, y)