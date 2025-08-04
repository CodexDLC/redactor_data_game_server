# File: infrastructure/ui/tkinter_views/editors/block/block_editor_view.py
import tkinter as tk
from typing import Any, Callable, Dict

from interfaces.ui.i_block_editor_view import IBlockEditorView
from .block_editor_controls import BlockEditorControls
from ...base_editor_view import BaseEditorView
from ...styles import *


class BlockEditorView(BaseEditorView, IBlockEditorView):
    """
    View-слой редактора блоков.
    Выступает в роли посредника между Service (логика) и Controls (UI).
    """

    def __init__(self, master, app: Any, node_schema: Dict[str, Any]):
        super().__init__(master, app)
        self.node_schema = node_schema  # Может понадобиться для передачи в Controls в будущем
        self._block_data: dict = self.get_initial_data()
        self._on_canvas_click_callback = None

        self.FIXED_GRID_SIZE = 300
        self.block_canvas = None

        self._setup_ui()
        self._set_initial_data()

    def _setup_ui(self):
        self.three_panel_layout()

        self.block_canvas = tk.Canvas(self.center_frame, bg=BG_CANVAS, highlightthickness=0)
        self.block_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.block_canvas.bind("<Button-1>", self._on_canvas_click)
        self.block_canvas.bind("<Configure>", lambda e: self.draw_block_on_canvas())
        self._create_context_menu_for_canvas(self.block_canvas)

        # Controls теперь создается без репозиториев
        self.controls = BlockEditorControls(self.right_frame, parent_view=self)
        self.controls.pack(fill=tk.BOTH, expand=True)

        self.bind_show_code_command(self._show_code_preview_window, "Код данных блока")

    def get_initial_data(self) -> dict:
        """Возвращает пустую структуру данных для блока."""
        return {
            'block_key': '',
            'display_name': '',
            'nodes_structure': [[None for _ in range(3)] for _ in range(3)],
            'nodes_data': {}
        }

    def _set_initial_data(self):
        """Устанавливает базовые значения при запуске редактора."""
        data = self.get_initial_data()
        data['block_key'] = 'new_block_key'
        data['display_name'] = 'Новый Блок'
        self.set_form_data(data)

    def set_form_data(self, data: dict) -> None:
        """
        Основной метод для обновления всего View.
        Передает данные в Controls и перерисовывает холст.
        """
        self._block_data = data
        if self.controls:
            self.controls.set_block_data(data)
        self.draw_block_on_canvas()

    def get_form_data(self) -> dict:
        """
        Собирает данные со всех частей UI в единый словарь.
        """
        if not self.controls:
            return self._block_data

        # 1. Получаем базовые свойства блока
        self._block_data['block_key'] = self.controls.entry_block_key.get()
        self._block_data['display_name'] = self.controls.entry_display_name.get()

        # 2. Получаем ID выбранного нода
        selected_node_id = self.controls.selected_node_id
        if not selected_node_id:
            return self._block_data

        # 3. Получаем обновленные свойства для этого нода
        updated_properties = self.controls.get_properties_data() # <-- ИЗМЕНЕНО: теперь вызываем новый метод

        # 4. Обновляем данные только для выбранного нода
        if selected_node_id in self._block_data['nodes_data']:
            # Объединяем старые свойства с новыми
            current_properties = self._block_data['nodes_data'][selected_node_id].get('properties', {})
            current_properties.update(updated_properties)
            self._block_data['nodes_data'][selected_node_id]['properties'] = current_properties

        return self._block_data

    def clear_form(self) -> None:
        """Очищает форму и сбрасывает ее к начальному состоянию."""
        self._set_initial_data()

    def draw_block_on_canvas(self) -> None:
        """Отрисовывает блок на холсте на основе _block_data."""
        self.block_canvas.delete("all")
        canvas_width = self.block_canvas.winfo_width()
        canvas_height = self.block_canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1: return

        grid_size = min(min(canvas_width, canvas_height), self.FIXED_GRID_SIZE)
        tile_size = grid_size // 3
        if tile_size == 0: return

        x_offset = (canvas_width - grid_size) // 2
        y_offset = (canvas_height - grid_size) // 2

        nodes_structure = self._block_data.get('nodes_structure', [])
        for r, row in enumerate(nodes_structure):
            for c, node_id in enumerate(row):
                x1 = x_offset + c * tile_size
                y1 = y_offset + r * tile_size
                x2 = x1 + tile_size
                y2 = y1 + tile_size

                node_data = self._block_data.get('nodes_data', {}).get(node_id)
                fill_color = node_data.get('color', BG_SECONDARY) if node_data else BG_SECONDARY
                self.block_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=BG_CANVAS)

    def _on_canvas_click(self, event):
        """Обрабатывает клик по холсту и передает его в Service."""
        if not self._on_canvas_click_callback: return

        canvas_width = self.block_canvas.winfo_width()
        canvas_height = self.block_canvas.winfo_height()
        grid_size = min(min(canvas_width, canvas_height), self.FIXED_GRID_SIZE)
        tile_size = grid_size // 3
        if tile_size == 0: return

        x_offset = (canvas_width - grid_size) // 2
        y_offset = (canvas_height - grid_size) // 2

        col = int((event.x - x_offset) / tile_size)
        row = int((event.y - y_offset) / tile_size)

        if 0 <= row < 3 and 0 <= col < 3:
            node_id = self._block_data['nodes_structure'][row][col]
            self._on_canvas_click_callback(row, col, node_id)

    # --- Новые и обновленные методы-посредники ---

    def display_node_properties(self, properties_data: Dict[str, Any]):
        if self.controls:
            print(f"Данные о свойствах, передаваемые в Controls: {properties_data}")
            self.controls.display_available_properties(properties_data)

    def bind_request_node_properties(self, command: Callable[[str], None]) -> None:
        """
        Новый метод. Привязывает команду из Service, которая будет вызываться,
        когда Controls запросит данные о свойствах нода.
        """
        # Мы сохраняем команду, чтобы вызвать ее, когда Controls попросит
        self.request_properties_for_node = command

    def bind_canvas_click(self, callback: Callable[[int, int, str | None], None]):
        """Привязывает команду клика по холсту к Service."""
        self._on_canvas_click_callback = callback