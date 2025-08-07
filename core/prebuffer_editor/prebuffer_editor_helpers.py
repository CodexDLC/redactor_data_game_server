# File: core/prebuffer_editor/prebuffer_editor_helpers.py
from typing import Dict, List, Optional, Any
from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.persistence.i_node_repository import INodeRepository


def materialize_prebuffer(
        blocks_structure: List[List[str]],
        block_repo: IBlockRepository,
        node_repo: INodeRepository
) -> Dict[str, Any]:
    """
    Материализует 3x3 структуру блоков в плоскую 9x9 структуру нодов.
    """
    nodes_structure = [[None for _ in range(9)] for _ in range(9)]
    nodes_data = {}

    global_y = 0

    for block_row_index, block_row in enumerate(blocks_structure):
        for block_col_index, block_key in enumerate(block_row):
            if not block_key:
                continue

            block = block_repo.get_by_key(block_key)
            if not block:
                continue

            block_nodes_structure = block.get('nodes_structure', [[None for _ in range(3)] for _ in range(3)])
            block_nodes_data = block.get('nodes_data', {})

            for node_row in range(3):
                for node_col in range(3):
                    global_row = block_row_index * 3 + node_row
                    global_col = block_col_index * 3 + node_col

                    global_node_id = f"{global_row}_{global_col}"

                    nodes_structure[global_row][global_col] = global_node_id

                    node_id_in_block = block_nodes_structure[node_row][node_col]

                    if node_id_in_block is not None:
                        node_details = block_nodes_data.get(str(node_id_in_block))
                        if node_details:
                            nodes_data[global_node_id] = node_details.copy()

    return {
        "nodes_structure": nodes_structure,
        "nodes_data": nodes_data
    }


def _calculate_exits_for_node(
        r: int,
        c: int,
        width: int,
        height: int,
        structure: List[List[str | None]],
        nodes_data: Dict[str, Any]
) -> Dict[str, Optional[str]]:
    """
    Вспомогательная функция для расчета 8 направлений для одной ячейки.
    Проверяет, является ли соседний нод 'walkable'.
    """
    directions = {
        "north": (-1, 0), "north_east": (-1, 1), "east": (0, 1),
        "south_east": (1, 1), "south": (1, 0), "south_west": (1, -1),
        "west": (0, -1), "north_west": (-1, -1),
    }

    exits = {}
    current_node_id = structure[r][c]

    for name, (dr, dc) in directions.items():
        nr, nc = r + dr, c + dc

        if 0 <= nr < height and 0 <= nc < width:
            neighbor_node_id = structure[nr][nc]
            if neighbor_node_id is not None:
                # Проверяем, является ли соседний нод "проходимым"
                neighbor_template = nodes_data.get(neighbor_node_id, {}).get('template_key')
                if neighbor_template == 'walkable':
                    exits[name] = neighbor_node_id
                else:
                    exits[name] = None
            else:
                exits[name] = None
        else:
            exits[name] = None

    return exits


def calculate_all_exits(
        nodes_structure: List[List[str | None]],
        nodes_data: Dict[str, Any]
) -> Dict[str, Dict[str, Optional[str]]]:
    """
    Рассчитывает все переходы для всех нодов в предоставленной структуре,
    проверяя, является ли соседняя клетка "проходимой".
    """
    all_exits = {}
    height = len(nodes_structure)
    if height == 0:
        return {}
    width = len(nodes_structure[0])

    for r, row in enumerate(nodes_structure):
        for c, node_id in enumerate(row):
            if node_id is not None:
                # Передаем nodes_data в вспомогательную функцию
                all_exits[node_id] = _calculate_exits_for_node(r, c, width, height, nodes_structure, nodes_data)

    return all_exits