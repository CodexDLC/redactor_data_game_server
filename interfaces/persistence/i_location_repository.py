# File: interfaces/persistence/i_room_repository.py (version 0.1)
from abc import ABC, abstractmethod
from typing import Dict, Any

class ILocationRepository(ABC):
    """Интерфейс для репозитория, управляющего хранением комнат (9x9)."""

    @abstractmethod
    def get_all(self) -> Dict[str, Any]:
        """Возвращает словарь со всеми комнатами."""
        pass

    @abstractmethod
    def upsert(self, room_key: str, room_data: Dict[str, Any]) -> None:
        """Обновляет или создает комнату."""
        pass

    @abstractmethod
    def delete(self, room_key: str) -> None:
        """Удаляет комнату по ключу."""
        pass