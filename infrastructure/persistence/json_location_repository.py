# File: infrastructure/persistence/json_location_repository.py (version 0.1)
import json
import os
from typing import Dict, Any


from interfaces.persistence.i_location_repository import ILocationRepository


# Пока используем IBlockRepository как шаблон. В будущем может понадобиться отдельный интерфейс.


class JsonLocationRepository(ILocationRepository):
    """
    Конкретная реализация репозитория комнат, работающая с JSON-файлом.
    """
    _FILE_PATH = "data/location.json"

    def __init__(self):
        self._rooms: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Загружает данные из файла в память."""
        try:
            if os.path.exists(self._FILE_PATH):
                with open(self._FILE_PATH, 'r', encoding='utf-8') as f:
                    self._rooms = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._rooms = {}

    def _save_data(self) -> None:
        """Сохраняет данные из памяти в файл."""
        os.makedirs(os.path.dirname(self._FILE_PATH), exist_ok=True)
        with open(self._FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self._rooms, f, indent=4, ensure_ascii=False)

    def get_all(self) -> Dict[str, Any]:
        """Возвращает копию всех комнат."""
        return self._rooms.copy()

    def upsert(self, room_key: str, room_data: Dict[str, Any]) -> None:
        """Обновляет или создает комнату."""
        self._rooms[room_key] = room_data
        self._save_data()

    def delete(self, room_key: str) -> None:
        """Удаляет комнату по ключу."""
        if room_key in self._rooms:
            del self._rooms[room_key]
            self._save_data()