# File: infrastructure/persistence/json_node_repository.py (version 0.2)
import json
import os
from typing import Dict, Any

from interfaces.persistence.i_node_repository import INodeRepository


class JsonNodeRepository(INodeRepository):
    """
    Конкретная реализация репозитория нод, работающая с JSON-файлом.
    Путь к файлу теперь задан внутри класса.
    """
    _FILE_PATH = "data/nodes.json"

    def __init__(self):
        self._nodes: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Загружает данные из файла в память."""
        try:
            if os.path.exists(self._FILE_PATH):
                with open(self._FILE_PATH, 'r', encoding='utf-8') as f:
                    self._nodes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._nodes = {}

    def _save_data(self) -> None:
        """Сохраняет данные из памяти в файл."""
        os.makedirs(os.path.dirname(self._FILE_PATH), exist_ok=True)
        with open(self._FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self._nodes, f, indent=4, ensure_ascii=False)

    def get_all(self) -> Dict[str, Any]:
        """Возвращает копию всех нод."""
        return self._nodes.copy()

    def upsert(self, node_key: str, node_data: Dict[str, Any]) -> None:
        """Обновляет или создает ноду и сохраняет изменения."""
        self._nodes[node_key] = node_data
        self._save_data()

    def delete(self, node_key: str) -> None:
        """Удаляет ноду и сохраняет изменения."""
        if node_key in self._nodes:
            del self._nodes[node_key]
            self._save_data()

    def get_by_key(self, node_key: str) -> Dict[str, Any] | None:
        """Возвращает данные одной ноды по ключу."""
        return self._nodes.get(node_key)