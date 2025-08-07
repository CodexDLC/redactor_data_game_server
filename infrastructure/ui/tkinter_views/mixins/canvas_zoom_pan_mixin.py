# File: infrastructure/ui/tkinter_views/mixins/canvas_zoom_pan_mixin.py
import tkinter as tk
from typing import Any


class CanvasZoomPanMixin:
    """
    Миксин для добавления функционала масштабирования и панорамирования
    к виджету Canvas.
    """

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.zoom_level = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.pan_offset_x = 0
        self.pan_offset_y = 0

        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<ButtonPress-2>", self._on_pan_start)
        self.canvas.bind("<B2-Motion>", self._on_pan_move)

    def _on_mouse_wheel(self, event: Any):
        """Обрабатывает масштабирование колесиком мыши."""
        zoom_factor = 1.1 if event.delta > 0 else 1 / 1.1
        self.zoom_level *= zoom_factor
        self.draw_canvas()

    def _on_pan_start(self, event: Any):
        """Запоминает начальную позицию для панорамирования."""
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def _on_pan_move(self, event: Any):
        """Перемещает холст при зажатой кнопке."""
        delta_x = event.x - self.pan_start_x
        delta_y = event.y - self.pan_start_y
        self.pan_offset_x += delta_x
        self.pan_offset_y += delta_y
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.draw_canvas()

    def draw_canvas(self):
        """
        Метод должен быть реализован в классе, использующем этот миксин.
        Он будет отвечать за перерисовку всего содержимого холста с учетом
        текущего масштаба и смещения.
        """
        raise NotImplementedError("Метод draw_canvas должен быть переопределен.")