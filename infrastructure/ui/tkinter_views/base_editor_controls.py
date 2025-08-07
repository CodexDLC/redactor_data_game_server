# File: infrastructure/ui/tkinter_views/base_editor_controls.py
import tkinter as tk
from typing import Any
from .styles import *


class BaseEditorControls(tk.Frame):
    """
    Базовый класс для панелей управления редакторами.
    Содержит общую "Зону Действий" и предоставляет интерфейс
    для добавления специфических свойств.
    """

    def __init__(self, master, parent_view: Any):
        super().__init__(master, bg=BG_PRIMARY)
        self.parent_view = parent_view
        self.save_button = None
        self.delete_button = None
        self.new_button = None
        self.show_code_button = None
        self.actions_frame = None # <-- ДОБАВЛЕНО: Инициализируем атрибут

        self._build_ui()

    def _build_ui(self):
        # Эта зона будет заполнена в дочерних классах
        # Зона 1: Основные Свойства
        # Зона 2: Настраиваемые Свойства

        # Зона 3: Действия (общая для всех)
        # --- ИЗМЕНЕНО: Сохраняем рамку в self.actions_frame ---
        self.actions_frame = tk.LabelFrame(self, text="Действия", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        self.actions_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.BOTTOM)

        self.save_button = tk.Button(self.actions_frame, text="Сохранить", bg=BG_SECONDARY, fg=FG_TEXT)
        self.save_button.pack(fill=tk.X, pady=2)

        self.delete_button = tk.Button(self.actions_frame, text="Удалить", bg=BG_SECONDARY, fg=FG_TEXT)
        self.delete_button.pack(fill=tk.X, pady=2)

        self.new_button = tk.Button(self.actions_frame, text="Создать новый", bg=BG_SECONDARY, fg=FG_TEXT)
        self.new_button.pack(fill=tk.X, pady=2)

        self.show_code_button = tk.Button(self.actions_frame, text="Показать код", bg=BG_SECONDARY, fg=FG_TEXT)
        self.show_code_button.pack(fill=tk.X, pady=2)