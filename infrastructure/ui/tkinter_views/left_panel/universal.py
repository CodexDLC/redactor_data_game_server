# File: infrastructure/ui/tkinter_views/left_panel/universal.py
import tkinter as tk
from interfaces.persistence.i_node_repository import INodeRepository
from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.persistence.i_location_repository import ILocationRepository
from interfaces.persistence.i_module_repository import IModuleRepository

from .blocks import BlocksPanel
from .locations import ModulesPanel

from .map_tools import MapToolsPanel


class UniversalLeftPanel(tk.Frame):
    def __init__(self, master, app, node_repo: INodeRepository, block_repo: IBlockRepository,
                 location_repo: ILocationRepository, module_repo: IModuleRepository,
                 miniature_size, miniature_padding, font, frame_width):
        super().__init__(master, bg="#333333")
        self.app = app
        self.node_repo = node_repo
        self.block_repo = block_repo
        self.location_repo = location_repo
        self.module_repo = module_repo # --- ДОБАВЛЕНО: Репозиторий модулей ---
        self.miniature_size = miniature_size
        self.miniature_padding = miniature_padding
        self.font = font
        self.frame_width = frame_width

        self.blocks_panel = None
        self.modules_panel = None # --- ИСПРАВЛЕНО: Меняем название ---

        self.setup_ui()
        self.show_panel("blocks")

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
        self.blocks_button = tk.Button(self.top_buttons_frame, text="Тайлы (3x3)",
                                       command=lambda: self.show_panel("blocks"))
        self.modules_button = tk.Button(self.top_buttons_frame, text="Модули", # --- ИСПРАВЛЕНО: Меняем текст кнопки ---
                                          command=lambda: self.show_panel("modules")) # --- ИСПРАВЛЕНО: Меняем команду ---

        self.blocks_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.modules_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def show_panel(self, panel_name):
        for widget in self.top_content_frame.winfo_children():
            widget.destroy()

        if panel_name == "blocks":
            self.top_content_frame.config(text="Тайлы (3x3)")
            self.blocks_panel = BlocksPanel(self.top_content_frame, self.app, self.block_repo,
                                            self.miniature_size, self.miniature_padding,
                                            self.font, self.frame_width)
            self.blocks_panel.pack(fill=tk.BOTH, expand=True)

        elif panel_name == "modules": # --- ИСПРАВЛЕНО: Меняем имя панели ---
            self.top_content_frame.config(text="Модули")
            self.modules_panel = ModulesPanel(self.top_content_frame, self.app,
                                                  self.module_repo, self.block_repo, self.node_repo,
                                                  self.miniature_size, self.miniature_padding,
                                                  self.font, self.frame_width)
            self.modules_panel.pack(fill=tk.BOTH, expand=True)