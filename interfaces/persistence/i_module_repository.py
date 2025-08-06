from abc import ABC, abstractmethod
from typing import Dict, Any, List

class IModuleRepository(ABC):
    """
    Интерфейс для репозитория, управляющего хранением шаблонов модулей.
    """

    @abstractmethod
    def get_all(self) -> Dict[str, Any]:
        """
        Возвращает словарь со всеми шаблонами модулей.
        Ключ - ID модуля, значение - словарь с его данными.
        """
        pass

    @abstractmethod
    def upsert(self, module_key: str, module_data: Dict[str, Any]) -> None:
        """
        Обновляет существующий шаблон модуля или создает новый.
        """
        pass

    @abstractmethod
    def delete(self, module_key: str) -> None:
        """
        Удаляет шаблон модуля по его ключу.
        """
        pass

    @abstractmethod
    def get_by_key(self, module_key: str) -> Dict[str, Any] | None:
        """
        Возвращает данные одного шаблона модуля по ключу.
        """
        pass