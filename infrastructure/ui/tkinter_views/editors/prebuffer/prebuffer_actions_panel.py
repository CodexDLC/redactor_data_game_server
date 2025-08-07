# File: infrastructure/ui/tkinter_views/editors/prebuffer/prebuffer_actions_panel.py
import tkinter as tk
from typing import Any
from ..base_actions_panel import BaseActionsPanel
from ...styles import *


class PrebufferActionsPanel(BaseActionsPanel):
    def __init__(self, master, app: Any):
        self.show_code_button: tk.Button | None = None
        # NEW: Button for saving the object
        self.save_object_button: tk.Button | None = None
        super().__init__(master, app, palettes_to_show=['blocks'])

    def _build_ui(self):
        actions_frame = tk.LabelFrame(self, text="Действия", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        actions_frame.pack(fill=tk.X, side=tk.TOP)

        # CHANGE: Rename the save button to be more specific
        self.save_button = tk.Button(actions_frame, text="Сохранить Шаблон", bg=BG_SECONDARY, fg=FG_TEXT)
        self.save_button.pack(fill=tk.X, pady=2)

        # NEW: Add a button to save the object
        self.save_object_button = tk.Button(actions_frame, text="Сохранить Объект", bg=BG_SECONDARY, fg=FG_TEXT)
        self.save_object_button.pack(fill=tk.X, pady=2)

        self.delete_button = tk.Button(actions_frame, text="Удалить", bg=BG_SECONDARY, fg=FG_TEXT)
        self.delete_button.pack(fill=tk.X, pady=2)

        self.new_button = tk.Button(actions_frame, text="Создать новый", bg=BG_SECONDARY, fg=FG_TEXT)
        self.new_button.pack(fill=tk.X, pady=2)

        self.show_code_button = tk.Button(actions_frame, text="Показать код", bg=BG_SECONDARY, fg=FG_TEXT)
        self.show_code_button.pack(fill=tk.X, pady=2)

        palette_frame = tk.LabelFrame(self, text="Палитры", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        palette_frame.pack(fill=tk.X, side=tk.TOP, pady=10)

        if 'blocks' in self.palettes_to_show:
            self.block_palette_button = tk.Button(palette_frame, text="Палитра Блоков", bg=BG_SECONDARY, fg=FG_TEXT,
                                                  command=lambda: self._open_palette("blocks"))
            self.block_palette_button.pack(fill=tk.X, pady=2)

    def _open_palette(self, palette_type: str):
        x = self.app.winfo_pointerx()
        y = self.app.winfo_pointery()
        self.app.open_palette(palette_type, x, y)