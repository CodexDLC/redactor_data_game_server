# File: interfaces/ui/i_block_editor_view.py
from typing import Any, Callable
from abc import ABC, abstractmethod


class IBlockEditorView(ABC):
    @abstractmethod
    def set_form_data(self, data: dict) -> None:
        pass

    @abstractmethod
    def get_form_data(self) -> dict:
        pass

    @abstractmethod
    def clear_form(self) -> None:
        pass

    @abstractmethod
    def bind_save_command(self, command: Callable[[Any], None]) -> None:
        pass

    @abstractmethod
    def bind_delete_command(self, command: Callable[[Any], None]) -> None:
        pass

    @abstractmethod
    def bind_new_command(self, command: Callable[[Any], None]) -> None:
        pass