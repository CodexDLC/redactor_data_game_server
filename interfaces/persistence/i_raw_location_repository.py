from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IRawLocationRepository(ABC):
    """
    Интерфейс для репозитория, управляющего временным файлом-черновиком.
    """
    @abstractmethod
    def upsert(self, location_data: Dict[str, Any]) -> None:
        """
        Сохраняет или обновляет данные всей локации в едином временном файле.
        """
        pass

    @abstractmethod
    def load(self) -> Optional[Dict[str, Any]]:
        """
        Загружает данные локации из временного файла.
        Возвращает None, если файл не существует.
        """
        pass

    @abstractmethod
    def delete(self) -> None:
        """
        Удаляет временный файл-черновик.
        """
        pass