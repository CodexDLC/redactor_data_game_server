# File: infrastructure/ui/tkinter_views/left_panel/palette_list_panel.py (version 0.3)
import tkinter as tk
from tkinter import ttk
from interfaces.persistence.i_node_repository import INodeRepository
from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.persistence.i_location_repository import ILocationRepository
from ..widgets.floating_palette import FloatingPaletteWindow


class PaletteListPanel(tk.Frame):
    def __init__(self, master, app, node_repo: INodeRepository, block_repo: IBlockRepository, location_repo: ILocationRepository):
        super().__init__(master, bg="#333333")
        self.app = app
        self.node_repo = node_repo
        self.block_repo = block_repo
        self.location_repo = location_repo

        self.create_widgets()

    def create_widgets(self):
        # --- Удален статический заголовок "Палитры:" ---

        # Кнопка для палитры нодов
        node_palette_button = tk.Button(self, text="Палитра Нодов", bg="#444444", fg="white")
        node_palette_button.pack(fill=tk.X, padx=10, pady=2)
        node_palette_button.bind("<Button-1>", lambda e: self.open_palette("nodes", e.x_root, e.y_root))

        # Кнопка для палитры блоков
        block_palette_button = tk.Button(self, text="Палитра Блоков", bg="#444444", fg="white")
        block_palette_button.pack(fill=tk.X, padx=10, pady=2)
        block_palette_button.bind("<Button-1>", lambda e: self.open_palette("blocks", e.x_root, e.y_root))

        # Кнопка для палитры локаций (заглушка)
        location_palette_button = tk.Button(self, text="Палитра Локаций", bg="#444444", fg="white")
        location_palette_button.pack(fill=tk.X, padx=10, pady=2)
        location_palette_button.bind("<Button-1>", lambda e: self.open_palette("locations", e.x_root, e.y_root))


    def open_palette(self, palette_type: str, x: int, y: int):
        if palette_type == "nodes":
            nodes_data = self.node_repo.get_all()
            # --- ИСПРАВЛЕНИЕ ЗДЕСЬ: Передаем координаты в палитру ---
            self.app.open_palette("nodes", x, y)
        elif palette_type == "blocks":
            blocks_data = self.block_repo.get_all()
            print("Палитра блоков пока не реализована")
        elif palette_type == "locations":
            locations_data = self.location_repo.get_all()
            print("Палитра локаций пока не реализована")