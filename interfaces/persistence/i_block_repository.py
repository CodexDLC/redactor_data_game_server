from abc import ABC, abstractmethod
from typing import Dict, Any

class IBlockRepository(ABC):
    """Интерфейс для репозитория, управляющего хранением блоков (3x3)."""

    @abstractmethod
    def get_all(self) -> Dict[str, Any]:
        """Возвращает словарь со всеми блоками."""
        pass

    @abstractmethod
    def upsert(self, block_key: str, block_data: Dict[str, Any]) -> None:
        """Обновляет или создает блок."""
        pass

    @abstractmethod
    def delete(self, block_key: str) -> None:
        """Удаляет блок по ключу."""
        pass