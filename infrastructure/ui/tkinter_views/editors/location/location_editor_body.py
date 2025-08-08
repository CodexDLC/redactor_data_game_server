# File: infrastructure/ui/tkinter_views/editors/location/location_editor_body.py
import tkinter as tk
from typing import Any, Callable, Dict, Optional, Tuple
import logging

from interfaces.ui.i_location_editor_view import ILocationEditorView
from ..base_editor_body import BaseEditorBody
from .location_startup_menu import LocationStartupMenu
from .location_actions_panel import LocationActionsPanel
from .location_properties_panel import LocationPropertiesPanel
from ...styles import *


class LocationEditorBody(BaseEditorBody, ILocationEditorView):
    def __init__(self, master, app: Any):
        super().__init__(master, app)
        self.service: Optional[Any] = None
        self.location_data: Optional[Dict[str, Any]] = None
        self.start_menu: Optional[LocationStartupMenu] = None

        self.properties_panel = LocationPropertiesPanel(self.properties_panel, self.app)
        self.properties_panel.pack(fill=tk.BOTH, expand=True)

        self.actions_panel = LocationActionsPanel(self.actions_panel, self.app)
        self.actions_panel.pack(fill=tk.BOTH, expand=True)

    def set_service(self, service: Any):
        self.service = service
        self.start_menu = LocationStartupMenu(self.master, self.app, self.service.new_location)

        if self.actions_panel:
            self.actions_panel.save_button.config(command=self.service.save_location)
            self.actions_panel.delete_button.config(command=self.service.delete_location)
            self.actions_panel.new_button.config(command=self._show_start_menu)

    def _show_start_menu(self):
        if self.start_menu:
            self.start_menu.lift()

    def get_form_data(self) -> Dict[str, Any]:
        return self.location_data or {}

    def set_form_data(self, data: Dict[str, Any]):
        self.location_data = data
        self.draw_canvas()

    def clear_form(self) -> None:
        """
        ИЗМЕНЕНИЕ: Реализация метода clear_form, требуемого интерфейсом.
        """
        self.location_data = None
        # Возможно, здесь нужно обновить поля на панели свойств
        if self.properties_panel:
            self.properties_panel.set_data({})
        self.draw_canvas()

    def bind_save_command(self, command: Callable[[], None]) -> None:
        if self.actions_panel and self.actions_panel.save_button:
            self.actions_panel.save_button.config(command=command)

    def bind_delete_command(self, command: Callable[[], None]) -> None:
        if self.actions_panel and self.actions_panel.delete_button:
            self.actions_panel.delete_button.config(command=command)

    def bind_new_command(self, command: Callable[[], None]) -> None:
        if self.actions_panel and self.actions_panel.new_button:
            self.actions_panel.new_button.config(command=command)

    def bind_canvas_click(self, command: Callable[[Any], None]) -> None:
        pass

    def show_code_preview(self, data: Dict[str, Any], title: str) -> None:
        pass

    def draw_canvas(self):
        if not self.canvas: return
        self.canvas.delete("all")
        logging.info("LocationEditorBody: Отрисовка карты локации.")