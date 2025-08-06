# File: infrastructure/ui/tkinter_views/editors/location/location_editor_view.py
import tkinter as tk
from typing import Any, Dict, Optional, Callable

from infrastructure.persistence.json_node_repository import JsonNodeRepository
from interfaces.ui.i_location_editor_view import ILocationEditorView
from ...base_editor_view import BaseEditorView
from .location_editor_controls import LocationEditorControls
from ...styles import *


class LocationEditorView(BaseEditorView, ILocationEditorView):
    """
    Основной класс View для редактора локаций с поддержкой масштабирования и панорамирования.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, app)
        self.controls: Optional[LocationEditorControls] = None
        self.location_canvas: Optional[tk.Canvas] = None
        self.location_data: Optional[Dict[str, Any]] = None

        # --- 1. ПЕРЕМЕННЫЕ ДЛЯ НАВИГАЦИИ ---
        self.base_node_size = 32
        self.zoom_level = 1.0
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self._pan_start_x = 0
        self._pan_start_y = 0

        self.node_repo = JsonNodeRepository()
        self.node_templates = self.node_repo.get_all()

        self._setup_ui()
        # --- 2. ПРИВЯЗКА СОБЫТИЙ МЫШИ ---
        self.location_canvas.bind("<Configure>", lambda e: self.draw_canvas())
        self.location_canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.location_canvas.bind("<ButtonPress-2>", self._on_pan_start)  # Нажатие колесика
        self.location_canvas.bind("<B2-Motion>", self._on_pan_move)  # Движение с зажатым колесиком

    def _setup_ui(self):
        """Создает базовую трехпанельную структуру для редактора."""
        self.three_panel_layout()
        self.controls = LocationEditorControls(self.right_frame, self)
        self.controls.pack(fill=tk.BOTH, expand=True)
        self.location_canvas = tk.Canvas(self.center_frame, bg=BG_CANVAS, highlightthickness=0)
        self.location_canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        self._create_context_menu_for_canvas(self.location_canvas)
        self.bind_show_code_command(self._show_code_preview_window, "Код данных локации")

    def _on_mouse_wheel(self, event):
        """Обрабатывает прокрутку колесика мыши для изменения масштаба."""
        if event.delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level /= 1.1
        self.zoom_level = max(0.1, min(self.zoom_level, 5.0))
        self.draw_canvas()

    # --- 3. НОВЫЕ МЕТОДЫ ДЛЯ ПЕРЕМЕЩЕНИЯ ---
    def _on_pan_start(self, event):
        """Запоминает начальную точку при зажатии колесика мыши."""
        self._pan_start_x = event.x
        self._pan_start_y = event.y

    def _on_pan_move(self, event):
        """Вычисляет смещение и перерисовывает холст при движении мыши."""
        dx = event.x - self._pan_start_x
        dy = event.y - self._pan_start_y

        self.pan_offset_x += dx
        self.pan_offset_y += dy

        self._pan_start_x = event.x
        self._pan_start_y = event.y

        self.draw_canvas()

    def draw_canvas(self):
        """Отрисовывает всю локацию на холсте с учетом смещения и масштаба."""
        if not self.location_canvas or not self.location_data:
            return

        self.location_canvas.delete("all")

        node_size = self.base_node_size * self.zoom_level
        if node_size < 1: return

        # --- 4. УЧИТЫВАЕМ СМЕЩЕНИЕ ПРИ ОТРИСОВКЕ ---
        canvas_width = self.location_canvas.winfo_width()
        canvas_height = self.location_canvas.winfo_height()
        # Центрируем карту и добавляем смещение от панорамирования
        x_offset = (canvas_width / 2) - (4.5 * node_size) + self.pan_offset_x
        y_offset = (canvas_height / 2) - (4.5 * node_size) + self.pan_offset_y

        root_module = self.location_data.get("root_module", {})
        module_structure = root_module.get("structure", [])
        blocks_data = root_module.get("blocks_data", {})

        for block_row, block_cols in enumerate(module_structure):
            for block_col, block_idx in enumerate(block_cols):
                block = blocks_data.get(block_idx, {})
                nodes_structure = block.get("nodes_structure", [])
                nodes_data = block.get("nodes_data", {})

                for node_row, node_cols in enumerate(nodes_structure):
                    for node_col, node_idx in enumerate(node_cols):
                        node = nodes_data.get(node_idx, {})
                        template_key = node.get("template_key", "void")

                        node_template = self.node_templates.get(template_key, {})
                        fill_color = node_template.get("color", ERROR_COLOR)

                        global_node_col = block_col * 3 + node_col
                        global_node_row = block_row * 3 + node_row

                        x1 = x_offset + global_node_col * node_size
                        y1 = y_offset + global_node_row * node_size
                        x2 = x1 + node_size
                        y2 = y1 + node_size

                        self.location_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=BG_CANVAS)

    def set_form_data(self, data: Dict[str, Any]):
        """Сохраняет данные локации и инициирует перерисовку."""
        self.location_data = data
        self.draw_canvas()

    def get_form_data(self) -> Dict[str, Any]:
        return self.location_data or {}

    def clear_form(self) -> None:
        self.location_data = None
        self.draw_canvas()

    def bind_canvas_click(self, command: Callable[[Any], None]) -> None:
        self.location_canvas.bind("<Button-1>", command)
