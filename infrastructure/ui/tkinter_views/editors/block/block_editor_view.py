# File: infrastructure/ui/tkinter_views/editors/block/block_editor_view.py
import tkinter as tk
from typing import Any, Callable, Dict, Optional

from interfaces.ui.i_block_editor_view import IBlockEditorView
from .block_editor_controls import BlockEditorControls
from ...base_editor_view import BaseEditorView
from ...styles import *


class BlockEditorView(BaseEditorView, IBlockEditorView):
    """
    Упрощенный View-слой редактора блоков.
    Работает с простой панелью Controls и не занимается свойствами нодов.
    """
    def __init__(self, master, app: Any):
        super().__init__(master, app)
        self.service: Optional[Any] = None
        self._block_data: dict = self.get_initial_data()
        self._on_canvas_click_callback: Callable | None = None

        self.FIXED_GRID_SIZE = 300
        self.block_canvas: tk.Canvas | None = None
        self.controls: BlockEditorControls | None = None

        self._setup_ui()
        self._set_initial_data()

    def _setup_ui(self):
        hint_text = "Подсказка: ПКМ по холсту для вызова 'Палитры Кирпичиков'"
        hint_bar = tk.Label(self, text=hint_text, fg=FG_TEXT, bg=BG_SECONDARY, anchor='w', padx=10)
        hint_bar.pack(fill=tk.X, side=tk.TOP, padx=5, pady=(0, 5))

        self.three_panel_layout()

        self.block_canvas = tk.Canvas(self.center_frame, bg=BG_CANVAS, highlightthickness=0)
        self.block_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.block_canvas.bind("<Button-1>", self._on_canvas_click)
        self.block_canvas.bind("<Configure>", lambda e: self.draw_block_on_canvas())
        self._create_context_menu_for_canvas(self.block_canvas)

        self.controls = BlockEditorControls(self.right_frame, parent_view=self)
        self.controls.pack(fill=tk.BOTH, expand=True)

        self.bind_show_code_command(self._show_code_preview_window, "Код данных блока")

    def get_initial_data(self) -> dict:
        """Возвращает пустую структуру данных для блока."""
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
        """Обновляет View: сохраняет данные, передает их в Controls и перерисовывает холст."""
        self._block_data = data
        if self.controls:
            self.controls.set_data(data)
            self.controls.set_exits_data(data.get('calculated_exits', {}))
        self.draw_block_on_canvas()

    def get_form_data(self) -> dict:
        """
        Собирает данные из Controls и объединяет их с текущими данными о нодах.
        """
        if not self.controls:
            return self._block_data

        # Получаем метаданные (key, name, tags) из панели Controls
        metadata = self.controls.get_data()

        # Обновляем наш основной словарь данных этой метаинформацией
        self._block_data.update(metadata)

        return self._block_data

    def clear_form(self) -> None:
        """Очищает форму и сбрасывает ее к начальному состоянию."""
        self._set_initial_data()

    def draw_block_on_canvas(self) -> None:
        """Отрисовывает блок на холсте на основе _block_data."""
        if not self.block_canvas: return
        self.block_canvas.delete("all")
        canvas_width = self.block_canvas.winfo_width()
        canvas_height = self.block_canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1: return

        nodes_structure = self._block_data.get('nodes_structure', [])
        nodes_data = self._block_data.get('nodes_data', {})

        # Проверяем, что nodes_structure не пустая
        if not nodes_structure or not nodes_structure[0]:
            return

        grid_size = min(min(canvas_width, canvas_height), self.FIXED_GRID_SIZE)

        # Определяем размер сетки из данных
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
                self.block_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=BG_CANVAS)

    def _on_canvas_click(self, event):
        """Обрабатывает клик по холсту и передает его в Service."""
        if not self._on_canvas_click_callback: return

        nodes_structure = self._block_data.get('nodes_structure', [])
        if not nodes_structure or not nodes_structure[0]:
            return

        height = len(nodes_structure)
        width = len(nodes_structure[0])
        grid_size = min(min(self.block_canvas.winfo_width(), self.block_canvas.winfo_height()), self.FIXED_GRID_SIZE)
        tile_size = min(grid_size // width, grid_size // height)
        if tile_size == 0: return

        x_offset = (self.block_canvas.winfo_width() - width * tile_size) // 2
        y_offset = (self.block_canvas.winfo_height() - height * tile_size) // 2

        col = int((event.x - x_offset) / tile_size)
        row = int((event.y - y_offset) / tile_size)

        if 0 <= row < height and 0 <= col < width:
            node_id_in_structure = nodes_structure[row][col]
            self._on_canvas_click_callback(row, col, node_id_in_structure)


    def bind_canvas_click(self, callback: Callable[[int, int, str | None], None]):
        """Привязывает команду клика по холсту к Service."""
        self._on_canvas_click_callback = callback