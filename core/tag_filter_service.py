# File: core/tag_filter_service.py
from typing import List, Optional
from interfaces.persistence.i_tag_repository import ITagRepository


class TagFilterService:
    """
    Сервис для работы с логикой фильтрации тегов.
    """

    def __init__(self, tag_repo: ITagRepository):
        self.tag_repo = tag_repo

    def get_all_tags(self, category: str) -> List[str]:
        """
        Возвращает все доступные теги для указанной категории.
        """
        return self.tag_repo.get_tags_by_category(category)

    def filter_tags(self, category: str, search_query: str) -> List[str]:
        """
        Возвращает отфильтрованный список тегов, соответствующих поисковому запросу.
        """
        all_tags = self.get_all_tags(category)
        if not search_query:
            return all_tags

        search_query_lower = search_query.strip().lower()
        return [tag for tag in all_tags if search_query_lower in tag.lower()]