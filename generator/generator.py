# generator.py

import random
from .templates import *
import pygame


# --- Класс для Комнат (внутри генератора) ---
class Room:
    def __init__(self, room_id, room_r, room_c, name, blueprint, exits):
        self.room_id = room_id
        self.room_r = room_r
        self.room_c = room_c
        self.name = name
        self.exits = exits
        self.grid = self._assemble_from_blueprint(room_id, blueprint)

    @staticmethod
    def _assemble_from_blueprint(room_id, blueprint):
        final_grid = {}
        for block_r in range(3):
            for block_c in range(3):
                block = blueprint[block_r][block_c]
                if block is None: continue
                for r in range(3):
                    for c in range(3):
                        sub_r, sub_c = block_r * 3 + r, block_c * 3 + c
                        node_value = block[r][c]
                        if node_value is not None:
                            tile_id = f"{room_id}_{sub_r}_{sub_c}"
                            final_grid[f"{sub_r}_{sub_c}"] = {"id": tile_id, "type": node_value}
        return final_grid


# --- Класс-интерфейс для внешних модулей ---
class DungeonGenerator:
    def __init__(self):
        self.room_counter = 0

    def _get_next_room_id(self, r, c):
        self.room_counter += 1
        return f"room_{r}_{c}"

    def start_new_dungeon(self, character_id=None, seed=None):
        """ Инициализирует новое подземелье. """
        self.room_counter = 0
        random.seed(seed)

        start_room_template = random.choice(START_ROOM_TEMPLATES)
        start_room_id = self._get_next_room_id(0, 0)
        start_room = Room(start_room_id, 0, 0, start_room_template["name"], start_room_template["blueprint"],
                          start_room_template["exits"])

        dungeon_document = {
            "dungeon_id": f"dungeon_{start_room_id}",
            "character_id": character_id,
            "seed": seed,
            "dungeon_progress": {
                "visited_rooms": set(),
                "max_rooms": 10
            },
            "rooms": {start_room_id: start_room.__dict__},
            "current_room_id": start_room_id,
            "player_first_move": True
        }

        dungeon_document["dungeon_progress"]["visited_rooms"].add(start_room_id)

        self._generate_new_rooms(dungeon_document, start_room.__dict__)

        return dungeon_document

    def _get_open_exits(self, dungeon_document):
        """ Возвращает список всех незаполненных выходов на карте. """
        open_exits = []
        for room_id, room_data in dungeon_document["rooms"].items():
            for exit_direction in room_data["exits"]:
                room_r, room_c = room_data["room_r"], room_data["room_c"]
                neighbor_r, neighbor_c = room_r, room_c
                if exit_direction == "С":
                    neighbor_r -= 1
                elif exit_direction == "Ю":
                    neighbor_r += 1
                elif exit_direction == "З":
                    neighbor_c -= 1
                elif exit_direction == "В":
                    neighbor_c += 1

                neighbor_id = self._get_next_room_id(neighbor_r,
                                                     neighbor_c)  # Эта часть логики неверна. Нужно проверять существующий ID
                is_connected = False
                for existing_room_id, _ in dungeon_document["rooms"].items():
                    if existing_room_id.startswith(f"room_{neighbor_r}_{neighbor_c}"):
                        is_connected = True
                        break

                if not is_connected:
                    open_exits.append((room_id, exit_direction, (neighbor_r, neighbor_c)))
        return open_exits

    def _generate_new_rooms(self, dungeon_document, current_room):
        """ Генерирует новые комнаты вокруг заданной. """
        current_grid = dungeon_document["rooms"]
        room_r, room_c = current_room["room_r"], current_room["room_c"]

        # Новая логика: Проверка лимита комнат и открытых выходов
        remaining_rooms = dungeon_document["dungeon_progress"]["max_rooms"] - len(current_grid)
        open_exits = self._get_open_exits(dungeon_document)

        if remaining_rooms <= len(open_exits) and remaining_rooms > 0:
            # Если количество оставшихся комнат меньше или равно количеству открытых выходов,
            # мы должны запустить сценарий "конца игры"
            pass  # Пока оставляем пустым, чтобы не вызывать дважды генерацию.

        empty_neighbors = {}
        if "С" in current_room["exits"] and f"room_{room_r - 1}_{room_c}" not in current_grid:
            empty_neighbors["С"] = (room_r - 1, room_c)
        if "Ю" in current_room["exits"] and f"room_{room_r + 1}_{room_c}" not in current_grid:
            empty_neighbors["Ю"] = (room_r + 1, room_c)
        if "З" in current_room["exits"] and f"room_{room_r}_{room_c - 1}" not in current_grid:
            empty_neighbors["З"] = (room_r, room_c - 1)
        if "В" in current_room["exits"] and f"room_{room_r}_{room_c + 1}" not in current_grid:
            empty_neighbors["В"] = (room_r, room_c + 1)

        for direction, (nr, nc) in empty_neighbors.items():
            required_exit = {"С": "Ю", "Ю": "С", "З": "В", "В": "З"}[direction]

            possible_rooms = CORRIDOR_TEMPLATES.get(required_exit, [])
            if possible_rooms:
                room_template = random.choice(possible_rooms)
                room_id = self._get_next_room_id(nr, nc)
                new_room = Room(room_id, nr, nc, room_template["name"], room_template["blueprint"],
                                room_template["exits"])
                dungeon_document["rooms"][room_id] = new_room.__dict__

    def _seal_unchosen_paths(self, dungeon_document, player_room_id, chosen_direction):
        """ Запечатывает невыбранные пути, ставя тупиковые комнаты. """
        player_room = dungeon_document["rooms"][player_room_id]
        room_r, room_c = player_room["room_r"], player_room["room_c"]

        empty_neighbors = {}
        if "С" in player_room["exits"] and f"room_{room_r - 1}_{room_c}" not in dungeon_document["rooms"]:
            empty_neighbors["С"] = (room_r - 1, room_c)
        if "Ю" in player_room["exits"] and f"room_{room_r + 1}_{room_c}" not in dungeon_document["rooms"]:
            empty_neighbors["Ю"] = (room_r + 1, room_c)
        if "З" in player_room["exits"] and f"room_{room_r}_{room_c - 1}" not in dungeon_document["rooms"]:
            empty_neighbors["З"] = (room_r, room_c - 1)
        if "В" in player_room["exits"] and f"room_{room_r}_{room_c + 1}" not in dungeon_document["rooms"]:
            empty_neighbors["В"] = (room_r, room_c + 1)

        for direction, (nr, nc) in empty_neighbors.items():
            if direction != chosen_direction:
                required_exit = {"С": "Ю", "Ю": "С", "З": "В", "В": "З"}[direction]
                possible_rooms = DEAD_END_TEMPLATES.get(required_exit, [])
                if possible_rooms:
                    room_template = random.choice(possible_rooms)
                    room_id = self._get_next_room_id(nr, nc)
                    new_room = Room(room_id, nr, nc, room_template["name"], room_template["blueprint"],
                                    room_template["exits"])
                    dungeon_document["rooms"][room_id] = new_room.__dict__

    def _endgame_scenario(self, dungeon_document, current_room):
        """ Запускает сценарий конца игры, добавляя финальные комнаты. """
        current_grid = dungeon_document["rooms"]
        room_r, room_c = current_room["room_r"], current_room["room_c"]

        empty_neighbors = {}
        if "С" in current_room["exits"] and f"room_{room_r - 1}_{room_c}" not in current_grid:
            empty_neighbors["С"] = (room_r - 1, room_c)
        if "Ю" in current_room["exits"] and f"room_{room_r + 1}_{room_c}" not in current_grid:
            empty_neighbors["Ю"] = (room_r + 1, room_c)
        if "З" in current_room["exits"] and f"room_{room_r}_{room_c - 1}" not in current_grid:
            empty_neighbors["З"] = (room_r, room_c - 1)
        if "В" in current_room["exits"] and f"room_{room_r}_{room_c + 1}" not in current_grid:
            empty_neighbors["В"] = (room_r, room_c + 1)

        for direction, (nr, nc) in empty_neighbors.items():
            if direction in current_room["exits"]:
                corridor_template = CORRIDOR_TEMPLATES["С"][0]
                corridor_id = self._get_next_room_id(nr, nc)
                corridor_room = Room(corridor_id, nr, nc, corridor_template["name"], corridor_template["blueprint"],
                                     corridor_template["exits"])
                dungeon_document["rooms"][corridor_id] = corridor_room.__dict__

                final_template = FINAL_ROOM_TEMPLATES[0]
                final_room_id = self._get_next_room_id(nr + (1 if direction == "Ю" else -1),
                                                       nc + (1 if direction == "В" else -1))
                final_room = Room(final_room_id, nr + (1 if direction == "Ю" else -1),
                                  nc + (1 if direction == "В" else -1), final_template["name"],
                                  final_template["blueprint"], final_template["exits"])
                dungeon_document["rooms"][final_room_id] = final_room.__dict__

    def handle_player_move(self, dungeon_document, player, key):
        """
        Основной метод, который обновляет подземелье на основе хода игрока.
        """
        current_room_id = dungeon_document["current_room_id"]
        current_room_data = dungeon_document["rooms"][current_room_id]

        prev_sub_r, prev_sub_c = player.sub_r, player.sub_c
        target_sub_r, target_sub_c = prev_sub_r, prev_sub_c

        move_direction = None
        if key in (pygame.K_UP, pygame.K_w):
            target_sub_r -= 1
            move_direction = "С"
        elif key in (pygame.K_DOWN, pygame.K_s):
            target_sub_r += 1
            move_direction = "Ю"
        elif key in (pygame.K_LEFT, pygame.K_a):
            target_sub_c -= 1
            move_direction = "З"
        elif key in (pygame.K_RIGHT, pygame.K_d):
            target_sub_c += 1
            move_direction = "В"
        else:
            return dungeon_document

        if 0 <= target_sub_r < 9 and 0 <= target_sub_c < 9:
            tile_key = f"{target_sub_r}_{target_sub_c}"
            if tile_key in current_room_data["grid"]:
                tile_type = current_room_data["grid"][tile_key]["type"]
                if tile_type != WALL:
                    player.move(target_sub_r, target_sub_c)
        else:
            current_exit_tile_key = f"{prev_sub_r}_{prev_sub_c}"
            if current_exit_tile_key in current_room_data["grid"] and current_room_data["grid"][current_exit_tile_key][
                "type"] == EXIT:
                new_room_r, new_room_c = player.r, player.c
                if move_direction == "С":
                    new_room_r -= 1
                    new_sub_r, new_sub_c = 8, 4
                elif move_direction == "Ю":
                    new_room_r += 1
                    new_sub_r, new_sub_c = 0, 4
                elif move_direction == "З":
                    new_room_c -= 1
                    new_sub_r, new_sub_c = 4, 8
                elif move_direction == "В":
                    new_room_c += 1
                    new_sub_r, new_sub_c = 4, 0

                target_room_id = None
                for r_id, r_data in dungeon_document["rooms"].items():
                    if r_data["room_r"] == new_room_r and r_data["room_c"] == new_room_c:
                        target_room_id = r_id
                        break

                if target_room_id:
                    target_room_data = dungeon_document["rooms"][target_room_id]
                    target_exit_tile_key = f"{new_sub_r}_{new_sub_c}"
                    if target_exit_tile_key in target_room_data["grid"] and \
                            target_room_data["grid"][target_exit_tile_key]["type"] == EXIT:
                        player.move(new_sub_r, new_sub_c, new_room_r, new_room_c)
                        dungeon_document["current_room_id"] = target_room_id

                        if dungeon_document["player_first_move"]:
                            self._seal_unchosen_paths(dungeon_document, current_room_id, move_direction)
                            dungeon_document["player_first_move"] = False

                        if target_room_id not in dungeon_document["dungeon_progress"]["visited_rooms"]:
                            dungeon_document["dungeon_progress"]["visited_rooms"].add(target_room_id)
                            steps = len(dungeon_document["dungeon_progress"]["visited_rooms"])

                            current_grid_size = len(dungeon_document["rooms"])
                            remaining_rooms = dungeon_document["dungeon_progress"]["max_rooms"] - current_grid_size
                            open_exits = self._get_open_exits(dungeon_document)

                            if remaining_rooms <= len(open_exits) and remaining_rooms > 0:
                                self._endgame_scenario(dungeon_document, target_room_data)
                            else:
                                self._generate_new_rooms(dungeon_document, target_room_data)

        return dungeon_document