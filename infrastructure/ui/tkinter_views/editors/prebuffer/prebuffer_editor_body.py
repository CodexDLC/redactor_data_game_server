# File: infrastructure/ui/tkinter_views/editors/prebuffer/prebuffer_editor_body.py
import tkinter as tk
from typing import Any, Callable, Dict, Optional
import logging

from interfaces.ui.i_prebuffer_editor_view import IPrebufferEditorView
from ..base_editor_body import BaseEditorBody
from .prebuffer_actions_panel import PrebufferActionsPanel
from .prebuffer_properties_panel import PrebufferPropertiesPanel
from ...styles import *
from ...mixins.canvas_zoom_pan_mixin import CanvasZoomPanMixin
from ...widgets.code_preview_window import CodePreviewWindow


class PrebufferEditorBody(BaseEditorBody, IPrebufferEditorView, CanvasZoomPanMixin):
    def __init__(self, master, app: Any):
        BaseEditorBody.__init__(self, master, app)
        CanvasZoomPanMixin.__init__(self, self.canvas)
        self.prebuffer_data: Dict[str, Any] = self._get_initial_data()
        self.node_templates: Dict[str, Any] = self.app.repos.node.get_all()
        self._code_preview_window: Optional[CodePreviewWindow] = None

        self.properties_panel = PrebufferPropertiesPanel(self.properties_panel, self.app)
        self.properties_panel.pack(fill=tk.BOTH, expand=True)

        self.actions_panel = PrebufferActionsPanel(self.actions_panel, self.app)
        self.actions_panel.pack(fill=tk.BOTH, expand=True)

        self._create_context_menu_for_canvas()

        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Configure>", lambda e: self.draw_canvas())

    def set_service(self, service: Any):
        self.service = service
        self.properties_panel.set_service(service)

        if self.actions_panel:
            self.actions_panel.save_button.config(command=self.service.save_prebuffer_template)
            self.actions_panel.delete_button.config(command=self.service.delete_prebuffer_template)
            self.actions_panel.new_button.config(command=self.service.new_prebuffer)
            self.actions_panel.show_code_button.config(command=self._on_show_code)
            # NEW: Bind the new "Save Object" button
            self.actions_panel.save_object_button.config(command=self.service.save_prebuffer_object)

        self.bind_canvas_click(self.service.on_canvas_click)

    def _on_show_code(self):
        template_data = {"prebuffer_template": self.get_form_data()}
        object_data = self.service.materialize_and_show_object(self.get_form_data(), "Код готового объекта")
        self.show_code_preview(template_data, object_data, "Код данных пре-буфера")

    def bind_save_command(self, command: Callable[[], None]) -> None:
        if self.actions_panel and hasattr(self.actions_panel, 'save_button'):
            self.actions_panel.save_button.config(command=command)

    def bind_delete_command(self, command: Callable[[], None]) -> None:
        if self.actions_panel and hasattr(self.actions_panel, 'delete_button'):
            self.actions_panel.delete_button.config(command=command)

    def bind_new_command(self, command: Callable[[], None]) -> None:
        if self.actions_panel and hasattr(self.actions_panel, 'new_button'):
            self.actions_panel.new_button.config(command=command)

    def bind_canvas_click(self, command: Callable[[int, int, int, int], None]):
        self.canvas.bind("<Button-1>", lambda event: command(
            int((event.y - self._get_canvas_offset('y')) / self._get_block_size()),
            int((event.x - self._get_canvas_offset('x')) / self._get_block_size()),
            int(((event.y - self._get_canvas_offset('y')) % self._get_block_size()) / self._get_tile_size()),
            int(((event.x - self._get_canvas_offset('x')) % self._get_block_size()) / self._get_tile_size())
        ))

    def _get_canvas_offset(self, axis: str) -> int:
        canvas_dim = self.canvas.winfo_width() if axis == 'x' else self.canvas.winfo_height()
        grid_size = self._get_grid_size()
        offset = self.pan_offset_x if axis == 'x' else self.pan_offset_y
        return (canvas_dim - grid_size) // 2 + offset

    def _get_grid_size(self) -> float:
        return min(self.canvas.winfo_width(), self.canvas.winfo_height()) * self.zoom_level

    def _get_block_size(self) -> float:
        return self._get_grid_size() / 3

    def _get_tile_size(self) -> float:
        return self._get_block_size() / 3

    def _get_initial_data(self) -> Dict[str, Any]:
        return {
            'prebuffer_key': 'new_prebuffer',
            'display_name': 'Новый Пре-буфер',
            'tags': [],
            'blocks_structure': [[None for _ in range(3)] for _ in range(3)],
        }

    def set_form_data(self, data: Dict[str, Any]):
        self.prebuffer_data = data
        if self.properties_panel:
            self.properties_panel.set_data(data)
        self.draw_canvas()

    def get_form_data(self) -> Dict[str, Any]:
        if not self.properties_panel:
            return self.prebuffer_data

        metadata = self.properties_panel.get_data()

        self.prebuffer_data.update(metadata)
        return self.prebuffer_data

    def _on_canvas_click(self, event):
        pass

    def draw_canvas(self):
        if not self.canvas: return
        self.canvas.delete("all")

        grid_size = self._get_grid_size()
        block_size_px = self._get_block_size()
        tile_size_px = self._get_tile_size()

        if block_size_px <= 1: return

        x_offset = self._get_canvas_offset('x')
        y_offset = self._get_canvas_offset('y')

        for block_row in range(3):
            for block_col in range(3):
                block_x1 = x_offset + block_col * block_size_px
                block_y1 = y_offset + block_row * block_size_px

                block_key = self.prebuffer_data['blocks_structure'][block_row][block_col]

                if block_key is None:
                    self.canvas.create_rectangle(block_x1, block_y1,
                                                 block_x1 + block_size_px, block_y1 + block_size_px,
                                                 fill=BG_CANVAS, outline=BG_PRIMARY)
                    continue

                block_data = self.app.repos.block.get_by_key(block_key)
                if not block_data:
                    self.canvas.create_rectangle(block_x1, block_y1,
                                                 block_x1 + block_size_px, block_y1 + block_size_px,
                                                 fill=ERROR_COLOR, outline=BG_PRIMARY)
                    continue

                nodes_structure = block_data.get('nodes_structure', [[None] * 3 for _ in range(3)])
                nodes_data = block_data.get('nodes_data', {})

                for node_row in range(3):
                    for node_col in range(3):
                        node_x1 = block_x1 + node_col * tile_size_px
                        node_y1 = block_y1 + node_row * tile_size_px
                        node_x2 = node_x1 + tile_size_px
                        node_y2 = node_y1 + tile_size_px

                        node_id = nodes_structure[node_row][node_col]
                        fill_color = BG_SECONDARY
                        if node_id is not None:
                            node_details = nodes_data.get(str(node_id))
                            if node_details:
                                template_key = node_details.get('template_key', 'void')
                                node_template = self.app.repos.node.get_by_key(template_key)
                                if node_template:
                                    fill_color = node_template.get('color', BG_SECONDARY)
                                else:
                                    fill_color = ERROR_COLOR
                            else:
                                fill_color = BG_CANVAS

                        self.canvas.create_rectangle(node_x1, node_y1, node_x2, node_y2,
                                                     fill=fill_color, outline=BG_PRIMARY)

        for r in range(4):
            y = y_offset + r * block_size_px
            self.canvas.create_line(x_offset, y, x_offset + grid_size, y, fill=FG_TEXT, width=2)

        for c in range(4):
            x = x_offset + c * block_size_px
            self.canvas.create_line(x, y_offset, x, y_offset + grid_size, fill=FG_TEXT, width=2)

    def show_code_preview(self, template_data: Any, object_data: Any, title: str):
        if self._code_preview_window and self._code_preview_window.winfo_exists():
            self._code_preview_window.update_content(template_data)
            self._code_preview_window.lift()
        else:
            self._code_preview_window = CodePreviewWindow(self.master, template_data, object_data, title)