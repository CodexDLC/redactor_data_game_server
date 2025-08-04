# File: core/block_editor/block_editor_service.py (version 0.8)
from interfaces.ui.i_block_editor_view import IBlockEditorView
from interfaces.persistence.i_block_repository import IBlockRepository
from typing import Any, Optional
import logging


class BlockEditorService:
    def __init__(self, view: IBlockEditorView, repository: IBlockRepository, app: Any):
        self.view = view
        self.repository = repository
        self.app = app
        self.current_block_key: Optional[str] = None

        self.view.bind_save_command(self.save_block)
        self.view.bind_delete_command(self.delete_block)
        self.view.bind_new_command(self.new_block)
        self.view.bind_canvas_click(self.on_canvas_click)

    def save_block(self) -> None:
        data = self.view.get_form_data()
        block_key = data.get('block_key')

        if not block_key:
            self.app.set_status_message("Ошибка: Имя блока не может быть пустым.", is_error=True)
            logging.error("Попытка сохранить блок без имени.")
            return

        block_data_to_save = {
            'block_key': block_key,
            'display_name': data.get('display_name', block_key),
            'nodes_structure': data.get('nodes_structure'),
            'nodes_data': data.get('nodes_data')
        }

        # TODO: Добавить логику генерации ребер (exits)
        logging.info("TODO: Генерация ребер")

        self.repository.upsert(block_key, block_data_to_save)
        self.current_block_key = block_key
        self.app.set_status_message(f"Блок '{block_key}' успешно сохранен.")
        logging.info(f"Блок '{block_key}' успешно сохранен.")

    def delete_block(self) -> None:
        if self.current_block_key:
            self.repository.delete(self.current_block_key)
            self.view.clear_form()
            self.current_block_key = None
            self.app.set_status_message(f"Блок '{self.current_block_key}' удален.")
            logging.info(f"Блок '{self.current_block_key}' удален.")
        else:
            self.app.set_status_message("Ошибка: Не выбран блок для удаления.", is_error=True)
            logging.error("Попытка удалить блок, когда ни один не выбран.")

    def new_block(self) -> None:
        self.current_block_key = None
        self.view.clear_form()
        self.app.set_status_message("Создан новый пустой блок.")
        logging.info("Создан новый пустой блок.")

    def on_canvas_click(self, row: int, col: int) -> None:
        """Обрабатывает клик по канвасу, "рисуя" активной кисточкой или выбирая нод."""
        brush_node = self.app.get_active_brush_node()
        block_data = self.view.get_form_data()
        block_key = block_data.get('block_key')

        if not block_key and brush_node:
            self.app.set_status_message("Ошибка: Для рисования блок должен иметь ключ.", is_error=True)
            logging.error("Попытка рисовать без ключа блока.")
            return

        if brush_node:
            node_key = brush_node.get('node_key')
            node_id = f"{block_key}_{row}_{col}"

            node_data_to_add = {
                'id': node_id,
                'node_key': node_key,
            }

            nodes_structure = list(list(r) for r in block_data['nodes_structure'])
            nodes_structure[row][col] = node_id

            nodes_data = block_data['nodes_data'].copy()
            nodes_data[node_id] = node_data_to_add

            block_data['nodes_structure'] = tuple(tuple(r) for r in nodes_structure)
            block_data['nodes_data'] = nodes_data

            self.view.set_form_data(block_data)
            self.app.set_status_message(f"Нод '{node_key}' размещен в [{row},{col}].")
            logging.info(f"Нод '{node_key}' размещен в [{row},{col}].")

        else:
            nodes_structure = block_data['nodes_structure']
            node_id = nodes_structure[row][col]
            if node_id:
                node_data = block_data['nodes_data'][node_id]
                node_key = node_data['node_key']
                self.app.set_status_message(f"Выбран нод с ключом: {node_key}")
                logging.info(f"Выбран нод с ключом: {node_key}")
                self.view.show_node_properties(node_id)
            else:
                self.app.set_status_message("Выбрана пустая ячейка.")
                logging.info("Выбрана пустая ячейка.")