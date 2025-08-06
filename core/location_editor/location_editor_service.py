# File: core/location_editor/location_editor_service.py
import logging
from typing import Any, Dict, Optional


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
        # self.view.bind_canvas_click(self.on_canvas_click)

    def new_location(self):
        """Создает новую, пустую локацию для редактирования."""
        logging.info("Создание новой локации...")

        # Создаем стартовую иерархическую структуру: 1 модуль -> 9 блоков -> 81 нода

        # 1. Создаем 9 экземпляров блоков
        blocks_data = {}
        for block_idx in range(9):
            nodes_data = {}
            for node_idx in range(9):
                # Каждая нода по умолчанию ссылается на шаблон 'void'
                nodes_data[node_idx] = {"template_key": "void"}

            blocks_data[block_idx] = {
                "template_key": "void_block",  # Условно, блоки тоже могут иметь шаблон
                "nodes_data": nodes_data,
                "nodes_structure": [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
            }

        # 2. Создаем корневой модуль, который содержит эти 9 блоков
        root_module = {
            "level": 0,
            "structure": [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
            "blocks_data": blocks_data
        }

        # 3. Сохраняем полную структуру локации
        self.current_location_data = {
            "location_id": "new_location",
            "root_module": root_module
        }

        self.view.clear_form()
        # Передаем данные в View, чтобы он мог их отрисовать
        self.view.set_form_data(self.current_location_data)
        self.view.draw_canvas()

    def save_location(self):
        """Сохраняет текущую локацию."""
        logging.info("Сохранение локации...")
        # TODO: Реализовать логику сохранения
        pass

    def delete_location(self):
        """Удаляет текущую локацию."""
        logging.info("Удаление локации...")
        # TODO: Реализовать логику удаления
        pass

    def on_canvas_click(self, event: Any):
        """Обрабатывает клик по холсту."""
        logging.info(f"Клик по холсту в координатах: ({event.x}, {event.y})")
        # TODO: Реализовать логику обработки клика
        pass
