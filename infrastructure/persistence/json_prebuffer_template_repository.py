# File: infrastructure/persistence/json_prebuffer_template_repository.py
import json
import os
from typing import Dict, Any, Optional

from interfaces.persistence.i_prebuffer_template_repository import IPrebufferTemplateRepository

class JsonPrebufferTemplateRepository(IPrebufferTemplateRepository):
    """
    Репозиторий для шаблонов-кисточек пре-буферов, работающий с JSON-файлом.
    """
    _FILE_PATH = "data/templates/prebuffers.json"

    def __init__(self):
        self._templates: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Загружает данные из файла в память."""
        try:
            if os.path.exists(self._FILE_PATH):
                with open(self._FILE_PATH, 'r', encoding='utf-8') as f:
                    self._templates = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._templates = {}

    def _save_data(self) -> None:
        """Сохраняет данные из памяти в файл."""
        os.makedirs(os.path.dirname(self._FILE_PATH), exist_ok=True)
        with open(self._FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self._templates, f, indent=4, ensure_ascii=False)

    def get_all(self) -> Dict[str, Any]:
        """Возвращает копию всех шаблонов."""
        return self._templates.copy()

    def upsert(self, prebuffer_key: str, prebuffer_data: Dict[str, Any]) -> None:
        """Обновляет или создает шаблон и сохраняет изменения."""
        self._templates[prebuffer_key] = prebuffer_data
        self._save_data()

    def delete(self, prebuffer_key: str) -> None:
        """Удаляет шаблон по ключу."""
        if prebuffer_key in self._templates:
            del self._templates[prebuffer_key]
            self._save_data()

    def get_by_key(self, prebuffer_key: str) -> Optional[Dict[str, Any]]:
        """Возвращает данные одного шаблона по ключу."""
        return self._templates.get(prebuffer_key)