# File: core/location_editor/location_editor_service.py
import logging
from typing import Any, Dict, Optional
import copy


class LocationEditorService:
    """
    Основной класс-сервис, управляющий всей логикой Редактора Локаций.
    """

    def __init__(self, view: Any, app: Any):
        self.view = view
        self.app = app
        self.current_location_data: Optional[Dict[str, Any]] = None

        self._bind_commands()
        self.new_location()

    def _bind_commands(self):
        """Привязывает методы сервиса к кнопкам в UI."""
        self.view.bind_save_command(self.save_location)
        self.view.bind_delete_command(self.delete_location)
        self.view.bind_new_command(self.new_location)

    def new_location(self):
        """Создает новую, пустую локацию для редактирования."""
        logging.info("Создание новой локации...")

        blocks_data = {}
        for block_idx in range(9):
            nodes_data = {}
            for node_idx in range(9):
                nodes_data[str(node_idx)] = {"template_key": "void"}

            blocks_data[str(block_idx)] = {
                "template_key": "void_block",
                "nodes_data": nodes_data,
                "nodes_structure": [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
            }

        root_module = {
            "level": 0,
            "structure": [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
            "blocks_data": blocks_data
        }

        self.current_location_data = {
            "location_id": "new_location",
            "root_module": root_module
        }

        self.view.clear_form()
        self.view.set_form_data(self.current_location_data)

    def save_location(self):
        """Сохраняет текущую локацию."""
        logging.info("Сохранение локации...")
        pass

    def delete_location(self):
        """Удаляет текущую локацию."""
        logging.info("Удаление локации...")
        pass

    def on_node_selected(self, global_row: int, global_col: int):
        """
        Обрабатывает выбор ноды на холсте.
        Если активна кисточка-блок, "рисует" им.
        Иначе - просто показывает ID выбранной ноды.
        """
        block_row = global_row // 3
        block_col = global_col // 3
        block_idx = block_row * 3 + block_col

        active_brush = self.app.get_active_brush()
        if active_brush and active_brush[0] == "block":
            brush_data = active_brush[1]
            logging.info(f"Применение кисточки-блока '{brush_data.get('block_key')}' на блок с индексом {block_idx}")

            new_block_instance = copy.deepcopy(brush_data)
            new_block_instance.pop('block_key', None)

            self.current_location_data["root_module"]["blocks_data"][str(block_idx)] = new_block_instance

            self.view.set_form_data(self.current_location_data)

        else:
            local_node_row = global_row % 3
            local_node_col = global_col % 3
            node_idx = local_node_row * 3 + local_node_col

            # --- ИСПРАВЛЕНО: Формируем правильную структуру данных для UI ---
            path_components = [
                ("Модуль", f"module_{self.current_location_data['root_module']['level']}"),
                ("Блок", f"block_{block_idx}"),
                ("Нода", f"node_{node_idx}")
            ]

            logging.info(f"Выбрана нода. Путь: {path_components}")
            self.view.controls.update_path_display(path_components)
