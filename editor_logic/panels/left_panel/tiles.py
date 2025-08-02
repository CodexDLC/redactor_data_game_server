import tkinter as tk
from tkinter import messagebox
from .base import BaseLeftPanel
from ...helpers import utils


class Tiles1x1Panel(BaseLeftPanel):
    def __init__(self, master, app, blocks_dict, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master, app, blocks_dict, miniature_size, miniature_padding, font, frame_width)
        # Изменен порядок вызовов
        self.tiles = {} # Инициализируем атрибут перед вызовом
        self.load_tiles()
        self.draw_all_miniatures()

    def load_tiles(self):
        # Логика загрузки 1x1 тайлов из tiles.json (пока что пустой)
        self.tiles, message = utils.load_json_file(utils.TILES_JSON_FILE)
        if not self.tiles:
            messagebox.showinfo("Информация", message)
            self.tiles = {"tile_open": ((1,),), "tile_block": ((0,),)}
            utils.save_json_file(utils.TILES_JSON_FILE, self.tiles)

    def draw_all_miniatures(self):
        self.draw_miniatures_for_category(self, self.tiles.keys())

    def draw_miniatures_for_category(self, container_frame, tile_names):
        for widget in container_frame.winfo_children():
            widget.destroy()

        if self.num_miniature_cols == 0:
            return

        for i, name in enumerate(tile_names):
            row = i // self.num_miniature_cols
            col = i % self.num_miniature_cols

            miniature_frame = tk.Frame(container_frame, bg="#333333", borderwidth=1, relief="solid",
                                       width=self.frame_width, height=self.miniature_size + 20)
            miniature_frame.grid(row=row, column=col, padx=self.miniature_padding, pady=self.miniature_padding,
                                 sticky="n")
            miniature_frame.pack_propagate(False)

            block_canvas = tk.Canvas(miniature_frame, width=self.miniature_size, height=self.miniature_size,
                                     bg="#222222", highlightthickness=0)
            block_canvas.pack(pady=(5, 0))

            # Логика отрисовки 1x1 тайла
            tile_data = self.tiles[name][0][0]
            tile_colors = {1: "#888888", 0: "#000000"}  # Используем только цвета для 1x1
            fill_color = tile_colors.get(tile_data, "#888888")
            block_canvas.create_rectangle(0, 0, self.miniature_size, self.miniature_size, fill=fill_color, outline="")

            block_label = tk.Label(miniature_frame, text=name, fg="white", bg="#333333", font=self.font)
            block_label.pack()

            miniature_frame.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            block_canvas.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            block_label.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))

            miniature_frame.bind("<Enter>", lambda e, fr=miniature_frame: fr.config(bg="gray"))
            miniature_frame.bind("<Leave>", lambda e, fr=miniature_frame: fr.config(bg="#333333"))