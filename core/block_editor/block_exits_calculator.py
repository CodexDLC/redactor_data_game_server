# File: core/block_editor/block_exits_calculator.py
from typing import Dict, List, Optional


class BlockExitsCalculator:
    """
    Класс-помощник, отвечающий за расчет внутренних переходов (exits)
    внутри одного блока 3x3.
    """

    def calculate_all_exits(self, nodes_structure: List[List[Optional[str]]]) -> Dict[str, Dict[str, Optional[str]]]:
        """
        Рассчитывает все переходы для всех нодов в предоставленной структуре блока.

        :param nodes_structure: Двумерный список 3x3 с ID нодов.
        :return: Словарь, где ключ - это ID нода, а значение - словарь его выходов.
                 Пример: { "node_id_1_1": {"north": "node_id_0_1", "north_east": "node_id_0_2", ...} }
        """
        all_exits = {}
        if not nodes_structure or len(nodes_structure) != 3:
            return {}

        for r, row in enumerate(nodes_structure):
            if len(row) != 3:
                return {}  # Некорректная структура
            for c, node_id in enumerate(row):
                if node_id:
                    all_exits[node_id] = self._calculate_exits_for_node(r, c, nodes_structure)

        return all_exits

    def _calculate_exits_for_node(self, r: int, c: int, structure: List[List[Optional[str]]]) -> Dict[
        str, Optional[str]]:
        """
        Рассчитывает 8 направлений для одной конкретной ячейки.
        """
        # (dr, dc) - смещение по строке и столбцу
        directions = {
            "north": (-1, 0),
            "north_east": (-1, 1),
            "east": (0, 1),
            "south_east": (1, 1),
            "south": (1, 0),
            "south_west": (1, -1),
            "west": (0, -1),
            "north_west": (-1, -1),
        }

        exits = {}
        for name, (dr, dc) in directions.items():
            nr, nc = r + dr, c + dc  # Новые координаты соседа

            # Проверяем, что сосед находится в пределах сетки 3x3
            if 0 <= nr < 3 and 0 <= nc < 3:
                neighbor_id = structure[nr][nc]
                exits[name] = neighbor_id
            else:
                exits[name] = None  # Выход за пределы блока

        return exits