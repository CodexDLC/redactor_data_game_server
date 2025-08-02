# templates.py

# --- Уровень 1: Система кодирования Точек ---
WALL, FLOOR, EXIT = 0, 1, 2

# --- Уровень 2: Библиотека "LEGO-блоков" 3x3 ---
BLOCK_WALL_W = ((WALL, FLOOR, FLOOR), (WALL, FLOOR, FLOOR), (WALL, FLOOR, FLOOR))
BLOCK_WALL_N = ((WALL, WALL, WALL), (FLOOR, FLOOR, FLOOR), (FLOOR, FLOOR, FLOOR))
BLOCK_WALL_E = ((FLOOR, FLOOR, WALL), (FLOOR, FLOOR, WALL), (FLOOR, FLOOR, WALL))
BLOCK_WALL_S = ((FLOOR, FLOOR, FLOOR), (FLOOR, FLOOR, FLOOR), (WALL, WALL, WALL))
BLOCK_SOLID_WALL = ((WALL, WALL, WALL), (WALL, WALL, WALL), (WALL, WALL, WALL))

BLOCK_CORNER_NW = ((WALL, WALL, WALL), (WALL, FLOOR, FLOOR), (WALL, FLOOR, FLOOR))
BLOCK_CORNER_NE = ((WALL, WALL, WALL), (FLOOR, FLOOR, WALL), (FLOOR, FLOOR, WALL))
BLOCK_CORNER_SE = ((WALL, FLOOR, FLOOR), (FLOOR, FLOOR, WALL), (WALL, WALL, WALL))
BLOCK_CORNER_SW = ((WALL, FLOOR, FLOOR), (WALL, FLOOR, FLOOR), (WALL, WALL, WALL))

BLOCK_HALL = ((FLOOR, FLOOR, FLOOR), (FLOOR, FLOOR, FLOOR), (FLOOR, FLOOR, FLOOR))
BLOCK_HALL_PILLAR = ((FLOOR, FLOOR, FLOOR), (FLOOR, WALL, FLOOR), (FLOOR, FLOOR, FLOOR))
BLOCK_CORRIDOR_STRAIGHT = ((WALL, FLOOR, WALL), (FLOOR, FLOOR, FLOOR), (WALL, FLOOR, WALL))
BLOCK_CROSS = ((FLOOR, WALL, FLOOR), (WALL, EXIT, WALL), (FLOOR, WALL, FLOOR))

BLOCK_GATE_N = ((WALL, EXIT, WALL), (FLOOR, FLOOR, FLOOR), (FLOOR, FLOOR, FLOOR))
BLOCK_GATE_S = ((FLOOR, FLOOR, FLOOR), (FLOOR, FLOOR, FLOOR), (WALL, EXIT, WALL))
BLOCK_GATE_W = ((WALL, FLOOR, FLOOR), (EXIT, FLOOR, FLOOR), (WALL, FLOOR, FLOOR))
BLOCK_GATE_E = ((FLOOR, FLOOR, WALL), (FLOOR, FLOOR, EXIT), (FLOOR, FLOOR, WALL))

# --- Уровень 3: "Чертежи" Комнат ---
START_ROOM_BLUEPRINT = ((BLOCK_CORNER_NW, BLOCK_WALL_N, BLOCK_CORNER_NE),
                        (BLOCK_GATE_W, BLOCK_HALL, BLOCK_GATE_E),
                        (BLOCK_CORNER_SW, BLOCK_GATE_S, BLOCK_CORNER_SE))

# Исправленные чертежи, соответствующие вашему изображению
CORRIDOR_NS_BLUEPRINT = ((BLOCK_WALL_W, BLOCK_GATE_N, BLOCK_WALL_E),
                         (BLOCK_HALL, BLOCK_HALL, BLOCK_HALL),
                         (BLOCK_WALL_W, BLOCK_GATE_S, BLOCK_WALL_E))

CORRIDOR_EW_BLUEPRINT = ((BLOCK_WALL_N, BLOCK_HALL, BLOCK_WALL_N),
                         (BLOCK_GATE_W, BLOCK_HALL, BLOCK_GATE_E),
                         (BLOCK_WALL_S, BLOCK_HALL, BLOCK_WALL_S))


CROSSROAD_BLUEPRINT = ((BLOCK_CORNER_SE, BLOCK_GATE_N, BLOCK_CORNER_SW),
                       (BLOCK_GATE_W, BLOCK_HALL, BLOCK_GATE_E),
                       (BLOCK_CORNER_NE, BLOCK_GATE_S, BLOCK_CORNER_NW))

