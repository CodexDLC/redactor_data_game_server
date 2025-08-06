# File: infrastructure/ui/tkinter_views/editors/location/location_editor_controls.py
import tkinter as tk
from typing import Any
from ...base_editor_controls import BaseEditorControls
from ...styles import *


class LocationEditorControls(BaseEditorControls):
    """
    Панель управления для редактора локаций.
    Наследует общие кнопки от BaseEditorControls.
    """

    def __init__(self, master, parent_view: Any):
        super().__init__(master, parent_view)

    def _build_ui(self):
        """Создает UI для правой панели, включая будущую иерархию пути."""

        # --- Зона 1: Иерархия/Путь (пока заглушка) ---
        path_frame = tk.LabelFrame(self, text="Путь к элементу", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        path_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        # Здесь будет наш интерактивный путь с кнопками "Сохранить как кисточку"
        tk.Label(path_frame, text="dungeon > module_1_1 > ...", fg=FG_TEXT, bg=BG_PRIMARY).pack(pady=5)

        # --- Зона 2: Свойства (пока заглушка) ---
        props_frame = tk.LabelFrame(self, text="Свойства", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        props_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(props_frame, text="Здесь будут свойства выбранного\nблока или модуля.", justify=tk.LEFT, fg=FG_TEXT,
                 bg=BG_PRIMARY).pack(pady=10)

        # --- Зона 3: Действия (общая для всех) ---
        # Вызываем родительский метод, чтобы создать кнопки "Сохранить", "Удалить" и т.д.
        super()._build_ui()
