# File: interfaces/persistence/i_prebuffer_template_repository.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IPrebufferTemplateRepository(ABC):
    """
    Интерфейс для репозитория, управляющего хранением шаблонов-кисточек пре-буферов.
    """
    @abstractmethod
    def get_all(self) -> Dict[str, Any]:
        """Возвращает словарь со всеми шаблонами пре-буферов."""
        pass

    @abstractmethod
    def upsert(self, prebuffer_key: str, prebuffer_data: Dict[str, Any]) -> None:
        """Обновляет или создает шаблон пре-буфера."""
        pass

    @abstractmethod
    def delete(self, prebuffer_key: str) -> None:
        """Удаляет шаблон пре-буфера по ключу."""
        pass

    @abstractmethod
    def get_by_key(self, prebuffer_key: str) -> Optional[Dict[str, Any]]:
        """Возвращает данные одного шаблона пре-буфера по ключу."""
        pass