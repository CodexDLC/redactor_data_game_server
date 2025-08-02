# game_ui.py

import pygame


# --- Класс Игрока ---
class Player:
    def __init__(self, sub_r, sub_c, current_room, color, size_in_pixels):
        self.sub_r, self.sub_c = sub_r, sub_c
        self.r, self.c = current_room["room_r"], current_room["room_c"]
        self.color = color
        self.size = size_in_pixels

    def move(self, new_sub_r, new_sub_c, new_room_r=None, new_room_c=None):
        self.sub_r, self.sub_c = new_sub_r, new_sub_c
        if new_room_r is not None and new_room_c is not None:
            self.r, self.c = new_room_r, new_room_c


# --- Отрисовка ---
def draw_dungeon(screen, dungeon_document, player, constants):
    screen.fill(constants['GRID_BG_COLOR'])

    GRID_CELL_SIZE = constants['GRID_CELL_SIZE']
    screen_center_x = screen.get_width() / 2
    screen_center_y = screen.get_height() / 2

    # Размер маленького тайла
    sub_cell_size = GRID_CELL_SIZE / 9.0

    # Смещение для центрирования на игроке
    offset_x = screen_center_x - (player.c * GRID_CELL_SIZE + player.sub_c * sub_cell_size + (sub_cell_size / 2))
    offset_y = screen_center_y - (player.r * GRID_CELL_SIZE + player.sub_r * sub_cell_size + (sub_cell_size / 2))

    # Отрисовка всех комнат
    for room_id, room_data in dungeon_document["rooms"].items():

        screen_x = room_data["room_c"] * GRID_CELL_SIZE + offset_x
        screen_y = room_data["room_r"] * GRID_CELL_SIZE + offset_y

        # Оптимизация: отрисовываем только видимые комнаты
        if screen_x + GRID_CELL_SIZE < 0 or screen_x > screen.get_width() or \
                screen_y + GRID_CELL_SIZE < 0 or screen_y > screen.get_height():
            continue

        for sub_r in range(9):
            for sub_c in range(9):
                tile_key = f"{sub_r}_{sub_c}"
                tile_data = room_data["grid"].get(tile_key)

                if not tile_data:
                    continue

                node_value = tile_data["type"]

                color = constants['TILE_WALL_COLOR']
                if node_value == 1:
                    color = constants['TILE_FLOOR_COLOR']
                elif node_value == 2:
                    color = constants['TILE_EXIT_COLOR']

                pygame.draw.rect(
                    screen, color,
                    (screen_x + sub_c * sub_cell_size,
                     screen_y + sub_r * sub_cell_size,
                     sub_cell_size + 1, sub_cell_size + 1)
                )

    # Рисуем игрока всегда в центре экрана
    pygame.draw.circle(screen, player.color, (screen_center_x, screen_center_y), player.size)

    # Отрисовка текста
    font = pygame.font.SysFont("arial", 24)
    visited_text = f"Посещено комнат: {len(dungeon_document['dungeon_progress']['visited_rooms'])}/{dungeon_document['dungeon_progress']['max_rooms']}"
    text_surface = font.render(f"WASD/Стрелки | {visited_text}", True, constants['WHITE'])
    screen.blit(text_surface, (10, 10))