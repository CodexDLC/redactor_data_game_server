# File: core/block_editor/block_editor_service.py
import logging
from typing import Any, Dict, Optional

from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.persistence.i_node_repository import INodeRepository
from interfaces.ui.i_block_editor_view import IBlockEditorView
from .block_editor_helpers import transform_nodes_data_for_saving, calculate_all_exits


class BlockEditorService:
    def __init__(self, view: IBlockEditorView, repository: IBlockRepository,
                 node_repo: INodeRepository, app: Any):
        self.view = view
        self.repository = repository
        self.app = app
        self.node_repo = node_repo
        self.current_block_key: Optional[str] = None

        self.view.bind_save_command(self.save_block)
        self.view.bind_delete_command(self.delete_block)
        self.view.bind_new_command(self.new_block)
        self.view.bind_canvas_click(self.on_canvas_click)

    def save_block(self) -> None:
        data = self.view.get_form_data()
        block_key = data.get('block_key')

        if not block_key:
            self.app.set_status_message("Ошибка: Имя ключа блока не может быть пустым.", is_error=True)
            return

        nodes_structure = data.get('nodes_structure', [])
        nodes_data = data.get('nodes_data', {})

        all_exits = calculate_all_exits(nodes_structure)

        transformed_nodes_data = transform_nodes_data_for_saving(nodes_data)

        block_data_to_save = {
            'display_name': data.get('display_name', ''),
            'tags': data.get('tags', []),
            'width': data.get('width', 3),
            'height': data.get('height', 3),
            'nodes_structure': nodes_structure,
            'nodes_data': transformed_nodes_data,
            'calculated_exits': all_exits
        }

        self.app.repos.tag.add_tags_to_category('block_tags', block_data_to_save.get('tags', []))

        self.repository.upsert(block_key, block_data_to_save)
        self.current_block_key = block_key
        self.app.set_status_message(f"Блок '{block_key}' успешно сохранен.")

    def on_canvas_click(self, row: int, col: int, node_id: int | None) -> None:
        active_brush_info = self.app.get_active_brush()

        if not active_brush_info or active_brush_info[0] != "node":
            logging.info("BlockEditorService: Клик без активной кисти-нода.")
            return

        brush_node = active_brush_info[1]
        block_data = self.view.get_form_data()

        width = block_data.get('width', 3)
        local_id = row * width + col

        local_id_str = str(local_id)

        block_data['nodes_data'][local_id_str] = {
            'template_key': brush_node['node_key']
        }

        nodes_structure = [list(r) for r in block_data['nodes_structure']]
        nodes_structure[row][col] = local_id_str
        block_data['nodes_structure'] = tuple(tuple(r) for r in nodes_structure)

        block_data = self.enrich_data_with_colors(
            block_data)  # --- ИСПРАВЛЕНО: Теперь сохраняем возвращаемое значение ---
        self.view.set_form_data(block_data)

        logging.info(
            f"BlockEditorService: Нод '{brush_node['node_key']}' размещен в [{row},{col}] с ID {local_id_str}.")

    # --- ИСПРАВЛЕНО: Возвращаем словарь ---
    def enrich_data_with_colors(self, block_data: dict) -> dict:
        """
        Публичный метод для обогащения данных блока цветами.
        """
        return self._enrich_block_data_with_colors(block_data)

    def _enrich_block_data_with_colors(self, block_data: dict) -> dict:
        for node_id, node_details in block_data.get('nodes_data', {}).items():
            if 'color' not in node_details:
                template_key = node_details.get('template_key')
                if template_key:
                    node_template = self.node_repo.get_by_key(template_key)
                    node_details['color'] = node_template.get('color', '#ff00ff') if node_template else '#ff00ff'
        return block_data

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