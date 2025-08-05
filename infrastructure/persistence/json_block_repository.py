import json
import os
from typing import Dict, Any

from interfaces.persistence.i_block_repository import IBlockRepository


class JsonBlockRepository(IBlockRepository):
    """
    Конкретная реализация репозитория блоков, работающая с JSON-файлом.
    """
    _FILE_PATH = "data/blocks.json"

    def __init__(self):
        self._blocks: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Загружает данные из файла в память."""
        try:
            if os.path.exists(self._FILE_PATH):
                with open(self._FILE_PATH, 'r', encoding='utf-8') as f:
                    self._blocks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._blocks = {}

    def _save_data(self) -> None:
        """Сохраняет данные из памяти в файл."""
        os.makedirs(os.path.dirname(self._FILE_PATH), exist_ok=True)
        with open(self._FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self._blocks, f, indent=4, ensure_ascii=False)

    def get_all(self) -> Dict[str, Any]:
        """Возвращает копию всех блоков."""
        return self._blocks.copy()

    def upsert(self, block_key: str, block_data: Dict[str, Any]) -> None:
        """Обновляет или создает блок и сохраняет изменения."""
        self._blocks[block_key] = block_data
        self._save_data()

    def delete(self, block_key: str) -> None:
        """Удаляет блок и сохраняет изменения."""
        if block_key in self._blocks:
            del self._blocks[block_key]
            self._save_data()