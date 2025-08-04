# File: infrastructure/ui/tkinter_views/left_panel/universal.py (version 1.5)
import tkinter as tk
from interfaces.persistence.i_node_repository import INodeRepository
from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.persistence.i_location_repository import ILocationRepository

from .nodes import NodesPanel
from .blocks import BlocksPanel
from .locations import LocationsPanel
from .map_tools import MapToolsPanel
from .palette_list_panel import PaletteListPanel
from typing import Any, Optional


class UniversalLeftPanel(tk.Frame):
    def __init__(self, master, app, node_repo: INodeRepository, block_repo: IBlockRepository,
                 location_repo: ILocationRepository, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master, bg="#333333")
        self.app = app
        self.node_repo = node_repo
        self.block_repo = block_repo
        self.location_repo = location_repo
        self.miniature_size = miniature_size
        self.miniature_padding = miniature_padding
        self.font = font
        self.frame_width = frame_width

        self.nodes_panel = None
        self.blocks_panel = None
        self.locations_panel = None
        self.map_tools_panel = None
        self.palette_list_panel = None

        self.block_editor_service = None

        self.setup_ui()
        self.show_panel("nodes")

    def setup_ui(self):
        self.top_pane = tk.Frame(self, bg="#333333")
        self.top_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.top_buttons_frame = tk.LabelFrame(self.top_pane, text="Режимы", fg="white", bg="#333333", padx=5, pady=5)
        self.top_buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.top_content_frame = tk.LabelFrame(self.top_pane, text="Коллекция", fg="white", bg="#333333", padx=5,
                                               pady=5)
        self.top_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.create_top_buttons()

    def create_top_buttons(self):
        self.nodes_button = tk.Button(self.top_buttons_frame, text="Nodes", command=lambda: self.show_panel("nodes"))
        self.blocks_button = tk.Button(self.top_buttons_frame, text="Blocks", command=lambda: self.show_panel("blocks"))
        self.locations_button = tk.Button(self.top_buttons_frame, text="Locations",
                                          command=lambda: self.show_panel("locations"))

        self.nodes_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.blocks_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.locations_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def show_panel(self, panel_name):
        if panel_name == "nodes":
            self.top_content_frame.config(text="Ноды")
            for widget in self.top_content_frame.winfo_children():
                widget.destroy()
            self.nodes_panel = NodesPanel(self.top_content_frame, self.app, self.node_repo,
                                          self.miniature_size, self.miniature_padding,
                                          self.font, self.frame_width)
            self.nodes_panel.pack(fill=tk.BOTH, expand=True)
        elif panel_name == "blocks":
            self.top_content_frame.config(text="Блоки")
            for widget in self.top_content_frame.winfo_children():
                widget.destroy()
            self.blocks_panel = BlocksPanel(self.top_content_frame, self.app, self.block_repo,
                                            self.miniature_size, self.miniature_padding,
                                            self.font, self.frame_width)
            self.blocks_panel.pack(fill=tk.BOTH, expand=True)
        elif panel_name == "locations":
            self.top_content_frame.config(text="Локации")
            for widget in self.top_content_frame.winfo_children():
                widget.destroy()
            self.locations_panel = LocationsPanel(self.top_content_frame, self.app,
                                                  self.location_repo, self.block_repo,
                                                  self.miniature_size, self.miniature_padding,
                                                  self.font, self.frame_width)
            self.locations_panel.pack(fill=tk.BOTH, expand=True)
        elif panel_name == "palette":
            # Эта часть логики теперь недоступна из-за удаления кнопок, но оставлена как заглушка
            pass
        elif panel_name == "map_tools":
            # Эта часть логики теперь недоступна из-за удаления кнопок, но оставлена как заглушка
            pass

    def get_nodes_panel(self):
        return self.nodes_panel