import json
import os
from typing import Dict, Any
from interfaces.persistence.i_module_repository import IModuleRepository


class JsonModuleRepository(IModuleRepository):
    """
    Конкретная реализация репозитория модулей, работающая с JSON-файлом.
    """
    _FILE_PATH = "data/templates/modules.json"

    def __init__(self):
        self._modules: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Загружает данные из файла в память."""
        try:
            if os.path.exists(self._FILE_PATH):
                with open(self._FILE_PATH, 'r', encoding='utf-8') as f:
                    self._modules = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._modules = {}

    def _save_data(self) -> None:
        """Сохраняет данные из памяти в файл."""
        os.makedirs(os.path.dirname(self._FILE_PATH), exist_ok=True)
        with open(self._FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self._modules, f, indent=4, ensure_ascii=False)

    def get_all(self) -> Dict[str, Any]:
        """Возвращает копию всех модулей."""
        return self._modules.copy()

    def upsert(self, module_key: str, module_data: Dict[str, Any]) -> None:
        """Обновляет или создает модуль и сохраняет изменения."""
        self._modules[module_key] = module_data
        self._save_data()

    def delete(self, module_key: str) -> None:
        """Удаляет модуль по ключу."""
        if module_key in self._modules:
            del self._modules[module_key]
            self._save_data()

    def get_by_key(self, module_key: str) -> Dict[str, Any] | None:
        """Возвращает данные одного модуля по ключу."""
        return self._modules.get(module_key)