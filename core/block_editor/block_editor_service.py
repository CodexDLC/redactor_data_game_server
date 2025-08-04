# File: core/block_editor/block_editor_service.py
import logging
from typing import Any, Dict, Optional, List

from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.persistence.i_node_repository import INodeRepository
from interfaces.persistence.i_property_repository import IPropertyRepository
from interfaces.ui.i_block_editor_view import IBlockEditorView
from .block_exits_calculator import BlockExitsCalculator


class BlockEditorService:
    def __init__(self, view: IBlockEditorView, repository: IBlockRepository,
                 node_repo: INodeRepository, property_repo: IPropertyRepository,
                 node_schema: Dict[str, Any], app: Any):
        self.view = view
        self.repository = repository
        self.app = app
        self.node_repo = node_repo
        self.property_repo = property_repo
        self.node_schema = node_schema
        self.exits_calculator = BlockExitsCalculator()
        self.current_block_key: Optional[str] = None

        self.view.bind_save_command(self.save_block)
        self.view.bind_delete_command(self.delete_block)
        self.view.bind_new_command(self.new_block)
        self.view.bind_canvas_click(self.on_canvas_click)
        self.view.bind_request_node_properties(self.on_request_node_properties)

    def save_block(self) -> None:
        """Собирает данные, обогащает их выходами (exits) и сохраняет."""
        data_from_ui = self.view.get_form_data()
        block_key = data_from_ui.get('block_key')

        if not block_key:
            self.app.set_status_message("Ошибка: Имя блока не может быть пустым.", is_error=True)
            return

        nodes_structure = data_from_ui.get('nodes_structure', [])
        nodes_data = data_from_ui.get('nodes_data', {})

        # --- НАЧАЛО ИСПРАВЛЕННОЙ ЛОГИКИ ---
        # 1. Сначала рассчитываем актуальные выходы для ВСЕХ нодов
        all_exits = self.exits_calculator.calculate_all_exits(nodes_structure)

        # 2. Теперь проходим по всем нодам и ОБЪЕДИНЯЕМ их свойства
        for node_id, node_details in nodes_data.items():
            # Получаем свойства, которые пришли из UI (могли быть изменены)
            ui_properties = node_details.get('properties', {})

            # Получаем рассчитанные выходы для этого нода
            calculated_exits = all_exits.get(node_id, {})

            # Объединяем их: сохраняем и выходы, и измененные в UI свойства
            ui_properties['exits'] = calculated_exits
            node_details['properties'] = ui_properties
        # --- КОНЕЦ ИСПРАВЛЕННОЙ ЛОГИКИ ---

        transformed_nodes_data = self._transform_data_for_saving(nodes_data)
        block_data_to_save = {
            'display_name': data_from_ui.get('display_name', block_key),
            'nodes_structure': nodes_structure,
            'nodes_data': transformed_nodes_data
        }

        self.repository.upsert(block_key, block_data_to_save)
        self.current_block_key = block_key
        self.app.set_status_message(f"Блок '{block_key}' успешно сохранен.")

    def on_request_node_properties(self, node_id: str):
        block_data = self.view.get_form_data()
        properties_for_view = self._prepare_node_properties_for_view(node_id, block_data)
        self.view.display_node_properties(properties_for_view)

    def _prepare_node_properties_for_view(self, node_id: str, block_data: dict) -> dict:
        """
        Готовит данные для отображения в панели свойств со вкладками.
        """
        instance_data = block_data.get('nodes_data', {}).get(node_id, {})
        template_key = instance_data.get('template_key') or instance_data.get('node_key')
        if not template_key: return {}

        template_data = self.node_repo.get_by_key(template_key)
        if not template_data: return {}

        properties_for_ui = {
            "basic_properties": {},
            "feature_properties": {}
        }

        instance_properties = instance_data.get("properties", {})
        template_properties = template_data.get("properties", {})

        # --- 1. Заполняем "Основные" свойства ---
        # (Когда мы их добавим, логика будет здесь)
        # TODO: Добавить логику для material_type, movement_time, exits

        # --- 2. Заполняем "Фичи" (Триггеры, Секреты и т.д.) ---
        for prop_key, template_value in template_properties.items():
            if template_value is True:
                prop_schema = self._find_property_in_schema(prop_key)
                if not prop_schema: continue

                # --- НАЧАЛО ИСПРАВЛЕННОЙ ЛОГИКИ ---
                instance_value = instance_properties.get(prop_key)

                # Если у экземпляра уже есть сохраненные детальные настройки (в виде словаря), используем их.
                # В противном случае (если их нет, или там старое значение 'true'),
                # мы принудительно создаем их из значений по умолчанию.
                if isinstance(instance_value, dict):
                    values = instance_value
                else:
                    values = self._get_default_params_for_property(prop_key)
                # --- КОНЕЦ ИСПРАВЛЕННОЙ ЛОГИКИ ---

                feature_data = {
                    "label": prop_schema.get("label", prop_key),
                    "values": values
                }

                properties_for_ui["feature_properties"][prop_key] = feature_data

        return properties_for_ui

    def on_canvas_click(self, row: int, col: int, node_id: str | None) -> None:
        brush_node = self.app.get_active_brush_node()
        if brush_node:
            block_data = self.view.get_form_data()  # Получаем данные ПЕРЕД изменением
            self._handle_brush_click(row, col, brush_node, block_data)
        else:
            self._handle_selection_click(node_id)

    def _handle_brush_click(self, row: int, col: int, brush_node: dict, block_data: dict) -> None:
        block_key = block_data.get('block_key')
        if not block_key:
            self.app.set_status_message("Ошибка: Для рисования блок должен иметь ключ.", is_error=True)
            return

        node_id = f"{block_key}_{row}_{col}"

        # Меняем node_key на template_key для ясности
        block_data['nodes_data'][node_id] = {
            'template_key': brush_node['node_key'],
            'properties': brush_node.get('properties', {}).copy()
        }

        nodes_structure = [list(r) for r in block_data['nodes_structure']]
        nodes_structure[row][col] = node_id
        block_data['nodes_structure'] = tuple(tuple(r) for r in nodes_structure)

        # Обогащаем данные цветом для отрисовки
        enriched_block_data = self._enrich_block_data_with_colors(block_data)
        self.view.set_form_data(enriched_block_data)

    def _handle_selection_click(self, node_id: str | None) -> None:
        if node_id:
            self.on_request_node_properties(node_id)
        else:
            self.view.display_node_properties({})

    def _transform_data_for_saving(self, nodes_data: dict) -> dict:
        clean_data = {}
        for node_id, details in nodes_data.items():
            new_details = details.copy()
            new_details.pop('color', None)

            # Трансформируем properties
            clean_props = {}
            if 'properties' in new_details:
                for key, value in new_details['properties'].items():
                    if isinstance(value, dict):  # Сохраняем только фичи и выходы
                        clean_props[key] = value
            new_details['properties'] = clean_props
            clean_data[node_id] = new_details
        return clean_data

    def _find_property_in_schema(self, prop_key: str) -> Optional[Dict[str, Any]]:
        if prop_key in self.node_schema['common_properties']:
            return self.node_schema['common_properties'][prop_key]
        for type_specific_props in self.node_schema['type_specific_properties'].values():
            if prop_key in type_specific_props:
                return type_specific_props[prop_key]
        return None

    def _get_default_params_for_property(self, prop_key: str) -> dict:
        params_schema = self.property_repo.get_by_key(prop_key)
        defaults = {}
        if not params_schema: return defaults
        for key, details in params_schema.items():
            if "default" in details:
                defaults[key] = details["default"]
            elif details.get("type") == "dropdown":
                defaults[key] = details.get("options", [""])[0]
            else:
                defaults[key] = ""
        return defaults

    def new_block(self) -> None:
        self.current_block_key = None
        self.view.clear_form()

    def delete_block(self) -> None:
        if self.current_block_key:
            key_to_delete = self.current_block_key
            self.repository.delete(key_to_delete)
            self.app.set_status_message(f"Блок '{key_to_delete}' удален.")
            self.new_block()
        else:
            self.app.set_status_message("Ошибка: Не выбран блок для удаления.", is_error=True)

    def _enrich_block_data_with_colors(self, block_data: dict) -> dict:
        for node_id, node_details in block_data.get('nodes_data', {}).items():
            if 'color' not in node_details:
                template_key = node_details.get('template_key') or node_details.get('node_key')
                node_template = self.node_repo.get_by_key(template_key)
                node_details['color'] = node_template.get('color', '#ff00ff') if node_template else '#ff00ff'
        return block_data