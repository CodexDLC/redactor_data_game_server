# File: infrastructure/persistence/json_property_repository.py
import json
import os
from typing import Dict, Any
from interfaces.persistence.i_property_repository import IPropertyRepository


class JsonPropertyRepository(IPropertyRepository):
    """
    Реализация репозитория для настраиваемых свойств, работающая с JSON-файлом.
    """
    def __init__(self, file_path: str = "data/properties.json"):
        self.file_path = file_path
        self._data: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Загружает данные из файла."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {}

    def _save_data(self) -> None:
        """Сохраняет данные в файл."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)

    def get_all(self) -> Dict[str, Any]:
        """Возвращает словарь со всеми свойствами."""
        return self._data

    def upsert(self, property_key: str, property_data: Dict[str, Any]) -> None:
        """Обновляет или создает свойство."""
        self._data[property_key] = property_data
        self._save_data()

    def delete(self, property_key: str) -> None:
        """Удаляет свойство по ключу."""
        if property_key in self._data:
            del self._data[property_key]
            self._save_data()

    def get_by_key(self, property_key: str) -> Dict[str, Any] | None:
        """Возвращает данные одного свойства по ключу."""
        return self._data.get(property_key)