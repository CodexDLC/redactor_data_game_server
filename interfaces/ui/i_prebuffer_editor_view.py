# File: interfaces/ui/i_prebuffer_editor_view.py
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict

class IPrebufferEditorView(ABC):
    """
    Интерфейс для представления Редактора Пре-буферов (View).
    Определяет методы, которые View должен предоставить для Service.
    """
    @abstractmethod
    def set_form_data(self, data: Dict[str, Any]):
        """Заполняет UI данными пре-буфера."""
        pass

    @abstractmethod
    def get_form_data(self) -> Dict[str, Any]:
        """Собирает данные из UI."""
        pass

    @abstractmethod
    def bind_save_command(self, command: Callable[[], None]) -> None:
        """Привязывает команду к кнопке 'Сохранить'."""
        pass

    @abstractmethod
    def bind_delete_command(self, command: Callable[[], None]) -> None:
        """Привязывает команду к кнопке 'Удалить'."""
        pass

    @abstractmethod
    def bind_new_command(self, command: Callable[[], None]) -> None:
        """Привязывает команду к кнопке 'Создать новый'."""
        pass

    @abstractmethod
    def bind_canvas_click(self, command: Callable[[int, int, int, int], None]):
        """Привязывает команду к клику по холсту."""
        pass

    @abstractmethod
    def show_code_preview(self, data: Dict[str, Any], title: str) -> None:
        """Показывает окно с предпросмотром кода."""
        pass