# Новые чертежи тупиков для всех направлений
DEAD_END_ROOM_S_BLUEPRINT = ((BLOCK_HALL, BLOCK_WALL_N, BLOCK_HALL),
                             (BLOCK_HALL, BLOCK_HALL, BLOCK_HALL),
                             (BLOCK_HALL, BLOCK_GATE_S, BLOCK_HALL))

DEAD_END_ROOM_N_BLUEPRINT = ((BLOCK_HALL, BLOCK_GATE_N, BLOCK_HALL),
                             (BLOCK_HALL, BLOCK_HALL, BLOCK_HALL),
                             (BLOCK_HALL, BLOCK_WALL_S, BLOCK_HALL))

DEAD_END_ROOM_E_BLUEPRINT = ((BLOCK_HALL, BLOCK_HALL, BLOCK_WALL_W),
                             (BLOCK_HALL, BLOCK_HALL, BLOCK_GATE_E),
                             (BLOCK_HALL, BLOCK_HALL, BLOCK_WALL_W))

DEAD_END_ROOM_W_BLUEPRINT = ((BLOCK_WALL_E, BLOCK_HALL, BLOCK_HALL),
                             (BLOCK_GATE_W, BLOCK_HALL, BLOCK_HALL),
                             (BLOCK_WALL_E, BLOCK_HALL, BLOCK_HALL))


FINAL_ROOM_S_BLUEPRINT = ((BLOCK_CORNER_NW, BLOCK_WALL_N, BLOCK_CORNER_NE),
                          (BLOCK_WALL_W, BLOCK_HALL_PILLAR, BLOCK_WALL_E),
                          (BLOCK_CORNER_SW, BLOCK_GATE_S, BLOCK_CORNER_SE))


# --- Уровень 4: Коллекции комнат для генератора ---
CORRIDOR_TEMPLATES = {
    "С": [
        {"name": "corridor_ns", "blueprint": CORRIDOR_NS_BLUEPRINT, "exits": {'С', 'Ю'}},
        {"name": "crossroad", "blueprint": CROSSROAD_BLUEPRINT, "exits": {'С', 'Ю', 'З', 'В'}}
    ],
    "Ю": [
        {"name": "corridor_ns", "blueprint": CORRIDOR_NS_BLUEPRINT, "exits": {'С', 'Ю'}},
        {"name": "dead_end", "blueprint": DEAD_END_ROOM_S_BLUEPRINT, "exits": {'Ю'}},
        {"name": "crossroad", "blueprint": CROSSROAD_BLUEPRINT, "exits": {'С', 'Ю', 'З', 'В'}}
    ],
    "З": [
        {"name": "corridor_ew", "blueprint": CORRIDOR_EW_BLUEPRINT, "exits": {'З', 'В'}},
        {"name": "crossroad", "blueprint": CROSSROAD_BLUEPRINT, "exits": {'С', 'Ю', 'З', 'В'}}
    ],
    "В": [
        {"name": "corridor_ew", "blueprint": CORRIDOR_EW_BLUEPRINT, "exits": {'З', 'В'}},
        {"name": "crossroad", "blueprint": CROSSROAD_BLUEPRINT, "exits": {'С', 'Ю', 'З', 'В'}}
    ],
}

DEAD_END_TEMPLATES = {
    "С": [{"name": "dead_end_n", "blueprint": DEAD_END_ROOM_N_BLUEPRINT, "exits": {'С'}}],
    "Ю": [{"name": "dead_end_s", "blueprint": DEAD_END_ROOM_S_BLUEPRINT, "exits": {'Ю'}}],
    "З": [{"name": "dead_end_w", "blueprint": DEAD_END_ROOM_W_BLUEPRINT, "exits": {'З'}}],
    "В": [{"name": "dead_end_e", "blueprint": DEAD_END_ROOM_E_BLUEPRINT, "exits": {'В'}}],
}

START_ROOM_TEMPLATES = [
    {"name": "start_room", "blueprint": START_ROOM_BLUEPRINT, "exits": {'Ю', 'З', 'В'}},
]

STANDARD_ROOM_TEMPLATES = [
    # TODO: Добавить сюда чертежи других комнат
]

FINAL_ROOM_TEMPLATES = [
    {"name": "final_room", "blueprint": FINAL_ROOM_S_BLUEPRINT, "exits": {'Ю'}},
]