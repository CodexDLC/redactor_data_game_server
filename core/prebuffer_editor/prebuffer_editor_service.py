# File: core/prebuffer_editor/prebuffer_editor_service.py
import logging
import json
import uuid
from typing import Any, Dict, Optional

from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.persistence.i_node_repository import INodeRepository
from interfaces.ui.i_prebuffer_editor_view import IPrebufferEditorView
from interfaces.persistence.i_prebuffer_object_repository import IPrebufferObjectRepository
from interfaces.persistence.i_prebuffer_template_repository import IPrebufferTemplateRepository
from infrastructure.ui.tkinter_views.widgets.save_brush_dialog import SaveBrushDialog

from .prebuffer_editor_helpers import materialize_prebuffer, calculate_all_exits


class PrebufferEditorService:
    def __init__(self, view: IPrebufferEditorView, block_repo: IBlockRepository,
                 node_repo: INodeRepository, app: Any,
                 prebuffer_template_repo: IPrebufferTemplateRepository,
                 prebuffer_object_repo: IPrebufferObjectRepository):
        self.view = view
        self.block_repo = block_repo
        self.node_repo = node_repo
        self.app = app
        self.prebuffer_template_repo = prebuffer_template_repo
        self.prebuffer_object_repo = prebuffer_object_repo
        self.current_prebuffer_key: Optional[str] = None

        self.view.bind_save_command(self.save_prebuffer_template)
        self.view.bind_delete_command(self.delete_prebuffer_template)
        self.view.bind_new_command(self.new_prebuffer)
        self.view.bind_canvas_click(self.on_canvas_click)

        logging.info("PrebufferEditorService: Сервис инициализирован.")

    def on_canvas_click(self, block_row: int, block_col: int, node_row: int, node_col: int) -> None:
        active_brush_info = self.app.get_active_brush()
        if not active_brush_info or active_brush_info[0] != "block":
            logging.info("PrebufferEditorService: Клик без активной кисти-блока. Действие проигнорировано.")
            return
        brush_block = active_brush_info[1]
        prebuffer_data = self.view.get_form_data()
        prebuffer_data['blocks_structure'][block_row][block_col] = brush_block['block_key']
        self.view.set_form_data(prebuffer_data)
        self.app.set_status_message(f"Блок '{brush_block['block_key']}' размещен в [{block_row},{block_col}].")

    def save_prebuffer_template(self) -> None:
        logging.info("PrebufferEditorService: Запуск сохранения шаблона.")
        data = self.view.get_form_data()
        prebuffer_key = data.get('prebuffer_key')
        if not prebuffer_key or prebuffer_key == 'new_prebuffer':
            prebuffer_key = f"prebuffer_{uuid.uuid4().hex[:6]}"
            data['prebuffer_key'] = prebuffer_key
            data['display_name'] = data['display_name'] if data['display_name'] != 'Новый Пре-буфер' else prebuffer_key

        self.app.repos.tag.add_tags_to_category('prebuffer_tags', data.get('tags', []))
        final_data_to_save = {"prebuffer_template": data}
        self.prebuffer_template_repo.upsert(prebuffer_key, final_data_to_save)
        self.current_prebuffer_key = prebuffer_key
        self.app.set_status_message(f"Шаблон '{prebuffer_key}' успешно сохранен автоматически.")
        logging.info(f"PrebufferEditorService: Шаблон '{prebuffer_key}' успешно сохранен автоматически.")
        self.view.set_form_data(data)

    def save_prebuffer_object(self) -> None:
        logging.info("PrebufferEditorService: Запуск сохранения объекта.")
        prebuffer_template_data = self.view.get_form_data()

        prebuffer_id = prebuffer_template_data.get('prebuffer_key')
        if not prebuffer_id:
            self.app.set_status_message("Ошибка: Сначала сохраните шаблон.", is_error=True)
            return

        materialized_data = materialize_prebuffer(
            prebuffer_template_data['blocks_structure'],
            self.block_repo,
            self.node_repo
        )

        all_exits = calculate_all_exits(
            materialized_data['nodes_structure'],
            materialized_data['nodes_data']
        )

        for node_id, exits_data in all_exits.items():
            if node_id in materialized_data['nodes_data']:
                materialized_data['nodes_data'][node_id]['exits'] = exits_data

        final_object_data = {
            "prebuffer_id": prebuffer_id,
            "display_name": prebuffer_template_data.get('display_name'),
            "tags": prebuffer_template_data.get('tags', []),
            "nodes_structure": materialized_data['nodes_structure'],
            "nodes_data": materialized_data['nodes_data']
        }

        self.prebuffer_object_repo.save_object(prebuffer_id, final_object_data)

        self.app.set_status_message(f"Объект '{prebuffer_id}' успешно сохранен.")
        logging.info(f"PrebufferEditorService: Объект '{prebuffer_id}' успешно сохранен в репозиторий объектов.")

    def new_prebuffer(self) -> None:
        self.current_prebuffer_key = None
        new_prebuffer_data = {
            'prebuffer_key': 'new_prebuffer',
            'display_name': 'Новый Пре-буфер',
            'tags': [],
            'blocks_structure': [[None for _ in range(3)] for _ in range(3)],
        }
        self.view.set_form_data(new_prebuffer_data)
        self.app.set_status_message("Создан новый пустой пре-буфер.")

    def delete_prebuffer_template(self) -> None:
        logging.info("PrebufferEditorService: Заглушка для удаления шаблона пре-буфера.")
        self.app.set_status_message("Функция удаления шаблона пре-буфера пока не реализована.")

    def show_object_code_preview(self, prebuffer_data: Dict[str, Any], title: str) -> Dict[str, Any]:
        logging.info("PrebufferEditorService: Материализация данных для предпросмотра объекта.")

        blocks_structure = prebuffer_data.get('blocks_structure', [])

        materialized_data = materialize_prebuffer(blocks_structure, self.block_repo, self.node_repo)

        final_data = {
            "prebuffer_object": {
                "prebuffer_id": prebuffer_data.get('prebuffer_key', 'new_prebuffer'),
                "display_name": prebuffer_data.get('display_name', 'Новый Пре-буфер'),
                "tags": prebuffer_data.get('tags', []),
                **materialized_data
            }
        }

        return final_data