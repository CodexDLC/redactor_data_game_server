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

    def update_path_display(self, path_components: List[Tuple[str, str]]):
        """
        Обновляет отображаемый иерархический путь, делая его интерактивным.
        :param path_components: Список кортежей, где каждый кортеж - (тип уровня, ID уровня).
                                Например: [('Модуль', 'module_0'), ('Блок', 'block_4'), ('Нода', 'node_0')]
        """
        # Очищаем старый путь
        for widget in self.path_frame.winfo_children():
            widget.destroy()

        # Создаем новый интерактивный путь
        for i, (level_type, level_id) in enumerate(path_components):
            level_frame = tk.Frame(self.path_frame, bg=BG_PRIMARY)
            level_frame.pack(fill=tk.X, padx=10, pady=2)

            # Отступ для имитации иерархии
            indent_label = tk.Label(level_frame, text=" " * (i * 4) + "└─", fg=FG_TEXT, bg=BG_PRIMARY)
            indent_label.pack(side=tk.LEFT)

            # Название уровня и его ID
            id_label = tk.Label(level_frame, text=f"[{level_type}] {level_id}", fg=FG_TEXT, bg=BG_PRIMARY)
            id_label.pack(side=tk.LEFT)

            # Добавляем кнопку "Сохранить", если это не нода
            if level_type != "Нода":
                save_button = tk.Button(
                    level_frame,
                    text="Сохранить как кисточку",
                    bg=BG_SECONDARY,
                    fg=FG_TEXT,
                    # TODO: Привязать команду к сервису
                    command=lambda l_id=level_id: print(f"Сохранение кисточки для {l_id}")
                )
                save_button.pack(side=tk.RIGHT, padx=5)
