# File: infrastructure/ui/tkinter_views/left_panel/locations.py (version 0.5)
import tkinter as tk
from tkinter import messagebox, ttk
from .base import BaseLeftPanel
from interfaces.persistence.i_location_repository import ILocationRepository
from interfaces.persistence.i_block_repository import IBlockRepository


class LocationsPanel(BaseLeftPanel):
    def __init__(self, master, app, location_repo: ILocationRepository, block_repo: IBlockRepository, miniature_size,
                 miniature_padding, font, frame_width):
        super().__init__(master, app, location_repo.get_all(), miniature_size, miniature_padding, font, frame_width)
        self.locations = self.blocks
        self.block_repo = block_repo

        tk.Label(self, text="Доступные локации", fg="white", bg="#333333").pack(pady=5)

        # --- Удаляем ttk.Notebook, так как он теперь в UniversalLeftPanel ---

        self.canvas = tk.Canvas(self, bg="#333333")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#333333")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.draw_all_miniatures()

    def on_notebook_configure(self, event):
        container_width = event.width
        if container_width > 0:
            new_num_cols = max(1, container_width // (self.frame_width + self.miniature_padding * 2))

            if new_num_cols != self.num_miniature_cols:
                self.num_miniature_cols = new_num_cols
                self.draw_all_miniatures()

    def group_locations_by_category(self):
        grouped_locations = {}
        for name in sorted(self.locations.keys()):
            parts = name.split('_')
            category = parts[1] if len(parts) > 1 else "other"
            if category not in grouped_locations:
                grouped_locations[category] = []
            grouped_locations[category].append(name)
        return grouped_locations

    def draw_all_miniatures(self):
        # Удаляем логику, связанную с Notebook
        grouped_locations = self.group_locations_by_category()
        all_location_names = [name for category, names in grouped_locations.items() for name in names]

        self._draw_miniatures_for_locations(self.scrollable_frame, all_location_names)

    def _draw_miniatures_for_locations(self, container_frame, location_names):
        for widget in container_frame.winfo_children():
            widget.destroy()

        if self.num_miniature_cols == 0:
            return

        for i, name in enumerate(location_names):
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

            room_data = self.locations[name]['structure']
            block_data_source = self.block_repo.get_all()
            tile_colors = {1: "#888888", 0: "#000000", 2: "#ff0000", 3: "#ffff00", 4: "#00ff00"}
            default_block_data = block_data_source.get("default", ((1, 1, 1), (1, 1, 1), (1, 1, 1)))

            block_tile_size = self.miniature_size // 3

            for room_row, room_cols in enumerate(room_data):
                for room_col, block_name in enumerate(room_cols):
                    block_data = block_data_source.get(block_name, default_block_data)
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