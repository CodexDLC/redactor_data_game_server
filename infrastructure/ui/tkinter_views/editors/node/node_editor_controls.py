# File: infrastructure/ui/tkinter_views/editors/node/node_editor_controls.py
import tkinter as tk
from tkinter import ttk, colorchooser
from typing import Dict, Any, Callable, List

from ...widgets.widget_factory import create_widget_for_property
from ...widgets.context_menu import add_editing_menu
from ...base_editor_controls import BaseEditorControls
from ...styles import * #! Импорт стилей уже был, теперь мы их используем


class NodeEditorControls(BaseEditorControls):
    """Панель управления для редактора нодов со всеми виджетами."""
    TYPE_MAPPING = {
        "Проходимый": "WALKABLE",
        "Непроходимый": "SOLID"
    }

    def __init__(self, master, schema: Dict[str, Any], parent_view, available_tags: List[str]):
        self.schema = schema
        self.available_tags = available_tags
        self.selected_color = "#ffffff"
        self._property_widgets: Dict[str, Any] = {}
        self.tag_combobox = None
        super().__init__(master, parent_view)

    def _build_ui(self):
        """Строит весь интерфейс панели, используя переменные стилей."""
        # --- Зона 1: Основные Свойства ---
        #! Используем переменные стилей BG_PRIMARY и FG_TEXT
        main_props_frame = tk.LabelFrame(self, text="Основные свойства", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        main_props_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        tk.Label(main_props_frame, text="Ключ ноды (node_key):", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        #! Используем BG_SECONDARY и FG_TEXT
        self.node_key_entry = tk.Entry(main_props_frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.node_key_entry.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.node_key_entry)

        tk.Label(main_props_frame, text="Имя для UI:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.display_name_entry = tk.Entry(main_props_frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.display_name_entry.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.display_name_entry)

        tk.Label(main_props_frame, text="Цвет:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.color_button = tk.Button(main_props_frame, text="Выбрать цвет", command=self._select_color,
                                      highlightthickness=0, bd=0) #! Убрали стандартные рамки
        self.color_button.pack(fill=tk.X, pady=(0, 5))
        self.color_button.config(bg=self.selected_color)

        tk.Label(main_props_frame, text="Тег:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.tag_combobox = ttk.Combobox(main_props_frame, values=self.available_tags)
        self.tag_combobox.pack(fill=tk.X, pady=(0, 5))

        tk.Label(main_props_frame, text="Базовый тип:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.type_combobox = ttk.Combobox(main_props_frame, state="readonly", values=list(self.TYPE_MAPPING.keys()))
        self.type_combobox.pack(fill=tk.X)
        self.type_combobox.bind("<<ComboboxSelected>>", self._on_type_changed)

        # --- Зона 2: Контекстные Свойства ---
        self.context_props_frame = tk.LabelFrame(self, text="Настраиваемые свойства", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        self.context_props_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        super()._build_ui()

    def _on_type_changed(self, event=None):
        """Перерисовывает Зону 2 на основе выбранного типа."""
        for widget in self.context_props_frame.winfo_children():
            widget.destroy()
        self._property_widgets.clear()

        # --- ИСПРАВЛЕНИЕ: Упрощенная логика ---
        def populate_properties(props):
            for key, prop_info in props.items():
                # Фабрика теперь возвращает готовую рамку
                frame, (var, widget) = create_widget_for_property(self.context_props_frame, key, prop_info)
                # Мы просто размещаем эту рамку целиком
                frame.pack(fill=tk.X, pady=2)
                self._property_widgets[key] = (var, widget)

        populate_properties(self.schema.get("common_properties", {}))

        selected_rus_type = self.type_combobox.get()
        selected_eng_type = self.TYPE_MAPPING.get(selected_rus_type)
        if selected_eng_type:
            specific_props = self.schema.get("type_specific_properties", {}).get(selected_eng_type, {})
            populate_properties(specific_props)

    def _select_color(self):
        """Открывает диалог выбора цвета и обновляет UI."""
        color_code = colorchooser.askcolor(title="Выберите цвет материала", initialcolor=self.selected_color)
        if color_code and color_code[1]:
            self.selected_color = color_code[1]
            self._update_color_button_visuals()

    def _update_color_button_visuals(self):
        """Обновляет цвет кнопки и большого превью в центре."""
        self.color_button.config(bg=self.selected_color, fg=self._get_text_color_for_bg(self.selected_color),
                                 activebackground=self.selected_color) #! Добавили цвет при нажатии
        self.parent_view.preview_canvas.config(bg=self.selected_color)
        if hasattr(self, 'preview_window') and self.preview_window and self.preview_window.winfo_exists():
            self.parent_view.update_code_preview(self.parent_view.get_form_data())

    def _get_text_color_for_bg(self, bg_color):
        """Определяет, какой цвет текста (черный/белый) лучше для фона."""
        try:
            r, g, b = self.winfo_rgb(bg_color)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            #! Используем FG_TEXT вместо "white"
            return FG_TEXT if brightness < 32768 else "black"
        except tk.TclError:
            return FG_TEXT