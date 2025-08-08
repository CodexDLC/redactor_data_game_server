# File: infrastructure/ui/tkinter_views/editors/location/location_actions_panel.py
import tkinter as tk
from typing import Any
from ..base_actions_panel import BaseActionsPanel
from ...styles import *


class LocationActionsPanel(BaseActionsPanel):
    """
    Панель действий для редактора локаций.
    Наследуется от BaseActionsPanel, чтобы использовать стандартные кнопки.
    """
    def __init__(self, master, app: Any):
        super().__init__(master, app, palettes_to_show=None)
        # У этого редактора не будет палитр, поэтому palettes_to_show=None

    def _build_ui(self):
        actions_frame = tk.LabelFrame(self, text="Действия", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        actions_frame.pack(fill=tk.X, side=tk.TOP)

        self.save_button = tk.Button(actions_frame, text="Сохранить", bg=BG_SECONDARY, fg=FG_TEXT)
        self.save_button.pack(fill=tk.X, pady=2)

        self.delete_button = tk.Button(actions_frame, text="Удалить", bg=BG_SECONDARY, fg=FG_TEXT)
        self.delete_button.pack(fill=tk.X, pady=2)

        self.new_button = tk.Button(actions_frame, text="Создать новый", bg=BG_SECONDARY, fg=FG_TEXT)
        self.new_button.pack(fill=tk.X, pady=2)