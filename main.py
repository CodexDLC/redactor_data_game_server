# main.py

import pygame, sys
import game_ui
from generator.generator import DungeonGenerator

# --- КОНСТАНТЫ ---
# Эти константы теперь определяют масштаб отрисовки, а не логику
SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 800, 800, 30
GRID_CELL_SIZE = 144
PLAYER_SIZE_PIXELS = (GRID_CELL_SIZE / 9) * 1.5

# --- Цвета ---
WHITE, PURPLE = (255, 255, 255), (160, 32, 240)
GRID_BG_COLOR, TILE_WALL_COLOR = (25, 25, 25), (50, 50, 50)
TILE_FLOOR_COLOR, TILE_EXIT_COLOR = (120, 120, 120), (200, 150, 50)

# Словарь для хранения констант и состояния
CONSTANTS = {
    "GRID_CELL_SIZE": GRID_CELL_SIZE, "FPS": FPS, "WHITE": WHITE, "PURPLE": PURPLE,
    "GRID_BG_COLOR": GRID_BG_COLOR, "TILE_WALL_COLOR": TILE_WALL_COLOR,
    "TILE_FLOOR_COLOR": TILE_FLOOR_COLOR, "TILE_EXIT_COLOR": TILE_EXIT_COLOR
}


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Архитектор Подземелий v3.0")
    clock = pygame.time.Clock()

    dungeon_generator = DungeonGenerator()
    dungeon_document = dungeon_generator.start_new_dungeon()

    # Создание игрока в центре комнаты (4, 4)
    start_room = dungeon_document["rooms"][dungeon_document["current_room_id"]]
    start_coords = (4, 4)  # Инициализируем игрока в центре
    player = game_ui.Player(start_coords[0], start_coords[1], start_room, PURPLE, PLAYER_SIZE_PIXELS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Обновление состояния игрока и подземелья через генератор
                dungeon_document = dungeon_generator.handle_player_move(dungeon_document, player, event.key)

        game_ui.draw_dungeon(screen, dungeon_document, player, CONSTANTS)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()