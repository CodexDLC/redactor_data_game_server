from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable


class IBlockEditorView(ABC):
    """Интерфейс для Представления (View) редактора блоков."""

    @abstractmethod
    def update_block_list_in_palette(self, block_keys: List[str]) -> None:
        """Обновляет список блоков в левой панели-палитре."""
        pass

    @abstractmethod
    def get_grid_data(self) -> List[List[str]]:
        """Возвращает текущее состояние сетки 3x3 (массив из ID нод)."""
        pass

    @abstractmethod
    def draw_grid(self, grid_data: List[List[str]]) -> None:
        """Отрисовывает сетку 3x3 на основе предоставленных данных."""
        pass

    # Здесь будут и другие методы для связи с UI...