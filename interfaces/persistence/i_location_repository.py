# File: interfaces/persistence/i_location_repository.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ILocationRepository(ABC):
    """
    Интерфейс для репозитория, управляющего хранением комнат/локаций в файловой системе.
    Теперь работает с отдельными файлами для блоков, объектов и карты.
    """

    @abstractmethod
    def get_all_location_names(self) -> List[str]:
        """
        Возвращает список имен всех доступных локаций (имен папок).
        """
        pass

    @abstractmethod
    def load_location(self, location_key: str) -> Dict[str, Any] | None:
        """
        Загружает полную структуру локации из ее папки по ключу (имени папки).
        Возвращает None, если локация не найдена.
        """
        pass

    @abstractmethod
    def save_location(self, location_key: str, data: Dict[str, Any]) -> None:
        """
        Сохраняет полную структуру локации в ее папку.
        Раскладывает данные на несколько файлов: blocks, objects, map.
        """
        pass

    @abstractmethod
    def delete_location(self, location_key: str) -> None:
        """
        Удаляет папку локации и все ее содержимое.
        """
        pass