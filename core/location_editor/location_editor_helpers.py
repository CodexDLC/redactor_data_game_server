# File: core/location_editor/location_editor_helpers.py
from typing import Any, Dict, Optional, Tuple, List
import copy

# --- ФУНКЦИЯ 1: Перенесена и сделана публичной ---
def get_parent_and_key(root: Dict, path: List) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Находит родительский элемент и ключ целевого элемента по пути.
    """
    if not path:
        return None, None

    current_level = root
    for i in range(len(path) - 1):
        key = path[i]['key']
        current_level = current_level.get('blocks_data', {}).get(key)
        if not current_level:
            return None, None

    final_key = path[-1]['key']
    return current_level, final_key

# --- ФУНКЦИЯ 2: Перенесена и сделана публичной ---
def find_target_block(current_module: Dict, target_row: int, target_col: int, path=None) -> Tuple[List, Optional[Dict]]:
    """Рекурсивно спускается по 'матрешке' до нужного блока."""
    if path is None:
        path = []

    level = current_module.get('level', 0)
    item_size_nodes = 3 ** (level + 1)

    item_row = target_row // item_size_nodes
    item_col = target_col // item_size_nodes
    item_key = f"{item_row}_{item_col}"

    next_item = current_module.get("blocks_data", {}).get(item_key)
    if not next_item:
        return [], None

    path.append({'key': item_key, 'is_module': 'level' in next_item, 'level': level})

    if 'level' in next_item:
        remaining_row = target_row % item_size_nodes
        remaining_col = target_col % item_size_nodes
        return find_target_block(next_item, remaining_row, remaining_col, path)
    else:
        return path, next_item

# --- ФУНКЦИЯ 3: Перенесена и сделана публичной ---
def create_void_module(parent_level: int) -> Dict[str, Any]:
    """Создает пустой модуль-заполнитель."""
    blocks_data = {}
    for r in range(3):
        for c in range(3):
            block_key = f"{r}_{c}"
            blocks_data[block_key] = {"template_key": "void"}

    return {
        "level": parent_level,
        "structure": [[f"{r}_{c}" for c in range(3)] for r in range(3)],
        "blocks_data": blocks_data
    }