# File: infrastructure/ui/tkinter_views/left_panel/map_tools.py (version 0.2)
import tkinter as tk
from .base import BaseLeftPanel


class MapToolsPanel(BaseLeftPanel):
    def __init__(self, master, app, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master, app, {}, miniature_size, miniature_padding, font, frame_width)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="map_tools", fg="white", bg="#333333").pack(pady=5)