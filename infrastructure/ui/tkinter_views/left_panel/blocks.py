# File: infrastructure/ui/tkinter_views/left_panel/blocks.py
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, Any, List

from .base import BaseLeftPanel
from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.persistence.i_node_repository import INodeRepository


class BlocksPanel(BaseLeftPanel):
    def __init__(self, master, app, block_repo: IBlockRepository, node_repo: INodeRepository, miniature_size,
                 miniature_padding, font, frame_width):
        super().__init__(master, app, block_repo.get_all(), miniature_size, miniature_padding, font, frame_width)
        self.node_repo = node_repo
        self.blocks = self.blocks  # Эта строка теперь корректна, так как self.blocks уже содержит данные.

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

        self.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        container_width = event.width
        if container_width > 0:
            new_num_cols = max(1, container_width // (self.frame_width + self.miniature_padding * 2))
            if new_num_cols != self.num_miniature_cols:
                self.num_miniature_cols = new_num_cols
                self.draw_all_miniatures()

    def group_blocks_by_category(self) -> Dict[str, List[str]]:
        grouped_blocks = {}
        for name in sorted(self.blocks.keys()):
            category = "Все блоки"
            if category not in grouped_blocks:
                grouped_blocks[category] = []
            grouped_blocks[category].append(name)
        return grouped_blocks

    def draw_all_miniatures(self):
        grouped_blocks = self.group_blocks_by_category()
        all_block_names = [name for category, names in grouped_blocks.items() for name in names]
        self._draw_miniatures_in_grid(self.scrollable_frame, all_block_names)

    def _draw_miniatures_in_grid(self, container_frame, block_names):
        for widget in container_frame.winfo_children():
            widget.destroy()

        all_node_data = self.node_repo.get_all()

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
            nodes_structure = block_data.get('nodes_structure', [])
            nodes_data_map = block_data.get('nodes_data', {})

            if nodes_structure:
                block_size_cells = len(nodes_structure[0])
                tile_size = self.miniature_size // block_size_cells

                for r in range(block_size_cells):
                    for c in range(block_size_cells):
                        node_id = nodes_structure[r][c]
                        if node_id is not None:
                            node_template_key = nodes_data_map.get(str(node_id), {}).get('template_key')
                            node_color = all_node_data.get(node_template_key, {}).get('color', '#888888')
                        else:
                            node_color = '#000000'

                        x1 = c * tile_size
                        y1 = r * tile_size
                        x2 = x1 + tile_size
                        y2 = y1 + tile_size

                        block_canvas.create_rectangle(x1, y1, x2, y2, fill=node_color, outline="")

            block_label = tk.Label(miniature_frame, text=name, fg="white", bg="#333333", font=self.font)
            block_label.pack()

            miniature_frame.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            block_canvas.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            block_label.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))

            miniature_frame.bind("<Enter>", lambda e, fr=miniature_frame: fr.config(bg="gray"))
            miniature_frame.bind("<Leave>", lambda e, fr=miniature_frame: fr.config(bg="#333333"))