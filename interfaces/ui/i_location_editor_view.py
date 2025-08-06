# File: interfaces/ui/i_location_editor_view.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Callable

# --- СТРОКА НИЖЕ БЫЛА ОШИБКОЙ И УДАЛЕНА ---
# from interfaces.ui.i_location_editor_view import ILocationEditorView

class ILocationEditorView(ABC):
    """
    Интерфейс для Представления (View) редактора локаций.
    Определяет, как сервис может взаимодействовать с UI этого редактора.
    """

    @abstractmethod
    def set_form_data(self, data: Dict[str, Any]) -> None:
        """Заполняет поля формы на правой панели данными локации."""
        pass

    @abstractmethod
    def get_form_data(self) -> Dict[str, Any]:
        """Собирает и возвращает все данные из полей формы."""
        pass

    @abstractmethod
    def clear_form(self) -> None:
        """Очищает все поля на форме."""
        pass

    @abstractmethod
    def draw_canvas(self) -> None:
        """Запускает полную перерисовку холста на основе текущих данных."""
        pass

    @abstractmethod
    def bind_save_command(self, command: Callable[[], None]) -> None:
        """Привязывает команду (функцию) к кнопке 'Сохранить'."""
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
    def bind_canvas_click(self, command: Callable[[Any], None]) -> None:
        """Привязывает команду к событию клика по холсту."""
        pass
