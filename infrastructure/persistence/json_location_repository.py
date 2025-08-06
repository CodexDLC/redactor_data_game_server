# File: infrastructure/persistence/json_location_repository.py
import json
import os
import shutil
from typing import Dict, Any, Optional, List

from interfaces.persistence.i_location_repository import ILocationRepository


class JsonLocationRepository(ILocationRepository):
    """
    Конкретная реализация репозитория, работающая с файловой системой.
    Каждая локация хранится в отдельной папке с тремя файлами.
    """
    _BASE_DIR = "data/locations/"
    _BLOCKS_FILE = "blocks.json"
    _OBJECTS_FILE = "objects.json"
    _MAP_FILE = "map.json"

    def _get_location_path(self, location_key: str) -> str:
        """Возвращает полный путь к папке локации."""
        return os.path.join(self._BASE_DIR, location_key)

    def get_all_location_names(self) -> List[str]:
        """Возвращает список имен всех доступных локаций (имен папок)."""
        if not os.path.exists(self._BASE_DIR):
            return []
        return [name for name in os.listdir(self._BASE_DIR)
                if os.path.isdir(os.path.join(self._BASE_DIR, name))]

    def load_location(self, location_key: str) -> Optional[Dict[str, Any]]:
        """
        Загружает полную структуру локации из ее папки по ключу.
        """
        location_path = self._get_location_path(location_key)
        if not os.path.exists(location_path):
            return None

        location_data = {}
        try:
            with open(os.path.join(location_path, self._BLOCKS_FILE), 'r', encoding='utf-8') as f:
                location_data['blocks_data'] = json.load(f)
            with open(os.path.join(location_path, self._OBJECTS_FILE), 'r', encoding='utf-8') as f:
                location_data['objects_data'] = json.load(f)
            with open(os.path.join(location_path, self._MAP_FILE), 'r', encoding='utf-8') as f:
                location_data['map_data'] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

        return location_data

    def save_location(self, location_key: str, data: Dict[str, Any]) -> None:
        """
        Сохраняет полную структуру локации в ее папку.
        """
        location_path = self._get_location_path(location_key)
        os.makedirs(location_path, exist_ok=True)

        with open(os.path.join(location_path, self._BLOCKS_FILE), 'w', encoding='utf-8') as f:
            json.dump(data.get('blocks_data', {}), f, indent=4, ensure_ascii=False)
        with open(os.path.join(location_path, self._OBJECTS_FILE), 'w', encoding='utf-8') as f:
            json.dump(data.get('objects_data', {}), f, indent=4, ensure_ascii=False)
        with open(os.path.join(location_path, self._MAP_FILE), 'w', encoding='utf-8') as f:
            json.dump(data.get('map_data', {}), f, indent=4, ensure_ascii=False)

    def delete_location(self, location_key: str) -> None:
        """
        Удаляет папку локации и все ее содержимое.
        """
        location_path = self._get_location_path(location_key)
        if os.path.exists(location_path):
            shutil.rmtree(location_path)