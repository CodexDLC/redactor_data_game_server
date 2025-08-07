# File: infrastructure/ui/tkinter_views/editors/location/location_editor_controls.py
import tkinter as tk
from typing import Any, List, Tuple, Optional
from ...base_editor_controls import BaseEditorControls
from ...styles import *


class LocationEditorControls(BaseEditorControls):
    """
    Панель управления для редактора локаций.
    Отображает интерактивный иерархический путь.
    """

    def __init__(self, master, parent_view: Any):
        self.path_frame: Optional[tk.LabelFrame] = None
        self.expand_button: Optional[tk.Button] = None # <-- ДОБАВЛЕНО: Атрибут для кнопки
        super().__init__(master, parent_view)

    def _build_ui(self):
        """Создает UI для правой панели, включая будущую иерархию пути."""

        self.path_frame = tk.LabelFrame(self, text="Путь к элементу", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        self.path_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        # Начальное сообщение
        tk.Label(self.path_frame, text="Кликните на любую ноду...", fg=FG_TEXT, bg=BG_PRIMARY).pack(pady=5)

        props_frame = tk.LabelFrame(self, text="Свойства", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        props_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(props_frame, text="Здесь будут свойства выбранного\nблока или модуля.", justify=tk.LEFT, fg=FG_TEXT,
                 bg=BG_PRIMARY).pack(pady=10)

        super()._build_ui()

        # --- ДОБАВЛЕНО: Кнопка "Увеличить масштаб" добавляется в конец панели Действий ---
        # Мы добавляем ее после вызова super()._build_ui(), чтобы она появилась под остальными кнопками
        self.expand_button = tk.Button(self.actions_frame, text="Увеличить масштаб", bg=BG_SECONDARY, fg=FG_TEXT)
        self.expand_button.pack(fill=tk.X, pady=2, side=tk.BOTTOM) # Используем side=BOTTOM чтобы разместить внизу


    def update_path_display(self, path_components: List[Tuple]):
        """
        Обновляет отображаемый иерархический путь.
        Принимает кортежи, которые могут содержать 2 или 3 элемента.
        """
        for widget in self.path_frame.winfo_children():
            widget.destroy()

        for i, component in enumerate(path_components):
            level_type = component[0]
            level_id = component[1]

            level_frame = tk.Frame(self.path_frame, bg=BG_PRIMARY)
            level_frame.pack(fill=tk.X, padx=10, pady=2)

            indent_label = tk.Label(level_frame, text=" " * (i * 4) + "└─", fg=FG_TEXT, bg=BG_PRIMARY)
            indent_label.pack(side=tk.LEFT)

            # Формируем текстовую метку в зависимости от типа элемента
            if level_type == "Модуль" and len(component) == 3:
                level_number = component[2]
                label_text = f"[{level_type} L{level_number}] {level_id}"
            else:
                label_text = f"[{level_type}] {level_id}"

            id_label = tk.Label(level_frame, text=label_text, fg=FG_TEXT, bg=BG_PRIMARY)
            id_label.pack(side=tk.LEFT)

            # Кнопка сохранения кисточки появляется ТОЛЬКО для модулей
            if level_type == "Модуль":
                save_button = tk.Button(
                    level_frame,
                    text="Сохранить как кисточку",
                    bg=BG_SECONDARY,
                    fg=FG_TEXT,
                    command=lambda l_id=level_id: print(f"Сохранение кисточки для модуля {l_id}")
                )
                save_button.pack(side=tk.RIGHT, padx=5)