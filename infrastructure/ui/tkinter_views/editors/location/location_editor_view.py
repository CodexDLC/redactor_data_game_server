# File: infrastructure/ui/tkinter_views/editors/location/location_editor_view.py
import tkinter as tk
from typing import Any, Dict, Optional, Callable
import logging

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
        self.service: Optional[Any] = None

        self.base_node_size = 32
        self.zoom_level = 1.0
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self._pan_start_x = 0
        self._pan_start_y = 0

        self.MODULE_SPACING_PX = 2

        self.node_repo = JsonNodeRepository()
        self.node_templates = self.node_repo.get_all()

        self._setup_ui()
        self.location_canvas.bind("<Configure>", lambda e: self.draw_canvas())
        self.location_canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.location_canvas.bind("<ButtonPress-2>", self._on_pan_start)
        self.location_canvas.bind("<B2-Motion>", self._on_pan_move)
        self.location_canvas.bind("<Button-1>", self._on_canvas_left_click)
        logging.info("LocationEditorView: Представление инициализировано.")

    def _setup_ui(self):
        """Создает базовую трехпанельную структуру для редактора."""
        self.three_panel_layout()
        self.controls = LocationEditorControls(self.right_frame, self)
        self.controls.pack(fill=tk.BOTH, expand=True)
        self.location_canvas = tk.Canvas(self.center_frame, bg=BG_CANVAS, highlightthickness=0)
        self.location_canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        self._create_context_menu_for_canvas(self.location_canvas)
        self.bind_show_code_command(self._show_code_preview_window, "Код данных локации")



    # --- НАЧАЛО ИЗМЕНЕНИЙ ---
    def _on_canvas_left_click(self, event):
        """Обрабатывает клик левой кнопкой мыши по холсту."""
        if not self.service or not self.location_data:
            logging.warning("LocationEditorView: Клик по холсту проигнорирован (сервис или данные не готовы).")
            return

        logging.debug(f"LocationEditorView: Зафиксирован клик в пиксельных координатах ({event.x}, {event.y}).")

        root_module = self.location_data.get("root_module", {})
        level = root_module.get("level", 0)

        # Правильная формула для расчета размера карты в нодах по одной стороне.
        # Уровень 0: 3^(0+2) = 9 нодов.
        # Уровень 1: 3^(1+2) = 27 нодов.
        total_size_nodes = 3 ** (level + 2)

        total_pixel_width = self._get_total_pixel_size(level)
        canvas_width = self.location_canvas.winfo_width()
        canvas_height = self.location_canvas.winfo_height()

        # Верхний левый угол отрисованной карты
        start_x = (canvas_width - total_pixel_width) / 2 + self.pan_offset_x
        start_y = (canvas_height - total_pixel_width) / 2 + self.pan_offset_y

        # Координаты клика относительно карты
        map_x = event.x - start_x
        map_y = event.y - start_y

        # Простое преобразование в нодовые координаты
        # (грубое, т.к. не учитывает отступы, но должно быть лучше чем раньше)
        row = int((map_y / total_pixel_width) * total_size_nodes)
        col = int((map_x / total_pixel_width) * total_size_nodes)

        logging.debug(f"LocationEditorView: Рассчитаны глобальные 'нодовые' координаты ({row}, {col}).")

        # Проверяем клик по границам карты
        if 0 <= row < total_size_nodes and 0 <= col < total_size_nodes:
            self.service.on_node_selected(row, col)
        else:
            logging.warning(
                f"LocationEditorView: Клик ({row}, {col}) вне границ карты ({total_size_nodes}x{total_size_nodes}).")

    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    def _on_mouse_wheel(self, event):
        """Обрабатывает прокрутку колесика мыши для изменения масштаба."""
        if event.delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level /= 1.1
        self.zoom_level = max(0.1, min(self.zoom_level, 5.0))
        self.draw_canvas()

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
        if not self.location_canvas or not self.location_data: return
        logging.info("LocationEditorView: Запуск полной перерисовки холста...")
        self.location_canvas.delete("all")

        root_module = self.location_data.get("root_module", {})
        total_pixel_width = self._get_total_pixel_size(root_module.get('level', 0))

        canvas_width = self.location_canvas.winfo_width()
        canvas_height = self.location_canvas.winfo_height()

        start_x = (canvas_width - total_pixel_width) / 2 + self.pan_offset_x
        start_y = (canvas_height - total_pixel_width) / 2 + self.pan_offset_y

        self._recursive_draw(root_module, start_x, start_y, total_pixel_width)
        logging.info("LocationEditorView: Перерисовка холста завершена.")

    def _get_total_pixel_size(self, level: int) -> float:
        """Рекурсивно вычисляет полный размер уровня в пикселях с учетом отступов."""
        node_size = self.base_node_size * self.zoom_level
        if level < 0:
            return 0
        if level == 0:
            # Базовый модуль 3x3 блока = 9x9 нодов
            return 9 * node_size

        child_size = self._get_total_pixel_size(level - 1)
        return 3 * child_size + 2 * self.MODULE_SPACING_PX

    def _recursive_draw(self, current_item: Dict, top_x: float, top_y: float, width: float):
        """
        Рекурсивно отрисовывает 'матрешку', оперируя пиксельными координатами.
        """
        if not current_item:
            return

        if 'level' not in current_item:
            if 'template_key' in current_item and 'nodes_structure' not in current_item:
                full_block_data = self.app.repos.block.get_by_key(current_item['template_key'])
                if full_block_data:
                    self._draw_block(full_block_data, top_x, top_y, width)
            else:
                self._draw_block(current_item, top_x, top_y, width)
            return

        level = current_item.get('level', 0)
        structure = current_item.get("structure", [])
        blocks_data = current_item.get("blocks_data", {})

        spacing = self.MODULE_SPACING_PX if level > 0 else 0

        child_width = (width - 2 * spacing) / 3.0

        for row_idx, row_content in enumerate(structure):
            for col_idx, item_key in enumerate(row_content):
                child_item = blocks_data.get(item_key)
                if not child_item:
                    continue

                child_top_x = top_x + col_idx * (child_width + spacing)
                child_top_y = top_y + row_idx * (child_width + spacing)

                self._recursive_draw(child_item, child_top_x, child_top_y, child_width)

    def _draw_block(self, block_data: Dict, top_x: float, top_y: float, width: float):
        """Отрисовывает блок в заданной пиксельной области."""

        node_size = width / 3.0
        if node_size < 1: return

        nodes_structure = block_data.get("nodes_structure", [])
        nodes_data = block_data.get("nodes_data", {})

        for node_row, node_cols in enumerate(nodes_structure):
            for node_col, node_key in enumerate(node_cols):
                node = nodes_data.get(str(node_key), {})
                template_key = node.get("template_key", "void")
                node_template = self.node_templates.get(template_key, {})
                fill_color = node_template.get("color", ERROR_COLOR)

                x1 = top_x + node_col * node_size
                y1 = top_y + node_row * node_size
                x2 = x1 + node_size
                y2 = y1 + node_size

                self.location_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=BG_CANVAS)

    def set_form_data(self, data: Dict[str, Any]):
        self.location_data = data
        self.draw_canvas()

    def get_form_data(self) -> Dict[str, Any]:
        return self.location_data or {}

    def clear_form(self) -> None:
        self.location_data = None
        self.draw_canvas()

    def bind_canvas_click(self, command: Callable[[Any], None]):
        pass

    def bind_expand_command(self, command: Callable[[], None]):
        """Привязывает команду к кнопке 'Увеличить масштаб'."""
        if self.controls and self.controls.expand_button:
            self.controls.expand_button.config(command=command)