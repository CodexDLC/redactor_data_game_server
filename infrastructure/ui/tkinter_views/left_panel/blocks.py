# File: infrastructure/ui/tkinter_views/left_panel/blocks.py (version 0.5)
import tkinter as tk
from tkinter import messagebox, ttk
from .base import BaseLeftPanel
from interfaces.persistence.i_block_repository import IBlockRepository


class BlocksPanel(BaseLeftPanel):
    def __init__(self, master, app, block_repo: IBlockRepository, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master, app, block_repo.get_all(), miniature_size, miniature_padding, font, frame_width)

        tk.Label(self, text="Доступные блоки", fg="white", bg="#333333").pack(pady=5)

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

    def group_blocks_by_category(self):
        grouped_blocks = {}
        for name in sorted(self.blocks.keys()):
            parts = name.split('_')
            category = parts[1] if len(parts) > 1 else "other"
            if category not in grouped_blocks:
                grouped_blocks[category] = []
            grouped_blocks[category].append(name)
        return grouped_blocks

    def draw_all_miniatures(self):
        # Исправленная логика: все миниатюры отрисовываются в одной прокручиваемой области
        grouped_blocks = self.group_blocks_by_category()
        all_block_names = [name for category, names in grouped_blocks.items() for name in names]
        self._draw_miniatures_in_grid(self.scrollable_frame, all_block_names)

    def _draw_miniatures_in_grid(self, container_frame, block_names):
        for widget in container_frame.winfo_children():
            widget.destroy()

        if self.num_miniature_cols == 0:
            return

        for i, name in enumerate(block_names):
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

            block_data = self.blocks[name]
            block_size = len(block_data)

            tile_colors = {1: "#7f7f7f", 0: "#000000", 2: "#ff0000", 3: "#ffff00"}

            for r in range(block_size):
                for c in range(block_size):
                    tile_x1 = c * (self.miniature_size // block_size)
                    tile_y1 = r * (self.miniature_size // block_size)
                    tile_x2 = tile_x1 + (self.miniature_size // block_size)
                    tile_y2 = tile_y1 + (self.miniature_size // block_size)

                    fill_color = tile_colors.get(block_data[r][c], "#7f7f7f")
                    block_canvas.create_rectangle(tile_x1, tile_y1, tile_x2, tile_y2, fill=fill_color, outline="")

            block_label = tk.Label(miniature_frame, text=name, fg="white", bg="#333333", font=self.font)
            block_label.pack()

            miniature_frame.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            block_canvas.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            block_label.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))

            miniature_frame.bind("<Enter>", lambda e, fr=miniature_frame: fr.config(bg="gray"))
            miniature_frame.bind("<Leave>", lambda e, fr=miniature_frame: fr.config(bg="#333333"))