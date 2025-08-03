# File: infrastructure/ui/tkinter_views/left_panel/palette_list_panel.py (version 0.2)
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
        node_palette_button = tk.Button(self, text="Палитра Нодов", bg="#444444", fg="white",
                                        command=lambda: self.open_palette("nodes"))
        node_palette_button.pack(fill=tk.X, padx=10, pady=2)

        # Кнопка для палитры блоков
        block_palette_button = tk.Button(self, text="Палитра Блоков", bg="#444444", fg="white",
                                         command=lambda: self.open_palette("blocks"))
        block_palette_button.pack(fill=tk.X, padx=10, pady=2)

        # Кнопка для палитры локаций (заглушка)
        location_palette_button = tk.Button(self, text="Палитра Локаций", bg="#444444", fg="white",
                                            command=lambda: self.open_palette("locations"))
        location_palette_button.pack(fill=tk.X, padx=10, pady=2)

    def open_palette(self, palette_type: str):
        if palette_type == "nodes":
            nodes_data = self.node_repo.get_all()
            FloatingPaletteWindow(self, title="Палитра Нодов", nodes_data=nodes_data)
        elif palette_type == "blocks":
            blocks_data = self.block_repo.get_all()
            # TODO: Реализовать логику для палитры блоков
            # FloatingPaletteWindow(self, title="Палитра Блоков", blocks_data=blocks_data)
            print("Палитра блоков пока не реализована")
        elif palette_type == "locations":
            locations_data = self.location_repo.get_all()
            # TODO: Реализовать логику для палитры локаций
            # FloatingPaletteWindow(self, title="Палитра Локаций", locations_data=locations_data)
            print("Палитра локаций пока не реализована")