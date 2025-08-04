# File: infrastructure/ui/tkinter_views/editors/block/block_editor_view.py (version 2.1)
import tkinter as tk
from tkinter import ttk
from interfaces.ui.i_block_editor_view import IBlockEditorView
from .block_editor_controls import BlockEditorControls
from typing import Any, Callable, List
from interfaces.persistence.i_node_repository import INodeRepository
import json
from ...base_editor_view import BaseEditorView


class BlockEditorView(BaseEditorView, IBlockEditorView):
    def __init__(self, master, app: Any, node_repo: INodeRepository):
        super().__init__(master, app)
        self.node_repo = node_repo

        self._block_data: dict = self.get_initial_data()
        self._tile_size = 0
        self._on_canvas_click_callback = None
        self.controls = None
        self.FIXED_GRID_SIZE = 300
        self.block_canvas = None

        self._setup_ui()
        self._set_initial_data()  # <-- Добавлен вызов для установки начальных данных
        self.draw_block_on_canvas()

    def get_initial_data(self) -> dict:
        return {
            'block_key': '',
            'display_name': '',
            'nodes_structure': [[None for _ in range(3)] for _ in range(3)],
            'nodes_data': {}
        }

    def _set_initial_data(self):
        """Устанавливает базовые значения при запуске редактора."""
        data = {
            'block_key': 'new_block_key',
            'display_name': 'Новый Блок',
            'nodes_structure': [[None for _ in range(3)] for _ in range(3)],
            'nodes_data': {}
        }
        self.set_form_data(data)

    def _setup_ui(self):
        self.three_panel_layout()

        self.block_canvas = tk.Canvas(self.center_frame, bg="#222222", highlightthickness=0)
        self.block_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.block_canvas.bind("<Button-1>", self._on_canvas_click)
        self.block_canvas.bind("<Configure>", self._on_canvas_configure)

        self._create_context_menu_for_canvas(self.block_canvas)

        self.controls = BlockEditorControls(self.right_frame, parent_view=self)
        self.controls.pack(fill=tk.BOTH, expand=True)

        self.bind_show_code_command(self._show_code_preview_window)

    def _on_canvas_configure(self, event):
        self.draw_block_on_canvas()

    def _on_canvas_click(self, event):
        if self._on_canvas_click_callback:
            canvas_width = self.block_canvas.winfo_width()
            canvas_height = self.block_canvas.winfo_height()

            grid_size = min(min(canvas_width, canvas_height), self.FIXED_GRID_SIZE)
            self._tile_size = grid_size // 3

            x_offset = (canvas_width - grid_size) // 2
            y_offset = (canvas_height - grid_size) // 2

            col = int((event.x - x_offset) / self._tile_size)
            row = int((event.y - y_offset) / self._tile_size)

            if 0 <= row < 3 and 0 <= col < 3:
                self._on_canvas_click_callback(row, col)

    def set_form_data(self, data: dict) -> None:
        self.controls.entry_block_key.delete(0, tk.END)
        self.controls.entry_block_key.insert(0, data.get('block_key', ''))

        self.controls.entry_display_name.delete(0, tk.END)
        self.controls.entry_display_name.insert(0, data.get('display_name', ''))

        self._block_data = data
        self.draw_block_on_canvas()

    def get_form_data(self) -> dict:
        self._block_data['block_key'] = self.controls.entry_block_key.get()
        self._block_data['display_name'] = self.controls.entry_display_name.get()
        return self._block_data

    def clear_form(self) -> None:
        self.controls.entry_block_key.delete(0, tk.END)
        self.controls.entry_display_name.delete(0, tk.END)
        self.controls.set_selected_node_id(None)
        self._block_data = self.get_initial_data()
        self.block_canvas.delete("all")
        self.draw_block_on_canvas()

    def draw_block_on_canvas(self) -> None:
        self.block_canvas.delete("all")
        canvas_width = self.block_canvas.winfo_width()
        canvas_height = self.block_canvas.winfo_height()

        grid_size = min(min(canvas_width, canvas_height), self.FIXED_GRID_SIZE)
        self._tile_size = grid_size // 3

        x_offset = (canvas_width - grid_size) // 2
        y_offset = (canvas_height - grid_size) // 2

        nodes_structure = self._block_data['nodes_structure']
        for r in range(3):
            for c in range(3):
                x1 = x_offset + c * self._tile_size
                y1 = y_offset + r * self._tile_size
                x2 = x1 + self._tile_size
                y2 = y1 + self._tile_size

                node_id = nodes_structure[r][c]
                fill_color = self._get_color_for_node(node_id)

                self.block_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="#222222")

    def _get_color_for_node(self, node_id: str | None) -> str:
        if not node_id:
            return "#444444"

        nodes_data = self._block_data['nodes_data']
        if node_id in nodes_data:
            node_key = nodes_data[node_id].get('node_key')
            if node_key:
                node_template = self.node_repo.get_by_key(node_key)
                return node_template.get('color', '#ff00ff') if node_template else '#ff00ff'

        return '#ff00ff'

    def bind_canvas_click(self, callback: Callable[[int, int], None]):
        self._on_canvas_click_callback = callback

    def bind_list_selection_command(self, command: Callable[[Any], None]) -> None:
        pass

    def show_node_properties(self, node_id: str) -> None:
        """Отображает свойства выбранного нода в правой панели."""
        self.controls.set_selected_node_id(node_id)

        nodes_data = self._block_data['nodes_data']
        node_key = nodes_data[node_id].get('node_key')

        node_template = self.node_repo.get_by_key(node_key)
        if node_template:
            self.controls.display_node_properties(node_template)
        else:
            self.controls.clear_custom_properties()