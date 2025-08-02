import json
import os
from tkinter import messagebox

# Получаем путь к родительской директории (editor_logic)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BLOCKS_JSON_FILE = os.path.join(BASE_DIR, 'data', 'blocks.json')
ROOMS_JSON_FILE = os.path.join(BASE_DIR, 'data', 'rooms.json')
MAPS_DIR = os.path.join(BASE_DIR, 'data', 'maps')
TILES_JSON_FILE = os.path.join(BASE_DIR, 'data', 'tiles.json') # Добавлен TILES_JSON_FILE
DEFAULT_BLOCK_NAME = "default_floor"


def save_json_file(file_path, data):
    """
    Сохраняет словарь в указанный JSON-файл.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True, "Файл успешно сохранен."
    except Exception as e:
        return False, f"Ошибка при сохранении: {e}"


def load_json_file(file_path):
    """
    Загружает словарь из указанного JSON-файла.
    """
    if not os.path.exists(file_path):
        return {}, f"Файл {os.path.basename(file_path)} не найден. Создан пустой словарь."

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data, "Файл успешно загружен."
    except json.JSONDecodeError:
        return {}, f"Не удалось прочитать {os.path.basename(file_path)}. Файл пуст или поврежден."
    except Exception as e:
        return {}, f"Ошибка при загрузке: {e}"


def save_blocks_to_json(blocks_dict):
    return save_json_file(BLOCKS_JSON_FILE, blocks_dict)

def load_blocks_from_json():
    """
    Загружает словарь блоков из файла blocks.json.
    """
    return load_json_file(BLOCKS_JSON_FILE)


def delete_block_from_json(block_name):
    blocks_dict, message = load_blocks_from_json()
    if block_name in blocks_dict:
        del blocks_dict[block_name]
        return save_blocks_to_json(blocks_dict)
    else:
        return False, f"Блок '{block_name}' не найден."


def generate_code_from_grid(grid_data):
    output_code = "(\n"
    for row in grid_data:
        row_str = "    (" + ", ".join(map(str, row)) + "),\n"
        output_code += row_str
    output_code += ")"
    return output_code

def save_map_to_json(map_name, map_data):
    file_path = os.path.join(MAPS_DIR, f"{map_name}.json")
    return save_json_file(file_path, map_data)

def load_map_from_json(map_name):
    file_path = os.path.join(MAPS_DIR, f"{map_name}.json")
    return load_json_file(file_path)

def save_tiles_to_json(tiles_dict):
    return save_json_file(TILES_JSON_FILE, tiles_dict)

def load_tiles_from_json():
    return load_json_file(TILES_JSON_FILE)