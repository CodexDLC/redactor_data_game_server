# File: interfaces/persistence/i_tag_repository.py
from abc import ABC, abstractmethod
from typing import List


class ITagRepository(ABC):
    """
    Интерфейс для репозитория, управляющего библиотекой тегов.
    """

    @abstractmethod
    def get_tags_by_category(self, category: str) -> List[str]:
        """
        Возвращает список тегов для указанной категории.

        :param category: Категория тегов (например, 'node_tags', 'block_tags').
        :return: Список тегов.
        """
        pass

    @abstractmethod
    def add_tag_to_category(self, category: str, tag: str) -> None:
        """
        Добавляет новый тег в указанную категорию, обеспечивая уникальность.

        :param category: Категория тегов.
        :param tag: Новый тег для добавления.
        """
        pass