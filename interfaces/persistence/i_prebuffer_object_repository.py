# File: interfaces/persistence/i_prebuffer_object_repository.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class IPrebufferObjectRepository(ABC):
    """
    Интерфейс для репозитория, управляющего хранением готовых объектов пре-буферов.
    """

    @abstractmethod
    def get_all_object_keys(self) -> List[str]:
        """Возвращает список ключей всех доступных объектов."""
        pass

    @abstractmethod
    def load_object(self, object_key: str) -> Optional[Dict[str, Any]]:
        """
        Загружает данные объекта из его папки по ключу.
        """
        pass

    @abstractmethod
    def save_object(self, object_key: str, data: Dict[str, Any]) -> None:
        """
        Сохраняет данные объекта в его папку.
        """
        pass

    @abstractmethod
    def delete_object(self, object_key: str) -> None:
        """
        Удаляет папку объекта и все ее содержимое.
        """
        pass