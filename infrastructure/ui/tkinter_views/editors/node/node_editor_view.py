# File: infrastructure/ui/tkinter_views/editors/node/node_editor_view.py
import tkinter as tk
from typing import Dict, Any, List, Callable

from interfaces.ui.i_node_editor_view import INodeEditorView
from .node_editor_controls import NodeEditorControls
from ...base_editor_view import BaseEditorView
from ...styles import *


class NodeEditorView(BaseEditorView, INodeEditorView):
    """
    Основной класс View для редактора нодов.
    Теперь принимает и передает список доступных тегов.
    """

    def __init__(self, master, app: Any, schema: Dict[str, Any], available_tags: List[str]): # <--- 1. ДОБАВЛЕН available_tags
        super().__init__(master, app)
        self.schema = schema
        self.available_tags = available_tags # <--- Сохраняем список тегов
        self._on_canvas_click = None
        self.preview_canvas = None
        self.controls = None

        self._setup_ui()
        self._set_initial_data()

    def _setup_ui(self):
        self.three_panel_layout()

        # <--- 2. ПЕРЕДАЕМ available_tags В CONTROLS
        self.controls = NodeEditorControls(
            self.right_frame,
            schema=self.schema,
            parent_view=self,
            available_tags=self.available_tags
        )
        self.controls.pack(fill=tk.BOTH, expand=True)

        self.preview_canvas = tk.Canvas(self.center_frame, bg=BG_CANVAS, highlightthickness=0)
        self.preview_canvas.pack(expand=True, anchor="center", padx=10, pady=5)
        self.preview_canvas.bind("<Button-1>", self._on_canvas_click_internal)

        self._create_context_menu_for_canvas(self.preview_canvas)
        self.bind_show_code_command(self._show_code_preview_window, "Код данных ноды")

    def _set_initial_data(self):
        """Устанавливает базовые значения при запуске редактора."""
        data = {
            "node_key": "new_node_key",
            "display_name": "Новая Нода",
            "tag": "",
            "color": "#ffffff",
            "type": "SOLID",
            "properties": {}
        }
        self.set_form_data(data)

    def _on_canvas_click_internal(self, event):
        if self._on_canvas_click:
            self._on_canvas_click(event)

    def get_form_data(self) -> Dict[str, Any]:
        """Собирает данные из всех полей, включая новый Combobox для тега."""
        node_key = self.controls.node_key_entry.get()
        display_name = self.controls.display_name_entry.get()
        rus_type = self.controls.type_combobox.get()
        eng_type = self.controls.TYPE_MAPPING.get(rus_type)
        tag = self.controls.tag_combobox.get() # <--- 3. ПОЛУЧАЕМ ДАННЫЕ ИЗ COMBOBOX

        properties = {}
        for key, (var, widget) in self.controls._property_widgets.items():
            if isinstance(var, tk.BooleanVar):
                properties[key] = var.get()
            elif isinstance(var, tk.StringVar):
                properties[key] = var.get()

        return {
            "node_key": node_key,
            "display_name": display_name,
            "tag": tag, # <--- Добавляем тег в словарь
            "color": self.controls.selected_color,
            "type": eng_type,
            "properties": properties
        }

    def set_form_data(self, node_data: Dict[str, Any]) -> None:
        """Заполняет все поля формы данными, включая тег."""
        self.clear_form()

        self.controls.node_key_entry.insert(0, node_data.get("node_key", ""))
        self.controls.display_name_entry.insert(0, node_data.get("display_name", ""))
        self.controls.tag_combobox.set(node_data.get("tag", "")) # <--- 4. УСТАНАВЛИВАЕМ ЗНАЧЕНИЕ ДЛЯ COMBOBOX

        self.controls.selected_color = node_data.get("color", "#ffffff")
        self.controls._update_color_button_visuals()

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
        """Очищает все поля формы."""
        self.controls.node_key_entry.delete(0, tk.END)
        self.controls.display_name_entry.delete(0, tk.END)
        self.controls.tag_combobox.set("") # <--- Очищаем Combobox
        self.controls.type_combobox.set("")
        self.controls.selected_color = "#ffffff"
        self.controls._update_color_button_visuals()
        self.preview_canvas.config(bg=self.controls.selected_color)
        self.controls._on_type_changed()

    def bind_canvas_click(self, command: Callable[[Any], None]) -> None:
        self._on_canvas_click = command

    # Методы ниже остаются без изменений
    def update_node_list(self, node_keys: List[str]) -> None: pass
    def bind_list_selection_command(self, command: Callable[[Any], None]) -> None: pass
    def get_selected_node_key(self) -> str | None: return None