# File: infrastructure/persistence/json_tag_repository.py
import json
import logging
from typing import Dict, List, Set

from interfaces.persistence.i_tag_repository import ITagRepository


class JsonTagRepository(ITagRepository):
    """
    Реализация репозитория тегов, работающая с единым JSON-файлом.
    """

    def __init__(self, filepath: str = 'data/tags_library.json'):
        self.filepath = filepath
        self.library = self._load()

    def _load(self) -> Dict[str, Set[str]]:
        """Загружает библиотеку тегов из файла и преобразует списки в множества (set)."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Превращаем каждый список тегов в set для быстрой и удобной работы
                return {category: set(tags) for category, tags in data.items()}
        except (FileNotFound, json.JSONDecodeError):
            logging.warning(f"Файл библиотеки тегов '{self.filepath}' не найден или пуст. Будет создан новый.")
            return {}

    def _save(self) -> None:
        """Сохраняет библиотеку тегов в файл, преобразуя множества (set) в отсортированные списки."""
        try:
            # Превращаем каждый set обратно в отсортированный список для красивого и предсказуемого вывода
            data_to_save = {category: sorted(list(tags)) for category, tags in self.library.items()}
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        except IOError as e:
            logging.error(f"Ошибка при сохранении файла библиотеки тегов '{self.filepath}': {e}")

    def get_tags_by_category(self, category: str) -> List[str]:
        """Возвращает отсортированный список тегов для указанной категории."""
        tags_set = self.library.get(category, set())
        return sorted(list(tags_set))

    def add_tag_to_category(self, category: str, tag: str) -> None:
        """Добавляет новый тег в категорию, если его там еще нет."""
        clean_tag = tag.strip().lower()
        if not clean_tag:
            return

        tags_set = self.library.setdefault(category, set())

        if clean_tag not in tags_set:
            tags_set.add(clean_tag)
            logging.info(f"Добавлен новый тег '{clean_tag}' в категорию '{category}'. Сохранение библиотеки.")
            self._save()
        else:
            logging.debug(f"Тег '{clean_tag}' уже существует в категории '{category}'. Сохранение не требуется.")

    # --- НОВЫЙ МЕТОД ---
    def add_tags_to_category(self, category: str, tags: List[str]) -> None:
        """
        Добавляет список тегов в указанную категорию.
        """
        for tag in tags:
            self.add_tag_to_category(category, tag)