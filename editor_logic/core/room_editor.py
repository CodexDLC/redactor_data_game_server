import tkinter as tk
from tkinter import messagebox
from ..core.base_editor import BaseEditor
from editor_logic.panels.left_panel.base import BaseLeftPanel
from ..panels.room_controls import RoomControls
from ..panels.center_panel import CenterPanel
from ..helpers import utils


class RoomEditor(BaseEditor):
    def __init__(self, master, app):
        super().__init__(master, app)  # Удалены weights
        self.grid_size = 9
        self.tile_size = 25
        self.block_size = 3

        self.blocks = {}
        self.load_available_blocks()

        self.room_data = [[utils.DEFAULT_BLOCK_NAME for _ in range(self.grid_size // self.block_size)]
                          for _ in range(self.grid_size // self.block_size)]

        self.miniature_size = 50
        self.miniature_padding = 5

        self.font = ("Helvetica", 10)
        self.longest_block_name = self.get_longest_block_name()
        self.text_width_estimate = self.get_text_width(self.longest_block_name)
        self.frame_width = self.text_width_estimate + 10

        self.tile_colors = {
            1: "#7f7f7f",  # FLOOR
            0: "#000000",  # WALL (Черный)
            2: "#ffcc00"  # EXIT
        }

        self.selected_block_name = None

        self.left_panel = BaseLeftPanel(self.left_frame, self, self.blocks, self.miniature_size, self.miniature_padding,
                                        self.font, self.frame_width)
        self.left_panel.pack(fill=tk.BOTH, expand=True)

        self.center_panel = CenterPanel(self.center_frame, self.grid_size, self.tile_size, self.draw_callback,
                                        self.click_callbacks)
        self.center_panel.pack(fill=tk.BOTH, expand=True)

        self.controls = RoomControls(self.right_frame, self)
        self.controls.pack(fill=tk.BOTH, expand=True)

        self.draw_grid()

    @property
    def click_callbacks(self):
        return {
            "left": self.on_left_click,
            "right": self.on_right_click
        }

    def draw_callback(self, canvas, grid_data, tile_size, tile_colors):
        for room_row in range(self.grid_size // self.block_size):
            for room_col in range(self.grid_size // self.block_size):
                block_name = self.room_data[room_row][room_col]
                block_data = self.blocks.get(block_name, self.blocks[utils.DEFAULT_BLOCK_NAME])

                for row in range(self.block_size):
                    for col in range(self.block_size):
                        x1 = (room_col * self.block_size + col) * tile_size
                        y1 = (room_row * self.block_size + row) * tile_size
                        x2 = x1 + tile_size
                        y2 = y1 + tile_size

                        fill_color = self.get_tile_color(block_data[row][col])
                        canvas.create_rectangle(x1, y1, x2, y2, outline="#444444", fill=fill_color)

    def draw_grid(self):
        self.center_panel.draw_grid(self.room_data, self.tile_colors)

    def load_available_blocks(self):
        self.blocks, message = utils.load_blocks_from_json()
        if not self.blocks:
            messagebox.showinfo("Информация", message)
            self.blocks = {utils.DEFAULT_BLOCK_NAME: ((1, 1, 1), (1, 1, 1), (1, 1, 1))}
            utils.save_blocks_to_json(self.blocks)

        if utils.DEFAULT_BLOCK_NAME not in self.blocks:
            self.blocks[utils.DEFAULT_BLOCK_NAME] = ((1, 1, 1), (1, 1, 1), (1, 1, 1))

    def on_left_click(self, row, col):
        if self.left_panel.selected_block_name:
            room_col = col // self.block_size
            room_row = row // self.block_size

            if 0 <= room_row < 3 and 0 <= room_col < 3:
                self.room_data[room_row][room_col] = self.left_panel.selected_block_name
                self.draw_grid()

    def on_right_click(self, row, col):
        room_col = col // self.block_size
        room_row = row // self.block_size

        if 0 <= room_row < 3 and 0 <= room_col < 3:
            self.room_data[room_row][room_col] = utils.DEFAULT_BLOCK_NAME
            self.draw_grid()

    def on_block_selected(self, block_name):
        self.selected_block_name = block_name

    def get_longest_block_name(self):
        if not self.blocks:
            return utils.DEFAULT_BLOCK_NAME
        return max(self.blocks.keys(), key=len)

    def get_text_width(self, text):
        temp_label = tk.Label(self, text=text, font=self.font)
        width = temp_label.winfo_reqwidth()
        temp_label.destroy()
        return width

    def get_tile_color(self, tile_value):
        colors = {
            1: "#7f7f7f",  # FLOOR
            0: "#000000",  # WALL (Черный)
            2: "#ffcc00"  # EXIT
        }
        return colors.get(tile_value, "#7f7f7f")