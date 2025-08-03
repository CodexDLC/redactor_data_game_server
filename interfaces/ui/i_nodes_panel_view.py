# File: interfaces/ui/i_nodes_panel_view.py (version 0.1)
from abc import ABC, abstractmethod
from typing import List, Callable, Any

class INodesPanelView(ABC):
    """
    Интерфейс для представления (View) панели со списком нод.
    Определяет, как сервис может взаимодействовать с этим списком.
    """

    @abstractmethod
    def update_node_list(self, node_keys: List[str]) -> None:
        """Обновляет список нод, отображаемый на панели."""
        pass

    @abstractmethod
    def get_selected_node_key(self) -> str | None:
        """Возвращает ключ ноды, выбранной в данный момент в списке."""
        pass

    @abstractmethod
    def bind_list_selection_command(self, command: Callable[[Any], None]) -> None:
        """Привязывает команду к событию выбора элемента в списке."""
        pass