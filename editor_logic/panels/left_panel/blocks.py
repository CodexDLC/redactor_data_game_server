import tkinter as tk
from tkinter import messagebox, ttk
from .base import BaseLeftPanel
from ...helpers import utils


class Blocks3x3Panel(BaseLeftPanel):
    def __init__(self, master, app, blocks_dict, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master, app, blocks_dict, miniature_size, miniature_padding, font, frame_width)

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
        grouped_blocks = self.group_blocks_by_category()

        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        for category, block_names in grouped_blocks.items():
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

            self._draw_miniatures_in_grid(scrollable_frame, block_names)