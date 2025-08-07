# File: infrastructure/ui/tkinter_views/editors/block/block_editor_body.py
import tkinter as tk
from typing import Any, Callable, Dict, Optional

from .block_properties_panel import BlockPropertiesPanel
from .block_actions_panel import BlockActionsPanel
from ..base_editor_body import BaseEditorBody
from ...styles import *


class BlockEditorBody(BaseEditorBody):
    """
    Основное "тело" для Редактора Блоков.
    Собирает воедино панель свойств, холст и панель действий.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, app)

        # --- Атрибуты, специфичные для этого редактора ---
        self._block_data: dict = self.get_initial_data()
        self._on_canvas_click_callback: Callable | None = None
        self.FIXED_GRID_SIZE = 300  # Фиксированный размер для предпросмотра блока

        # --- Заменяем заглушки на реальные панели ---
        self.properties_panel = BlockPropertiesPanel(self.properties_panel, self.app)
        self.properties_panel.pack(fill=tk.BOTH, expand=True)

        self.actions_panel = BlockActionsPanel(self.actions_panel, self.app)
        self.actions_panel.pack(fill=tk.BOTH, expand=True)

        # --- Настройка холста ---
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Configure>", lambda e: self.draw_block_on_canvas())
        self._create_context_menu_for_canvas()

        self._set_initial_data()

    def get_initial_data(self) -> dict:
        """Возвращает пустую структуру данных для нового блока."""
        return {
            'block_key': 'new_block',
            'display_name': 'Новый Блок',
            'tags': [],
            'width': 3,
            'height': 3,
            'nodes_structure': [[None for _ in range(3)] for _ in range(3)],
            'nodes_data': {},
            'calculated_exits': {}
        }

    def _set_initial_data(self):
        """Устанавливает базовые значения при запуске редактора."""
        data = self.get_initial_data()
        self.set_form_data(data)

    def set_form_data(self, data: dict) -> None:
        """Обновляет все части редактора: данные, панель свойств и холст."""
        self._block_data = data
        if self.properties_panel:
            self.properties_panel.set_data(data)
        self.draw_block_on_canvas()

    def get_form_data(self) -> dict:
        """Собирает данные из панели свойств и объединяет их с данными о нодах."""
        if not self.properties_panel:
            return self._block_data

        metadata = self.properties_panel.get_data()
        self._block_data.update(metadata)
        return self._block_data

    def clear_form(self) -> None:
        """Сбрасывает редактор к начальному состоянию."""
        self._set_initial_data()

    def draw_block_on_canvas(self) -> None:
        """Отрисовывает блок на холсте."""
        if not self.canvas: return
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1: return

        nodes_structure = self._block_data.get('nodes_structure', [])
        nodes_data = self._block_data.get('nodes_data', {})

        if not nodes_structure or not nodes_structure[0]: return

        grid_size = min(min(canvas_width, canvas_height), self.FIXED_GRID_SIZE)
        height = len(nodes_structure)
        width = len(nodes_structure[0])
        tile_size = min(grid_size // width, grid_size // height)
        if tile_size == 0: return

        x_offset = (canvas_width - width * tile_size) // 2
        y_offset = (canvas_height - height * tile_size) // 2

        for r, row in enumerate(nodes_structure):
            for c, node_id in enumerate(row):
                x1 = x_offset + c * tile_size
                y1 = y_offset + r * tile_size
                x2 = x1 + tile_size
                y2 = y1 + tile_size

                node_details = nodes_data.get(str(node_id))
                fill_color = node_details.get('color', BG_SECONDARY) if node_details else BG_SECONDARY
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=BG_CANVAS)

    def _on_canvas_click(self, event):
        """Обрабатывает клик по холсту и передает его в Service."""
        if not self._on_canvas_click_callback or not self.canvas: return

        nodes_structure = self._block_data.get('nodes_structure', [])
        if not nodes_structure or not nodes_structure[0]: return

        height = len(nodes_structure)
        width = len(nodes_structure[0])
        grid_size = min(min(self.canvas.winfo_width(), self.canvas.winfo_height()), self.FIXED_GRID_SIZE)
        tile_size = min(grid_size // width, grid_size // height)
        if tile_size == 0: return

        x_offset = (self.canvas.winfo_width() - width * tile_size) // 2
        y_offset = (self.canvas.winfo_height() - height * tile_size) // 2

        col = int((event.x - x_offset) / tile_size)
        row = int((event.y - y_offset) / tile_size)

        if 0 <= row < height and 0 <= col < width:
            node_id_in_structure = nodes_structure[row][col]
            self._on_canvas_click_callback(row, col, node_id_in_structure)

    def bind_canvas_click(self, callback: Callable[[int, int, str | None], None]):
        """Привязывает команду клика по холсту к Service."""
        self._on_canvas_click_callback = callback
