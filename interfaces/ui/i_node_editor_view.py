from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable

class INodeEditorView(ABC):
    """
    Интерфейс для Представления (View) редактора нод.
    Определяет, как ядро приложения взаимодействует с UI.
    """

    @abstractmethod
    def update_node_list(self, node_keys: List[str]) -> None:
        """Обновляет список нод, отображаемый в левой панели."""
        pass

    @abstractmethod
    def get_form_data(self) -> Dict[str, Any]:
        """Собирает и возвращает все данные из полей формы на правой панели."""
        pass

    @abstractmethod
    def set_form_data(self, node_data: Dict[str, Any]) -> None:
        """Заполняет поля формы на правой панели данными указанной ноды."""
        pass

    @abstractmethod
    def clear_form(self) -> None:
        """Очищает все поля на форме."""
        pass

    @abstractmethod
    def get_selected_node_key(self) -> str | None:
        """Возвращает ключ ноды, выбранной в данный момент в списке."""
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
    def bind_list_selection_command(self, command: Callable[[Any], None]) -> None:
        """Привязывает команду к событию выбора элемента в списке."""
        pass