# File: infrastructure/ui/tkinter_views/editors/block/block_editor_controls.py
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, List, Tuple

from ...base_editor_controls import BaseEditorControls
from ...styles import *
from ...widgets.context_menu import add_editing_menu
from ...widgets.exits_editor import ExitsEditorWidget
from ...widgets.widget_factory import create_widget_for_property
from ...widgets.node_selector_widget import NodeSelectorWidget


class BlockEditorControls(BaseEditorControls):
    """
    Класс-контейнер, который собирает и управляет кастомными виджетами
    для редактирования свойств блока.
    """

    def __init__(self, master, parent_view: Any):
        # ИЗМЕНЕНО: Инициализируем атрибуты ПЕРЕД вызовом super()
        self.current_block_data = {}
        self.selected_node_id = None
        self.current_node_properties_data: Dict[str, Any] = {}
        self._active_widgets: Dict[str, Any] = {}
        self.basic_properties_listbox = None
        self.feature_properties_listbox = None
        self.basic_prop_map = {}
        self.feature_prop_map = {}
        self.node_selector = None
        self.active_property_editor = None

        super().__init__(master, parent_view)

    def _build_ui(self):
        """Строит компоновку из зон, включая наши новые виджеты."""
        self._build_block_properties_zone()

        self.node_selector = NodeSelectorWidget(self, on_selection_changed=self._on_node_selected)
        self.node_selector.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        self._build_node_properties_zone()
        super()._build_ui()

        # ДОБАВЛЕНО: Обновляем данные после того, как виджеты созданы
        self.set_block_data(self.current_block_data)

    def _build_block_properties_zone(self):
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

    def _build_node_properties_zone(self):
        self.props_frame_container = tk.LabelFrame(self, text="Свойства нода", fg=FG_TEXT, bg=BG_PRIMARY, padx=5,
                                                   pady=5)
        self.props_frame_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        basic_props_frame = tk.LabelFrame(self.props_frame_container, text="Базовые свойства", fg=FG_TEXT,
                                          bg=BG_PRIMARY)
        basic_props_frame.pack(fill=tk.X, pady=(0, 5))
        self.basic_properties_listbox = tk.Listbox(basic_props_frame, bg=BG_SECONDARY, fg=FG_TEXT, height=3)
        self.basic_properties_listbox.pack(fill=tk.X)
        self.basic_properties_listbox.bind("<<ListboxSelect>>", self._on_property_selected_from_list)

        feature_props_frame = tk.LabelFrame(self.props_frame_container, text="Особые свойства", fg=FG_TEXT,
                                            bg=BG_PRIMARY)
        feature_props_frame.pack(fill=tk.X, pady=(0, 5))
        self.feature_properties_listbox = tk.Listbox(feature_props_frame, bg=BG_SECONDARY, fg=FG_TEXT, height=3)
        self.feature_properties_listbox.pack(fill=tk.X)
        self.feature_properties_listbox.bind("<<ListboxSelect>>", self._on_property_selected_from_list)

        self.property_editor_frame = tk.Frame(self.props_frame_container, bg=BG_PRIMARY)
        self.property_editor_frame.pack(fill=tk.BOTH, expand=True)

    def get_properties_data(self) -> Dict[str, Any]:
        """
        ИЗМЕНЕНО: Собирает данные из текущего активного виджета-редактора.
        """
        updated_data = {}
        if isinstance(self.active_property_editor, ExitsEditorWidget):
            updated_data['exits'] = self.active_property_editor.get_exits_data()
        else:
            # Для динамически созданных виджетов собираем данные из переменных
            for key, (variable, _, _) in self._active_widgets.items():
                if hasattr(variable, 'get'):
                    updated_data[key] = variable.get()
        return updated_data

    def set_block_data(self, block_data: Dict[str, Any]):
        self.current_block_data = block_data
        self.entry_block_key.delete(0, tk.END)
        self.entry_block_key.insert(0, block_data.get('block_key', ''))
        self.entry_display_name.delete(0, tk.END)
        self.entry_display_name.insert(0, block_data.get('display_name', ''))

        nodes_data = block_data.get('nodes_data', {})
        node_list_for_selector = []
        nodes_structure = block_data.get('nodes_structure', [])
        for r, row in enumerate(nodes_structure):
            for c, node_id in enumerate(row):
                if node_id and node_id in nodes_data:
                    template_key = nodes_data[node_id].get('template_key', 'N/A')
                    node_list_for_selector.append(f"[{r},{c}] {template_key} ({node_id})")

        print(f"Формируемый список нодов для селектора: {node_list_for_selector}")

        if self.node_selector:
            self.node_selector.update_list(node_list_for_selector)

        self._clear_properties_list_and_editor()

    def _on_node_selected(self, node_id: str):
        self.selected_node_id = node_id
        self.parent_view.request_properties_for_node(node_id)

    def display_available_properties(self, properties_data: Dict[str, Any]):
        self._clear_properties_list_and_editor()
        self.current_node_properties_data = properties_data

        self.basic_prop_map = {}
        self.feature_prop_map = {}

        # ДОБАВЛЕНО: Проверяем, что listbox'ы существуют
        if self.basic_properties_listbox:
            if 'basic_properties' in properties_data:
                for prop_key, prop_details in properties_data['basic_properties'].items():
                    if isinstance(prop_details, dict) and 'label' in prop_details:
                        label = prop_details['label']
                        self.basic_properties_listbox.insert(tk.END, label)
                        self.basic_prop_map[label] = prop_key

        if self.feature_properties_listbox:
            if 'feature_properties' in properties_data:
                for prop_key, prop_details in properties_data['feature_properties'].items():
                    if isinstance(prop_details, dict) and 'label' in prop_details:
                        label = prop_details['label']
                        self.feature_properties_listbox.insert(tk.END, label)
                        self.feature_prop_map[label] = prop_key

    def _on_property_selected_from_list(self, event=None):
        selected_listbox = None
        prop_key = None
        prop_details = None

        if self.basic_properties_listbox.curselection():
            selected_listbox = self.basic_properties_listbox
            prop_map = self.basic_prop_map
            prop_group = self.current_node_properties_data.get('basic_properties', {})
        elif self.feature_properties_listbox.curselection():
            selected_listbox = self.feature_properties_listbox
            prop_map = self.feature_prop_map
            prop_group = self.current_node_properties_data.get('feature_properties', {})
        else:
            return

        selection_indices = selected_listbox.curselection()
        if not selection_indices: return

        selected_label = selected_listbox.get(selection_indices[0])
        prop_key = prop_map.get(selected_label)
        prop_details = prop_group.get(prop_key)

        if prop_key == 'exits':
            self.parent_view.request_editor_for_property(self.selected_node_id, prop_key)
        else:
            if prop_details:
                # ИЗМЕНЕНО: теперь мы динамически создаём виджет
                self._display_property_editor(prop_key, prop_details)

    def _display_property_editor(self, prop_key: str, prop_details: Dict[str, Any]):
        self._clear_property_editor()
        self._active_widgets = {}

        # Если это простой тип, используем widget_factory
        if 'values' in prop_details and isinstance(prop_details['values'], dict):
            # Если это сложный тип (как триггер с несколькими полями)
            for param_key, param_info in prop_details['values'].items():
                variable, label, widget = create_widget_for_property(self.property_editor_frame, param_key, param_info)
                label.pack(anchor="w", padx=5, pady=(5, 0))
                widget.pack(fill=tk.X, padx=5, pady=(0, 5))
                self._active_widgets[param_key] = (variable, label, widget)

                # Устанавливаем значение
                if param_key in prop_details['values'] and hasattr(variable, 'set'):
                    value_to_set = prop_details['values'][param_key]
                    if isinstance(value_to_set, list):  # Для типа 'range'
                        variable.set(f"{value_to_set[0]},{value_to_set[1]}")
                    else:
                        variable.set(value_to_set)

        else:  # Для простых boolean или string
            # Это может быть более сложная логика, пока заглушка
            label = tk.Label(self.property_editor_frame, text=f"Редактор для {prop_key}", fg=FG_TEXT, bg=BG_PRIMARY)
            label.pack()

    def display_property_editor(self, prop_key: str, editor_data: Dict[str, Any]):
        self._clear_property_editor()
        if prop_key == 'exits':
            self.active_property_editor = ExitsEditorWidget(
                self.property_editor_frame,
                on_update_request=lambda: self.parent_view.request_properties_for_node(self.selected_node_id)
            )
            self.active_property_editor.pack()
            self.active_property_editor.update_visuals(
                exits_data=editor_data.get('exits', {}),
                is_connector=editor_data.get('is_connector', False)
            )

    def _clear_properties_list_and_editor(self):
        if self.basic_properties_listbox:
            self.basic_properties_listbox.delete(0, tk.END)
        if self.feature_properties_listbox:
            self.feature_properties_listbox.delete(0, tk.END)
        self._clear_property_editor()

    def _clear_property_editor(self):
        if self.active_property_editor:
            self.active_property_editor.destroy()
            self.active_property_editor = None

        # ДОБАВЛЕНО: Очищаем динамически созданные виджеты
        for _, (variable, label, widget) in self._active_widgets.items():
            label.destroy()
            widget.destroy()
        self._active_widgets = {}