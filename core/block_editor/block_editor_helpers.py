# File: core/block_editor/block_editor_helpers.py
from typing import Dict




# --- Наша старая функция ---
def transform_nodes_data_for_saving(nodes_data: Dict) -> Dict:
    """Убирает временные поля (как 'color') из данных перед сохранением."""
    clean_data = {}
    for node_id, details in nodes_data.items():
        new_details = details.copy()
        new_details.pop('color', None)
        clean_data[node_id] = new_details
    return clean_data


