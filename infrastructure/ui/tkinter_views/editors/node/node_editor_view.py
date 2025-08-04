# File: infrastructure/ui/tkinter_views/editors/node/node_editor_view.py (version 2.4)
import tkinter as tk
from tkinter import ttk, colorchooser
from typing import Dict, Any, List, Callable
import json

from interfaces.ui.i_node_editor_view import INodeEditorView
from .node_editor_controls import NodeEditorControls
from ...base_editor_view import BaseEditorView


class NodeEditorView(BaseEditorView, INodeEditorView):
    """
    Основной класс View, теперь с двухпанельной компоновкой.
    """

    def __init__(self, master, app: Any, schema: Dict[str, Any]):
        super().__init__(master, app)
        self.schema = schema
        self._on_canvas_click = None
        self.preview_canvas = None
        self.controls = None
        self._setup_ui()
        self._set_initial_data()  # <-- Добавлен вызов для установки начальных данных

    def _setup_ui(self):
        self.three_panel_layout()

        self.controls = NodeEditorControls(self.right_frame, self.schema, parent_view=self)
        self.controls.pack(fill=tk.BOTH, expand=True)

        self.preview_canvas = tk.Canvas(self.center_frame, bg="#222222", highlightthickness=0)
        self.preview_canvas.pack(expand=True, anchor="center", padx=10, pady=5)
        self.preview_canvas.bind("<Button-1>", self._on_canvas_click_internal)

        self._create_context_menu_for_canvas(self.preview_canvas)
        self.bind_show_code_command(self._show_code_preview_window)

    def _set_initial_data(self):
        """Устанавливает базовые значения при запуске редактора."""
        data = {
            "node_key": "new_node_key",
            "display_name": "Новая Нода",
            "color": "#ffffff",
            "type": "SOLID",
            "properties": {}
        }
        self.set_form_data(data)

    def _on_canvas_click_internal(self, event):
        if self._on_canvas_click:
            self._on_canvas_click(event)

    def update_node_list(self, node_keys: List[str]) -> None:
        pass

    def get_form_data(self) -> Dict[str, Any]:
        node_key = self.controls.node_key_entry.get()
        display_name = self.controls.display_name_entry.get()
        rus_type = self.controls.type_combobox.get()
        eng_type = self.controls.TYPE_MAPPING.get(rus_type)

        properties = {}

        for key, (var, widget) in self.controls._property_widgets.items():
            if isinstance(var, tk.BooleanVar):
                properties[key] = var.get()
            elif isinstance(var, tk.StringVar):
                properties[key] = var.get()

        return {
            "node_key": node_key,
            "display_name": display_name,
            "is_walkable": (eng_type == "WALKABLE"),
            "color": self.controls.selected_color,
            "type": eng_type,
            "properties": properties
        }

    def set_form_data(self, node_data: Dict[str, Any]) -> None:
        self.clear_form()

        self.controls.node_key_entry.delete(0, tk.END)
        self.controls.display_name_entry.delete(0, tk.END)

        self.controls.node_key_entry.insert(0, node_data.get("node_key", ""))
        self.controls.display_name_entry.insert(0, node_data.get("display_name", ""))

        self.controls.selected_color = node_data.get("color", "#ffffff")
        self.controls._update_color_button_visuals()
        self.preview_canvas.config(bg=self.controls.selected_color)

        eng_type = node_data.get("type")
        for rus, eng in self.controls.TYPE_MAPPING.items():
            if eng == eng_type:
                self.controls.type_combobox.set(rus)
                self.controls._on_type_changed()
                break

        properties = node_data.get("properties", {})
        for key, value in properties.items():
            widget_tuple = self.controls._property_widgets.get(key)
            if widget_tuple:
                variable, widget = widget_tuple
                if isinstance(variable, tk.BooleanVar):
                    variable.set(bool(value))
                elif isinstance(variable, tk.StringVar):
                    variable.set(str(value))

    def clear_form(self) -> None:
        self.controls.node_key_entry.delete(0, tk.END)
        self.controls.type_combobox.set("")
        self.controls.selected_color = "#ffffff"
        self.controls._update_color_button_visuals()
        self.preview_canvas.config(bg=self.controls.selected_color)
        self.controls._on_type_changed()

    def bind_canvas_click(self, command: Callable[[Any], None]) -> None:
        self._on_canvas_click = command

    def bind_list_selection_command(self, command: Callable[[Any], None]) -> None:
        pass

    def get_selected_node_key(self) -> str | None:
        return None