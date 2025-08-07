# File: infrastructure/persistence/json_prebuffer_object_repository.py
import json
import os
import shutil
from typing import Dict, Any, Optional, List

from interfaces.persistence.i_prebuffer_object_repository import IPrebufferObjectRepository


class JsonPrebufferObjectRepository(IPrebufferObjectRepository):
    """
    Репозиторий для готовых объектов пре-буферов.
    Каждый объект хранится в отдельной папке.
    """
    _BASE_DIR = "data/prebuffers/"
    _OBJECT_FILE = "object.json"
    _NODES_FILE = "nodes.json"

    def _get_object_path(self, object_key: str) -> str:
        """Возвращает полный путь к папке объекта."""
        return os.path.join(self._BASE_DIR, object_key)

    def get_all_object_keys(self) -> List[str]:
        """Возвращает список ключей всех доступных объектов."""
        if not os.path.exists(self._BASE_DIR):
            return []
        return [name for name in os.listdir(self._BASE_DIR)
                if os.path.isdir(os.path.join(self._BASE_DIR, name))]

    def load_object(self, object_key: str) -> Optional[Dict[str, Any]]:
        """
        Загружает данные объекта из его папки по ключу.
        """
        object_path = self._get_object_path(object_key)
        object_file_path = os.path.join(object_path, self._OBJECT_FILE)
        nodes_file_path = os.path.join(object_path, self._NODES_FILE)

        if not os.path.exists(object_file_path) or not os.path.exists(nodes_file_path):
            return None

        try:
            with open(object_file_path, 'r', encoding='utf-8') as f:
                object_data = json.load(f)
            with open(nodes_file_path, 'r', encoding='utf-8') as f:
                nodes_data = json.load(f)

            # Объединяем данные в одну структуру для удобства
            object_data['nodes_data'] = nodes_data
            return object_data
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_object(self, object_key: str, data: Dict[str, Any]) -> None:
        """
        Сохраняет данные объекта в его папку, разделяя на два файла.
        """
        object_path = self._get_object_path(object_key)
        os.makedirs(object_path, exist_ok=True)

        # Разделяем данные
        nodes_data = data.pop('nodes_data', {})
        object_data = data

        # Сохраняем object.json
        object_file_path = os.path.join(object_path, self._OBJECT_FILE)
        with open(object_file_path, 'w', encoding='utf-8') as f:
            json.dump(object_data, f, indent=4, ensure_ascii=False)

        # Сохраняем nodes.json
        nodes_file_path = os.path.join(object_path, self._NODES_FILE)
        with open(nodes_file_path, 'w', encoding='utf-8') as f:
            json.dump(nodes_data, f, indent=4, ensure_ascii=False)

    def delete_object(self, object_key: str) -> None:
        """
        Удаляет папку объекта и все ее содержимое.
        """
        object_path = self._get_object_path(object_key)
        if os.path.exists(object_path):
            shutil.rmtree(object_path)