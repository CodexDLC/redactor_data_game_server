# File: infrastructure/ui/tkinter_views/editors/block/block_editor_controls.py
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, List

from ...base_editor_controls import BaseEditorControls
from ...styles import *
from ...widgets.code_preview_window import CodePreviewWindow
from ...widgets.context_menu import add_editing_menu
from ...widgets.widget_factory import create_widget_for_property


class BlockEditorControls(BaseEditorControls):
    """
    Новая панель управления для редактора блоков с трехзонной компоновкой:
    1. Свойства всего блока.
    2. Выбор нода для редактирования.
    3. Свойства выбранного нода (во вкладках).
    """

    def __init__(self, master, parent_view: Any):
        super().__init__(master, parent_view)
        self.current_block_data = {}
        self.selected_node_id = tk.StringVar()
        self._property_widgets: Dict[str, Any] = {}

    # ---------------------------------------------------------------------
    # --- UI Building ---
    # ---------------------------------------------------------------------

    def _build_ui(self):
        """Строит новую трехзонную компоновку панели."""
        # --- Зона 1: Свойства Блока ---
        self._build_block_properties_zone()

        # --- Зона 2: Выбор Нода ---
        self._build_node_selection_zone()

        # --- Зона 3: Свойства Выбранного Нода ---
        self._build_node_properties_zone()

        # --- Зона 4: Действия (из базового класса) ---
        super()._build_ui()

    def _build_block_properties_zone(self):
        """Создает UI для редактирования свойств всего блока."""
        frame = tk.LabelFrame(self, text="Свойства блока", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        tk.Label(frame, text="Ключ блока (block_key):", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.entry_block_key = tk.Entry(frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.entry_block_key.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_block_key)

        tk.Label(frame, text="Имя для UI:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.entry_display_name = tk.Entry(frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.entry_display_name.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_display_name)

        # TODO: Добавить поле для тегов блока
        # tk.Label(frame, text="Теги блока (через запятую):", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        # self.entry_block_tags = tk.Entry(frame, bg=BG_SECONDARY, fg=FG_TEXT)
        # self.entry_block_tags.pack(fill=tk.X, pady=(0, 5))

    def _build_node_selection_zone(self):
        """Создает UI для выбора нода, который нужно редактировать."""
        frame = tk.LabelFrame(self, text="Выбор нода для редактирования", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        self.node_selector_combo = ttk.Combobox(frame, textvariable=self.selected_node_id, state="readonly")
        self.node_selector_combo.pack(fill=tk.X)
        self.node_selector_combo.bind("<<ComboboxSelected>>", self._on_node_selected_from_combo)

    def _build_node_properties_zone(self):
        """Создает контейнер для вкладок со свойствами выбранного нода."""
        self.props_frame_container = tk.LabelFrame(self, text="Свойства нода", fg=FG_TEXT, bg=BG_PRIMARY, padx=5,
                                                   pady=5)
        self.props_frame_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        style = ttk.Style()
        style.configure("TNotebook.Tab", background=BG_SECONDARY, foreground=FG_TEXT)
        style.map("TNotebook.Tab", background=[("selected", BG_HIGHLIGHT)])

        self.props_notebook = ttk.Notebook(self.props_frame_container, style="TNotebook")
        self.props_notebook.pack(fill=tk.BOTH, expand=True)

    # ---------------------------------------------------------------------
    # --- Data Handling & UI Updates ---
    # ---------------------------------------------------------------------

    def set_block_data(self, block_data: Dict[str, Any]):
        """
        Основной метод для обновления всей панели.
        Заполняет свойства блока и список выбора нодов.
        """
        self.current_block_data = block_data

        # 1. Заполняем свойства блока
        self.entry_block_key.delete(0, tk.END)
        self.entry_block_key.insert(0, block_data.get('block_key', ''))
        self.entry_display_name.delete(0, tk.END)
        self.entry_display_name.insert(0, block_data.get('display_name', ''))

        # 2. Обновляем выпадающий список нодов
        nodes_data = block_data.get('nodes_data', {})
        # Формируем красивые имена для списка: "[x,y] - template_key"
        node_list = []
        nodes_structure = block_data.get('nodes_structure', [])
        for r, row in enumerate(nodes_structure):
            for c, node_id in enumerate(row):
                if node_id and node_id in nodes_data:
                    template_key = nodes_data[node_id].get('template_key', 'N/A')
                    node_list.append(f"[{r},{c}] {template_key} ({node_id})")

        self.node_selector_combo['values'] = node_list
        self._clear_node_properties_tabs()

    def _on_node_selected_from_combo(self, event=None):
        """Срабатывает при выборе нода из выпадающего списка."""
        selection = self.selected_node_id.get()
        # Извлекаем ID нода из строки, например " (new_block_key_0_0)" -> "new_block_key_0_0"
        node_id = selection.split('(')[-1][:-1]

        # Запрашиваем у View (который спросит у Service) данные для этого нода
        self.parent_view.request_properties_for_node(node_id)

    def display_node_properties(self, properties_data: Dict[str, Any]):
        """Отображает полученные от сервиса свойства нода во вкладках."""
        self._clear_node_properties_tabs()
        self._property_widgets.clear()

        # --- Вкладка 1: Основные (всегда есть) ---
        basic_tab = ttk.Frame(self.props_notebook)
        self.props_notebook.add(basic_tab, text="Основные")

        # Виджеты для базовых свойств (например, material_type, movement_time)
        if "basic_properties" in properties_data:
            self._property_widgets["basic_properties"] = {}
            for key, info in properties_data["basic_properties"].items():
                value = info.get("value")
                schema = info.get("schema")
                if not schema: continue

                frame, (var, widget) = create_widget_for_property(basic_tab, key, schema)
                var.set(value)
                frame.pack(fill=tk.X, pady=2, anchor="w", padx=2)
                self._property_widgets["basic_properties"][key] = (var, widget)

        # --- Вкладки 2, 3...: Динамические (Триггер, Секрет...) ---
        if "feature_properties" in properties_data:
            for feature_name, feature_info in properties_data["feature_properties"].items():
                feature_tab = ttk.Frame(self.props_notebook)
                self.props_notebook.add(feature_tab, text=feature_info.get("label", feature_name))

                # --- НАЧАЛО ИСПРАВЛЕННОГО КОДА ---
                prop_values = feature_info.get("values", {})
                param_details_schema = self.parent_view.app.property_repo.get_by_key(feature_name)
                if not param_details_schema: continue

                # Сохраняем виджеты под ключом фичи (например, "is_solid_trigger")
                self._property_widgets[feature_name] = {}

                for param_key, param_info in param_details_schema.items():
                    frame, (var, widget) = create_widget_for_property(feature_tab, param_key, param_info)
                    frame.pack(fill=tk.X, pady=2, anchor="w", padx=2)
                    if param_key in prop_values:
                        var.set(prop_values[param_key])
                    self._property_widgets[feature_name][param_key] = (var, widget)
                # --- КОНЕЦ ИСПРАВЛЕННОГО КОДА ---

    def _clear_node_properties_tabs(self):
        """Очищает все вкладки в Notebook."""
        for i in reversed(range(self.props_notebook.index("end"))):
            self.props_notebook.forget(i)

        # File: infrastructure/ui/tkinter_views/editors/block/block_editor_controls.py

        def get_properties_data(self) -> Dict[str, Any]:
            """Собирает текущие значения из всех виджетов со всех вкладок."""
            # Этот словарь будет содержать итоговые свойства для одного нода
            # Например: {'material_type': 'stone', 'is_solid_trigger': {'event_id': 'evt1', ...}}
            collected_properties = {}

            # 1. Собираем данные с вкладки "Основные"
            if "basic_properties" in self._property_widgets:
                for key, (var, widget) in self._property_widgets["basic_properties"].items():
                    collected_properties[key] = var.get()

            # 2. Собираем данные с динамических вкладок (Триггер, Секрет и т.д.)
            for feature_name, widget_group in self._property_widgets.items():
                if feature_name == "basic_properties":
                    continue  # Эту вкладку уже обработали

                # Для каждой фичи (например, 'is_solid_trigger') создаем свой вложенный словарь
                feature_values = {}
                for sub_key, (var, widget) in widget_group.items():
                    feature_values[sub_key] = var.get()

                # Добавляем в итоговый словарь
                collected_properties[feature_name] = feature_values

            return collected_properties