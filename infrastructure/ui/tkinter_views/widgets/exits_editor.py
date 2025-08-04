# File: infrastructure/ui/tkinter_views/widgets/exits_editor.py
import tkinter as tk
from typing import Callable, Dict, Optional, List

from infrastructure.ui.tkinter_views.styles import *


class ExitsEditorWidget(tk.Frame):
    """
    Кастомный виджет для визуального отображения и обновления выходов (exits) нода.
    Представляет собой сетку 3x3 и кнопку "Обновить".
    """
    # Определим цвета для наглядности
    COLOR_CENTER_NODE = "green"
    COLOR_CONNECTOR_NODE = "yellow"
    COLOR_EXIT_EXISTS = "green"
    COLOR_NO_EXIT = BG_SECONDARY  # Серый

    def __init__(self, master, on_update_request: Callable[[], None]):
        """
        Инициализирует виджет.
        :param master: Родительский виджет.
        :param on_update_request: Функция (callback) для вызова при нажатии кнопки "Обновить".
        """
        super().__init__(master, bg=BG_PRIMARY)
        self.on_update_request_callback = on_update_request
        self.current_exits_data: Dict[str, Optional[str]] = {}  # <-- ДОБАВЛЕНО: Атрибут для хранения данных о выходах

        # Создаем сетку для хранения ячеек-виджетов
        self.cells: List[List[tk.Frame]] = []

        # --- Создание UI ---
        # 1. Рамка для сетки 3x3
        grid_frame = tk.Frame(self, bg=BG_PRIMARY)
        grid_frame.pack(pady=5)

        for r in range(3):
            row_frames = []
            for c in range(3):
                cell = tk.Frame(grid_frame, width=30, height=30, bg=self.COLOR_NO_EXIT,
                                borderwidth=1, relief="solid")
                cell.grid(row=r, column=c, padx=1, pady=1)
                row_frames.append(cell)
            self.cells.append(row_frames)

        # 2. Кнопка "Обновить"
        self.update_button = tk.Button(self, text="Пересчитать выходы",
                                       command=self.on_update_request_callback,
                                       bg=BG_SECONDARY, fg=FG_TEXT)
        self.update_button.pack(fill=tk.X, pady=(5, 0))

    def update_visuals(self, exits_data: Dict[str, Optional[str]], is_connector: bool):
        """
        Основной публичный метод для обновления цветов в сетке на основе новых данных.

        :param exits_data: Словарь с выходами, например {'north': 'id_1', 'east': None, ...}
        :param is_connector: Является ли центральный нод коннектором блока.
        """
        self.current_exits_data = exits_data  # <-- ДОБАВЛЕНО: Сохраняем данные при обновлении

        # 1. Обновляем цвет центральной ячейки
        center_cell = self.cells[1][1]
        center_color = self.COLOR_CONNECTOR_NODE if is_connector else self.COLOR_CENTER_NODE
        center_cell.config(bg=center_color)

        # 2. Обновляем цвета 8 окружающих ячеек
        # Сопоставление имени направления с координатами в нашей сетке 3x3
        direction_coords = {
            "north": (0, 1), "north_east": (0, 2), "east": (1, 2),
            "south_east": (2, 2), "south": (2, 1), "south_west": (2, 0),
            "west": (1, 0), "north_west": (0, 0)
        }

        for direction, (r, c) in direction_coords.items():
            cell_to_update = self.cells[r][c]
            # Если в данных для этого направления есть ID (не None), красим в зеленый. Иначе - в серый.
            if self.current_exits_data.get(direction) is not None:  # <-- ИЗМЕНЕНО: используем сохраненные данные
                cell_to_update.config(bg=self.COLOR_EXIT_EXISTS)
            else:
                cell_to_update.config(bg=self.COLOR_NO_EXIT)

    def get_exits_data(self) -> Dict[str, Optional[str]]:
        """
        <-- НОВЫЙ МЕТОД: Возвращает сохраненные данные о выходах.
        """
        return self.current_exits_data