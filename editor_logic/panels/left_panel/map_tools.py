import tkinter as tk
from .base import BaseLeftPanel


class MapToolsPanel(BaseLeftPanel):
    def __init__(self, master, app, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master, app, {}, miniature_size, miniature_padding, font, frame_width)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Инструменты карты", fg="white", bg="#333333").pack(pady=5)

        add_frame = tk.LabelFrame(self, text="Расширение поля", fg="white", bg="#333333")
        add_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(add_frame, text="Добавить поле", bg="#444444", fg="white",
                  command=lambda: print("Добавить поле")).pack(pady=5, padx=5)