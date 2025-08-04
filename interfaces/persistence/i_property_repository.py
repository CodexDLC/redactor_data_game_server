# File: interfaces/persistence/i_property_repository.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class IPropertyRepository(ABC):
    """
    Интерфейс для репозитория, управляющего хранением настраиваемых свойств.
    """

    @abstractmethod
    def get_all(self) -> Dict[str, Any]:
        """
        Возвращает словарь со всеми настраиваемыми свойствами.
        """
        pass

    @abstractmethod
    def upsert(self, property_key: str, property_data: Dict[str, Any]) -> None:
        """
        Обновляет или создает свойство.
        """
        pass

    @abstractmethod
    def delete(self, property_key: str) -> None:
        """
        Удаляет свойство по ключу.
        """
        pass

    @abstractmethod
    def get_by_key(self, property_key: str) -> Dict[str, Any] | None:
        """
        Возвращает данные одного свойства по ключу.
        """
        pass