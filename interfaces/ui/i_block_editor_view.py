# File: interfaces/ui/i_block_editor_view.py
from abc import ABC, abstractmethod
from typing import Callable, Any, Dict, List


class IBlockEditorView(ABC):

    @abstractmethod
    def set_form_data(self, data: dict) -> None:
        """Устанавливает данные в форму."""
        pass

    @abstractmethod
    def get_form_data(self) -> dict:
        """Получает данные из формы."""
        pass

    @abstractmethod
    def clear_form(self) -> None:
        """Очищает форму."""
        pass

    # --- Оставляем только самые базовые методы для привязки команд ---

    @abstractmethod
    def bind_save_command(self, command: Callable[[], None]) -> None:
        pass

    @abstractmethod
    def bind_delete_command(self, command: Callable[[], None]) -> None:
        pass

    @abstractmethod
    def bind_new_command(self, command: Callable[[], None]) -> None:
        pass

    @abstractmethod
    def bind_canvas_click(self, callback: Callable[[int, int, str | None], None]):
        pass