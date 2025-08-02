import tkinter as tk
from tkinter import messagebox, ttk
from .base import BaseLeftPanel
from ...helpers import utils


class Rooms9x9Panel(BaseLeftPanel):
    def __init__(self, master, app, rooms_dict, blocks_dict, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master, app, rooms_dict, miniature_size, miniature_padding, font, frame_width)
        self.rooms = rooms_dict
        self.blocks = blocks_dict

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.notebook.bind("<Configure>", self.on_notebook_configure)

        self.draw_all_miniatures()

    def on_notebook_configure(self, event):
        container_width = event.width
        if container_width > 0:
            new_num_cols = max(1, container_width // (self.frame_width + self.miniature_padding * 2))

            if new_num_cols != self.num_miniature_cols:
                self.num_miniature_cols = new_num_cols
                self.draw_all_miniatures()

    def group_rooms_by_category(self):
        grouped_rooms = {}
        for name in sorted(self.rooms.keys()):
            parts = name.split('_')
            category = parts[1] if len(parts) > 1 else "other"
            if category not in grouped_rooms:
                grouped_rooms[category] = []
            grouped_rooms[category].append(name)
        return grouped_rooms

    def draw_all_miniatures(self):
        grouped_rooms = self.group_rooms_by_category()

        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        for category, room_names in grouped_rooms.items():
            tab_frame = tk.Frame(self.notebook, bg="#333333")
            self.notebook.add(tab_frame, text=category.capitalize())

            canvas = tk.Canvas(tab_frame, bg="#333333")
            scrollbar = tk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#333333")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            self._draw_miniatures_for_rooms(scrollable_frame, room_names)

    def _draw_miniatures_for_rooms(self, container_frame, room_names):
        for widget in container_frame.winfo_children():
            widget.destroy()

        if self.num_miniature_cols == 0:
            return

        for i, name in enumerate(room_names):
            row = i // self.num_miniature_cols
            col = i % self.num_miniature_cols

            miniature_frame = tk.Frame(container_frame, bg="#333333", borderwidth=1, relief="solid",
                                       width=self.frame_width, height=self.miniature_size + 20)
            miniature_frame.grid(row=row, column=col, padx=self.miniature_padding, pady=self.miniature_padding,
                                 sticky="n")
            miniature_frame.pack_propagate(False)

            room_canvas = tk.Canvas(miniature_frame, width=self.miniature_size, height=self.miniature_size,
                                    bg="#222222", highlightthickness=0)
            room_canvas.pack(pady=(5, 0))

            room_data = self.rooms[name]['structure']
            tile_colors = {1: "#888888", 0: "#000000", 2: "#ff0000", 3: "#ffff00", 4: "#00ff00"}

            block_tile_size = self.miniature_size // 3

            for room_row, room_cols in enumerate(room_data):
                for room_col, block_name in enumerate(room_cols):
                    block_data = self.blocks.get(block_name, self.blocks[utils.DEFAULT_BLOCK_NAME])
                    for r, row_values in enumerate(block_data):
                        for c, tile_value in enumerate(row_values):
                            x1 = (room_col * 3 + c) * (block_tile_size // 3)
                            y1 = (room_row * 3 + r) * (block_tile_size // 3)
                            x2 = x1 + (block_tile_size // 3)
                            y2 = y1 + (block_tile_size // 3)

                            fill_color = tile_colors.get(tile_value, "#888888")
                            room_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="")

            room_label = tk.Label(miniature_frame, text=name, fg="white", bg="#333333", font=self.font)
            room_label.pack()

            miniature_frame.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            room_canvas.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            room_label.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))

            miniature_frame.bind("<Enter>", lambda e, fr=miniature_frame: fr.config(bg="gray"))
            miniature_frame.bind("<Leave>", lambda e, fr=miniature_frame: fr.config(bg="#333333"))