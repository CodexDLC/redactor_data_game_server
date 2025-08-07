# File: core/location_editor/location_editor_service.py
import logging
from typing import Any, Dict, Optional

from interfaces.ui.i_location_editor_view import ILocationEditorView


class LocationEditorService:
    def __init__(self, view: ILocationEditorView, app: Any):
        self.view = view
        self.app = app
        self.current_location_key: Optional[str] = None
        logging.info("LocationEditorService: Сервис инициализирован.")

        # Привязываем команды к кнопкам, которые будут на панели
        self.view.bind_save_command(self.save_location)
        self.view.bind_delete_command(self.delete_location)
        self.view.bind_new_command(self.new_location)

    def save_location(self) -> None:
        logging.info("LocationEditorService: Заглушка для сохранения локации.")
        self.app.set_status_message("Сохранение локации пока не реализовано.", is_error=True)

    def delete_location(self) -> None:
        logging.info("LocationEditorService: Заглушка для удаления локации.")
        self.app.set_status_message("Удаление локации пока не реализовано.", is_error=True)

    def new_location(self, key: str, name: str, dimensions: tuple) -> None:
        logging.info("LocationEditorService: Заглушка для создания новой локации.")
        self.app.set_status_message("Создание новой локации пока не реализовано.", is_error=True)