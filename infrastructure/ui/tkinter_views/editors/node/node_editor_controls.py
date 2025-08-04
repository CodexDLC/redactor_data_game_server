import tkinter as tk
from tkinter import ttk, colorchooser
from typing import Dict, Any, Callable
import json

from ...widgets.widget_factory import create_widget_for_property
from ...widgets.context_menu import add_editing_menu  # <-- Заменено на новую функцию
from ...base_editor_controls import BaseEditorControls


class NodeEditorControls(BaseEditorControls):
    """Панель управления справа со всеми виджетами."""
    TYPE_MAPPING = {
        "Проходимый": "WALKABLE",
        "Непроходимый": "SOLID"
    }

    def __init__(self, master, schema: Dict[str, Any], parent_view):
        self.schema = schema
        self.selected_color = "#ffffff"
        self._property_widgets: Dict[str, Any] = {}
        super().__init__(master, parent_view)

    def _build_ui(self):
        """Строит весь интерфейс панели."""
        # --- Зона 1: Основные Свойства ---
        main_props_frame = tk.LabelFrame(self, text="Основные свойства", fg="white", bg="#333333", padx=5, pady=5)
        main_props_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        tk.Label(main_props_frame, text="Ключ ноды (node_key):", fg="white", bg="#333333").pack(anchor="w")
        self.node_key_entry = tk.Entry(main_props_frame, bg="#444444", fg="white")
        self.node_key_entry.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.node_key_entry)  # <-- Обновлено

        tk.Label(main_props_frame, text="Имя для UI:", fg="white", bg="#333333").pack(anchor="w")
        self.display_name_entry = tk.Entry(main_props_frame, bg="#444444", fg="white")
        self.display_name_entry.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.display_name_entry)  # <-- Обновлено

        tk.Label(main_props_frame, text="Цвет:", fg="white", bg="#333333").pack(anchor="w")
        self.color_button = tk.Button(main_props_frame, text="Выбрать цвет", command=self._select_color)
        self.color_button.pack(fill=tk.X, pady=(0, 5))
        self.color_button.config(bg=self.selected_color)

        tk.Label(main_props_frame, text="Базовый тип:", fg="white", bg="#333333").pack(anchor="w")
        self.type_combobox = ttk.Combobox(main_props_frame, state="readonly", values=list(self.TYPE_MAPPING.keys()))
        self.type_combobox.pack(fill=tk.X)
        self.type_combobox.bind("<<ComboboxSelected>>", self._on_type_changed)

        # --- Зона 2: Контекстные Свойства ---
        self.context_props_frame = tk.LabelFrame(self, text="Настраиваемые свойства", fg="white", bg="#333333", padx=5,
                                                 pady=5)
        self.context_props_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Вызываем родительский метод для создания общих кнопок
        super()._build_ui()

    def _on_type_changed(self, event=None):
        """Перерисовывает Зону 2 на основе выбранного типа."""
        for widget in self.context_props_frame.winfo_children():
            widget.destroy()
        self._property_widgets.clear()

        # 1. Создаем виджеты для ОБЩИХ свойств, используя self.schema
        common_props = self.schema.get("common_properties", {})
        for key, prop_info in common_props.items():
            frame, (var, widget) = create_widget_for_property(self.context_props_frame, key, prop_info)
            frame.pack(fill=tk.X, pady=2, anchor="w")
            self._property_widgets[key] = (var, widget)

        # 2. Создаем виджеты для СПЕЦИФИЧНЫХ свойств, используя self.schema
        selected_rus_type = self.type_combobox.get()
        selected_eng_type = self.TYPE_MAPPING.get(selected_rus_type)
        if selected_eng_type:
            specific_props = self.schema.get("type_specific_properties", {}).get(selected_eng_type, {})
            for key, prop_info in specific_props.items():
                frame, (var, widget) = create_widget_for_property(self.context_props_frame, key, prop_info)
                frame.pack(fill=tk.X, pady=2, anchor="w")
                self._property_widgets[key] = (var, widget)

    def _select_color(self):
        """Открывает диалог выбора цвета и обновляет UI."""
        # askcolor возвращает кортеж ((r, g, b), '#rrggbb') или (None, None)
        color_code = colorchooser.askcolor(title="Выберите цвет материала", initialcolor=self.selected_color)
        if color_code and color_code[1]:
            self.selected_color = color_code[1]
            self._update_color_button_visuals()

    def _update_color_button_visuals(self):
        """Обновляет цвет кнопки и большого превью в центре."""
        self.color_button.config(bg=self.selected_color, fg=self._get_text_color_for_bg(self.selected_color))
        # Обращаемся к preview_canvas в родительском View
        self.parent_view.preview_canvas.config(bg=self.selected_color)
        # Обновляем окно с кодом, если оно открыто
        if hasattr(self, 'preview_window') and self.preview_window and self.preview_window.winfo_exists():
            self.preview_window.update_content(self.parent_view.get_form_data())

    def _get_text_color_for_bg(self, bg_color):
        """Определяет, какой цвет текста (черный/белый) лучше для фона."""
        try:
            r, g, b = self.winfo_rgb(bg_color)
            # Формула для определения яркости
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            return "white" if brightness < 32768 else "black"
        except tk.TclError:
            return "white"  # Возвращаем белый в случае ошибки

    def bind_show_code_command(self, command: Callable[[Any], None]) -> None:
        self.show_code_button.config(command=lambda: self._show_code_preview_wrapper(command))

    def _show_code_preview_wrapper(self, command: Callable[[Any], None]):
        """Обертка для вызова единого окна предпросмотра."""
        data = self.parent_view.get_form_data()
        command(data, "Код данных ноды")