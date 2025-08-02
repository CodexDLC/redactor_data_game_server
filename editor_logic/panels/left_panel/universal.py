import tkinter as tk
from tkinter import ttk
from .blocks import Blocks3x3Panel
from .rooms import Rooms9x9Panel
from .tiles import Tiles1x1Panel
from .map_tools import MapToolsPanel
from ...helpers import utils


class UniversalLeftPanel(tk.Frame):
    def __init__(self, master, app, blocks_dict, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master, bg="#333333")
        self.app = app
        self.blocks_dict = blocks_dict
        self.miniature_size = miniature_size
        self.miniature_padding = miniature_padding
        self.font = font
        self.frame_width = frame_width

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.create_tabs()

    def create_tabs(self):
        # Tab 1: 1x1 Tiles
        tiles_frame = tk.Frame(self.notebook, bg="#333333")
        self.notebook.add(tiles_frame, text="Тайлы 1x1")
        Tiles1x1Panel(tiles_frame, self.app, self.blocks_dict, self.miniature_size, self.miniature_padding, self.font,
                      self.frame_width).pack(fill=tk.BOTH, expand=True)

        # Tab 2: 3x3 Blocks
        blocks_frame = tk.Frame(self.notebook, bg="#333333")
        self.notebook.add(blocks_frame, text="Блоки 3x3")
        Blocks3x3Panel(blocks_frame, self.app, self.blocks_dict, self.miniature_size, self.miniature_padding, self.font,
                       self.frame_width).pack(fill=tk.BOTH, expand=True)

        # Tab 3: 9x9 Rooms
        rooms_frame = tk.Frame(self.notebook, bg="#333333")
        self.notebook.add(rooms_frame, text="Комнаты 9x9")
        Rooms9x9Panel(rooms_frame, self.app, {}, self.blocks_dict, self.miniature_size, self.miniature_padding,
                      self.font, self.frame_width).pack(fill=tk.BOTH, expand=True)

        # Tab 4: Map Tools
        map_tools_frame = tk.Frame(self.notebook, bg="#333333")
        self.notebook.add(map_tools_frame, text="Инструменты карты")
        MapToolsPanel(map_tools_frame, self.app, self.miniature_size, self.miniature_padding, self.font,
                      self.frame_width).pack(fill=tk.BOTH, expand=True)