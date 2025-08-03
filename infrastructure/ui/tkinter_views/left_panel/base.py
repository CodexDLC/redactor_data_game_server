# File: infrastructure/ui/tkinter_views/left_panel/base.py (version 0.4)
import tkinter as tk
from tkinter import ttk


class BaseLeftPanel(tk.Frame):
    def __init__(self, master, app, data_dict, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master)
        self.config(bg="#333333")
        self.app = app
        self.blocks = data_dict
        self.miniature_size = miniature_size
        self.miniature_padding = miniature_padding
        self.font = font
        self.frame_width = frame_width
        self.num_miniature_cols = 0
        self.selected_block_name = None

        # Перенос логики layout'а в дочерние классы.
        # Этот класс теперь предоставляет только общие атрибуты.

    def on_miniature_click(self, block_name):
        self.selected_block_name = block_name
        if hasattr(self.app, 'on_block_selected'):
            self.app.on_block_selected(block_name)