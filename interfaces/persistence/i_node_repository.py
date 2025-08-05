from abc import ABC, abstractmethod
from typing import Dict, Any

class INodeRepository(ABC):
    """
    Интерфейс для репозитория, управляющего хранением базовых нод (1x1).
    """

    @abstractmethod
    def get_all(self) -> Dict[str, Any]:
        """
        Возвращает словарь со всеми нодами.
        Ключ - ID ноды, значение - словарь с ее данными.
        """
        pass

    @abstractmethod
    def upsert(self, node_key: str, node_data: Dict[str, Any]) -> None:
        """
        Обновляет существующую ноду или создает новую, если она не существует.
        """
        pass

    @abstractmethod
    def delete(self, node_key: str) -> None:
        """
        Удаляет ноду по ее ключу.
        """
        pass

    @abstractmethod
    def get_by_key(self, node_key: str) -> Dict[str, Any] | None:
        """Возвращает данные одной ноды по ключу."""
        pass