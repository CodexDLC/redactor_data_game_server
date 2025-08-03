# File: infrastructure/ui/tkinter_views/left_panel/universal.py (version 1.0)
import tkinter as tk
from tkinter import ttk
from interfaces.persistence.i_node_repository import INodeRepository
from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.persistence.i_location_repository import ILocationRepository

from .nodes import NodesPanel
from .blocks import BlocksPanel
from .locations import LocationsPanel
from .map_tools import MapToolsPanel
from .palette_list_panel import PaletteListPanel


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

        self.setup_ui()
        self.show_panel("nodes")

    def setup_ui(self):
        self.main_paned_window = tk.PanedWindow(self, orient=tk.VERTICAL, sashrelief=tk.SUNKEN, bg="#333333")
        self.main_paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.bottom_pane = tk.Frame(self.main_paned_window, bg="#333333")
        self.main_paned_window.add(self.bottom_pane)

        self.bottom_buttons_frame = tk.LabelFrame(self.bottom_pane, text="Инструменты", fg="white", bg="#333333",
                                                  padx=5, pady=5)
        self.bottom_buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.bottom_content_frame = tk.LabelFrame(self.bottom_pane, text="Содержимое", fg="white", bg="#333333", padx=5,
                                                  pady=5)
        self.bottom_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.create_bottom_buttons()

        self.top_pane = tk.Frame(self.main_paned_window, bg="#333333")
        self.main_paned_window.add(self.top_pane)

        self.top_buttons_frame = tk.LabelFrame(self.top_pane, text="Режимы", fg="white", bg="#333333", padx=5, pady=5)
        self.top_buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.top_content_frame = tk.LabelFrame(self.top_pane, text="Коллекция", fg="white", bg="#333333", padx=5,
                                               pady=5)
        self.top_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.create_top_buttons()

        # --- НОВОЕ ИСПРАВЛЕНИЕ: Используем after для установки позиции ---
        self.main_paned_window.after(100, self._set_initial_sash_position)

    def _set_initial_sash_position(self):
        try:
            sash_position = self.main_paned_window.winfo_height() * 2 // 3
            self.main_paned_window.sash(0, 'place', 0, sash_position)
        except tk.TclError:
            # Если возникла ошибка, повторяем попытку
            self.main_paned_window.after(100, self._set_initial_sash_position)



    def create_top_buttons(self):
        self.nodes_button = tk.Button(self.top_buttons_frame, text="Nodes", command=lambda: self.show_panel("nodes"))
        self.blocks_button = tk.Button(self.top_buttons_frame, text="Blocks", command=lambda: self.show_panel("blocks"))
        self.locations_button = tk.Button(self.top_buttons_frame, text="Locations",
                                          command=lambda: self.show_panel("locations"))

        self.nodes_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.blocks_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.locations_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def create_bottom_buttons(self):
        self.palette_button = tk.Button(self.bottom_buttons_frame, text="Palette",
                                        command=lambda: self.show_panel("palette"))
        self.map_tools_button = tk.Button(self.bottom_buttons_frame, text="Map Tools",
                                          command=lambda: self.show_panel("map_tools"))

        self.palette_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.map_tools_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def show_panel(self, panel_name):
        # Меняем заголовок верхнего фрейма
        if panel_name == "nodes":
            self.top_content_frame.config(text="Ноды")
        elif panel_name == "blocks":
            self.top_content_frame.config(text="Блоки")
        elif panel_name == "locations":
            self.top_content_frame.config(text="Локации")

        # Меняем заголовок нижнего фрейма
        if panel_name == "palette":
            self.bottom_content_frame.config(text="Палитры")
        elif panel_name == "map_tools":
            self.bottom_content_frame.config(text="Инструменты карты")

        for widget in self.top_content_frame.winfo_children():
            widget.destroy()
        for widget in self.bottom_content_frame.winfo_children():
            widget.destroy()

        if panel_name == "nodes":
            self.nodes_panel = NodesPanel(self.top_content_frame, self.app, self.node_repo,
                                          self.miniature_size, self.miniature_padding,
                                          self.font, self.frame_width)
            self.nodes_panel.pack(fill=tk.BOTH, expand=True)
        elif panel_name == "blocks":
            self.blocks_panel = BlocksPanel(self.top_content_frame, self.app, self.block_repo,
                                            self.miniature_size, self.miniature_padding,
                                            self.font, self.frame_width)
            self.blocks_panel.pack(fill=tk.BOTH, expand=True)
        elif panel_name == "locations":
            self.locations_panel = LocationsPanel(self.top_content_frame, self.app,
                                                  self.location_repo, self.block_repo,
                                                  self.miniature_size, self.miniature_padding,
                                                  self.font, self.frame_width)
            self.locations_panel.pack(fill=tk.BOTH, expand=True)
        elif panel_name == "palette":
            self.palette_list_panel = PaletteListPanel(self.bottom_content_frame, self.app,
                                                       self.node_repo, self.block_repo,
                                                       self.location_repo)
            self.palette_list_panel.pack(fill=tk.BOTH, expand=True)
        elif panel_name == "map_tools":
            self.map_tools_panel = MapToolsPanel(self.bottom_content_frame, self.app,
                                                 self.miniature_size, self.miniature_padding,
                                                 self.font, self.frame_width)
            self.map_tools_panel.pack(fill=tk.BOTH, expand=True)

    def get_nodes_panel(self):
        return self.nodes_panel