# File: core/block_editor/block_editor_helpers.py
from typing import Dict, List, Optional




def calculate_all_exits(nodes_structure: List[List[Optional[int]]]) -> Dict[int, Dict[str, Optional[int]]]:
    """
    Рассчитывает все переходы для всех нодов в предоставленной структуре блока.
    """
    all_exits = {}
    height = len(nodes_structure)
    if height == 0:
        return {}
    width = len(nodes_structure[0])

    for r, row in enumerate(nodes_structure):
        for c, node_id in enumerate(row):
            if node_id is not None:
                all_exits[node_id] = _calculate_exits_for_node(r, c, width, height, nodes_structure)

    return all_exits


def _calculate_exits_for_node(r: int, c: int, width: int, height: int, structure: List[List[Optional[int]]]) -> Dict[
    str, Optional[int]]:
    """
    Внутренняя функция-помощник для расчета 8 направлений для одной ячейки.
    """
    directions = {
        "north": (-1, 0), "north_east": (-1, 1), "east": (0, 1),
        "south_east": (1, 1), "south": (1, 0), "south_west": (1, -1),
        "west": (0, -1), "north_west": (-1, -1),
    }

    exits = {}
    for name, (dr, dc) in directions.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            exits[name] = structure[nr][nc]
        else:
            exits[name] = None

    return exits