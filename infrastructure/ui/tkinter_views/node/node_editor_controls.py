import tkinter as tk
from tkinter import ttk, colorchooser
from typing import Dict, Any
import json

from .widget_factory import create_widget_for_property
from ..widgets.context_menu import add_right_click_menu  # <<< Импорт нашей новой функции


class NodeEditorControls(tk.Frame):
    """Панель управления справа со всеми виджетами."""
    TYPE_MAPPING = {
        "Проходимый": "WALKABLE",
        "Непроходимый": "SOLID"
    }

    def __init__(self, master, schema: Dict[str, Any], parent_view):
        super().__init__(master)
        self.schema = schema
        self.parent_view = parent_view
        self.config(bg="#333333")

        self.selected_color = "#ffffff"
        self._property_widgets: Dict[str, Any] = {}

        self.preview_window = None
        self.preview_text = None

        self._build_ui()

    def _build_ui(self):
        """Строит весь интерфейс панели."""
        # --- Зона 1: Основные Свойства ---
        main_props_frame = tk.LabelFrame(self, text="Основные свойства", fg="white", bg="#333333", padx=5, pady=5)
        main_props_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        tk.Label(main_props_frame, text="Ключ ноды (node_key):", fg="white", bg="#333333").pack(anchor="w")
        self.node_key_entry = tk.Entry(main_props_frame, bg="#444444", fg="white")
        self.node_key_entry.pack(fill=tk.X, pady=(0, 5))
        add_right_click_menu(self.node_key_entry)  # <<< ПРИМЕНЯЕМ МЕНЮ ПОСЛЕ СОЗДАНИЯ

        tk.Label(main_props_frame, text="Имя для UI:", fg="white", bg="#333333").pack(anchor="w")
        self.display_name_entry = tk.Entry(main_props_frame, bg="#444444", fg="white")
        self.display_name_entry.pack(fill=tk.X, pady=(0, 5))
        add_right_click_menu(self.display_name_entry)  # <<< ПРИМЕНЯЕМ МЕНЮ ПОСЛЕ СОЗДАНИЯ

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

        # --- Зона 3: Действия ---
        actions_frame = tk.LabelFrame(self, text="Действия", fg="white", bg="#333333", padx=5, pady=5)
        actions_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.BOTTOM)
        self.save_button = tk.Button(actions_frame, text="Сохранить", bg="#444444", fg="white")
        self.save_button.pack(fill=tk.X, pady=2)
        self.delete_button = tk.Button(actions_frame, text="Удалить", bg="#444444", fg="white")
        self.delete_button.pack(fill=tk.X, pady=2)
        self.new_button = tk.Button(actions_frame, text="Создать новый", bg="#444444", fg="white")
        self.new_button.pack(fill=tk.X, pady=2)
        self.show_code_button = tk.Button(actions_frame, text="Показать код", bg="#444444", fg="white",
                                          command=self._show_code_preview)
        self.show_code_button.pack(fill=tk.X, pady=2)

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
            self._update_preview_content()

    def _get_text_color_for_bg(self, bg_color):
        """Определяет, какой цвет текста (черный/белый) лучше для фона."""
        try:
            r, g, b = self.winfo_rgb(bg_color)
            # Формула для определения яркости
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            return "white" if brightness < 32768 else "black"
        except tk.TclError:
            return "white" # Возвращаем белый в случае ошибки

    # <<< ВОЗВРАЩАЕМ МЕТОДЫ ДЛЯ ПРЕДПРОСМОТРА КОДА
    def _update_preview_content(self):
        """Обновляет содержимое окна предпросмотра."""
        node_data = self.parent_view.get_form_data()
        formatted_json = json.dumps(node_data, indent=4, ensure_ascii=False)
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert(tk.END, formatted_json)
        self.preview_text.config(state=tk.DISABLED)

    def _create_preview_window(self):
        """Создает окно предпросмотра."""
        self.preview_window = tk.Toplevel(self)
        self.preview_window.title("Предпросмотр Кода Ноды")
        self.preview_window.geometry("400x500")
        self.preview_window.config(bg="#333333")
        self.preview_window.attributes("-topmost", True)
        self.preview_window.transient(self.winfo_toplevel())

        toolbar = tk.Frame(self.preview_window, bg="#333333")
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(toolbar, text="Обновить", command=self._update_preview_content, bg="#444444", fg="white").pack(
            side=tk.LEFT)

        self.preview_text = tk.Text(self.preview_window, bg="#222222", fg="white", wrap=tk.WORD, font=("Courier", 10))
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._update_preview_content()

    def _show_code_preview(self):
        """Переключает видимость окна предпросмотра."""
        if not self.preview_window or not self.preview_window.winfo_exists():
            self._create_preview_window()
        else:
            self.preview_window.destroy()
            self.preview_window = None