# File: infrastructure/ui/tkinter_views/node_editor_view.py (version 1.6)
import tkinter as tk
from tkinter import ttk, colorchooser
from typing import Dict, Any, List, Callable
import json

from infrastructure.ui.tkinter_views.base_editor import BaseEditor
from interfaces.ui.i_node_editor_view import INodeEditorView
# Импортируем обе структуры из файла схемы
from .node_editor_controls import NodeEditorControls


class NodeEditorView(tk.Frame, INodeEditorView):
    """
    Основной класс View, теперь с двухпанельной компоновкой.
    """

    # --- ИЗМЕНЕНИЯ ЗДЕСЬ ---
    def __init__(self, master, app, schema: Dict[str, Any]):
        super().__init__(master)
        self.app = app
        self.schema = schema  # Сохраняем схему
        self.three_panel_layout()

    def three_panel_layout(self):
        self.main_paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, bg="#333333")
        self.main_paned_window.pack(fill=tk.BOTH, expand=True)

        self.center_frame = tk.Frame(self.main_paned_window, bg="#333333")
        self.main_paned_window.add(self.center_frame, stretch="always")

        self.right_frame = tk.Frame(self.main_paned_window, bg="#333333")
        self.main_paned_window.add(self.right_frame, minsize=300)

        # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
        # Добавляем недостающий аргумент parent_view=self
        self.controls = NodeEditorControls(self.right_frame, self.schema, parent_view=self)
        self.controls.pack(fill=tk.BOTH, expand=True)

        self.preview_canvas = tk.Canvas(self.center_frame, bg="#222222", highlightthickness=0)
        self.preview_canvas.pack(expand=True, anchor="center")

    def update_node_list(self, node_keys: List[str]) -> None:
        pass

    def get_form_data(self) -> Dict[str, Any]:
        node_key = self.controls.node_key_entry.get()
        display_name = self.controls.display_name_entry.get()
        rus_type = self.controls.type_combobox.get()
        eng_type = self.controls.TYPE_MAPPING.get(rus_type)

        properties = {}

        # Собираем данные из динамически созданных виджетов
        for key, (var, widget) in self.controls._property_widgets.items():
            if isinstance(var, tk.BooleanVar):
                properties[key] = var.get()
            elif isinstance(var, tk.StringVar):
                properties[key] = var.get()

        return {
            "node_key": node_key,
            "display_name": display_name,
            "is_walkable": (eng_type == "WALKABLE"),  # Определяем is_walkable из типа
            "color": self.controls.selected_color,
            "type": eng_type,
            "properties": properties
        }

    def set_form_data(self, node_data: Dict[str, Any]) -> None:
        self.clear_form()  # Сначала полностью очищаем форму

        # --- ИСПРАВЛЕНИЕ: ПЕРЕД ЗАПОЛНЕНИЕМ ОЧИЩАЕМ ПОЛЯ ВВОДА ---
        self.controls.node_key_entry.delete(0, tk.END)
        self.controls.display_name_entry.delete(0, tk.END)

        # Вставляем новые данные в теперь уже пустые поля
        self.controls.node_key_entry.insert(0, node_data.get("node_key", ""))
        self.controls.display_name_entry.insert(0, node_data.get("display_name", ""))

        self.controls.selected_color = node_data.get("color", "#ffffff")
        self.controls._update_color_button_visuals()
        self.preview_canvas.config(bg=self.controls.selected_color)

        eng_type = node_data.get("type")
        for rus, eng in self.controls.TYPE_MAPPING.items():
            if eng == eng_type:
                self.controls.type_combobox.set(rus)
                self.controls._on_type_changed()  # Перерисовываем свойства для типа
                break

        # Заполняем значения для свойств, если они есть
        properties = node_data.get("properties", {})
        for key, value in properties.items():
            widget_tuple = self.controls._property_widgets.get(key)
            if widget_tuple:
                variable, widget = widget_tuple
                if isinstance(variable, tk.BooleanVar):
                    variable.set(bool(value))
                elif isinstance(variable, tk.StringVar):
                    variable.set(str(value))

        # Обновляем окно с кодом, если оно открыто
        if self.controls.preview_window and self.controls.preview_window.winfo_exists():
            self.controls._update_preview_content()

        node_properties = node_data.get("node_properties", {})
        for key, value in node_properties.items():
            widget = self.controls._context_widgets.get(key)
            if widget:
                if isinstance(widget, tuple) and isinstance(widget[0], tk.BooleanVar):
                    widget[0].set(value)
                elif isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                    widget.insert(0, str(value))

        if self.controls.preview_window and self.controls.preview_window.winfo_exists() and self.controls.preview_window.winfo_viewable():
            self.controls._update_preview_content()

    def clear_form(self) -> None:
        self.controls.node_key_entry.delete(0, tk.END)
        self.controls.type_combobox.set("")
        self.controls.selected_color = "#ffffff"
        self.controls._update_color_button_visuals()
        self.preview_canvas.config(bg=self.controls.selected_color)
        self.controls._on_type_changed()
        if self.controls.preview_window and self.controls.preview_window.winfo_exists() and self.controls.preview_window.winfo_viewable():
            self.controls._update_preview_content()

    def get_selected_node_key(self) -> str | None:
        return None

    def bind_save_command(self, command: Callable[[], None]) -> None:
        self.controls.save_button.config(command=command)

    def bind_delete_command(self, command: Callable[[], None]) -> None:
        self.controls.delete_button.config(command=command)

    def bind_new_command(self, command: Callable[[], None]) -> None:
        self.controls.new_button.config(command=command)

    def bind_list_selection_command(self, command: Callable[[Any], None]) -> None:
        pass