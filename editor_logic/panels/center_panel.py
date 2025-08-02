import tkinter as tk
from tkinter import ttk


class CenterPanel(tk.Frame):
    def __init__(self, master, grid_size, tile_size, draw_callback, click_callbacks, tile_controls_widget=None):
        super().__init__(master, bg="#333333")
        self.grid_size = grid_size
        self.tile_size = tile_size
        self.draw_callback = draw_callback
        self.click_callbacks = click_callbacks

        self.current_tile_size = self.tile_size
        self.grid_data = None
        self.tile_colors = None

        # Переносим Canvas в начало
        self.canvas = tk.Canvas(self,
                                width=self.grid_size * self.tile_size,
                                height=self.grid_size * self.tile_size,
                                bg="#222222",
                                highlightthickness=0)
        self.canvas.pack(expand=True, anchor="center")

        # Ползунок масштабирования
        zoom_frame = tk.Frame(self, bg="#333333")
        zoom_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)

        tk.Label(zoom_frame, text="Масштаб:", fg="white", bg="#333333").pack(side=tk.LEFT)
        self.zoom_scale = ttk.Scale(zoom_frame, from_=5, to=100, orient=tk.HORIZONTAL, command=self.on_zoom_scale)
        self.zoom_scale.set(self.tile_size)
        self.zoom_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Привязки событий после инициализации Canvas
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-2>", self.on_middle_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

    def on_zoom_scale(self, value):
        self.current_tile_size = int(float(value))
        self.update_canvas_size()

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.current_tile_size = min(100, self.current_tile_size + 5)
        else:
            self.current_tile_size = max(5, self.current_tile_size - 5)
        self.zoom_scale.set(self.current_tile_size)
        self.update_canvas_size()

    def update_canvas_size(self):
        new_width = self.grid_size * self.current_tile_size
        new_height = self.grid_size * self.current_tile_size
        self.canvas.config(width=new_width, height=new_height)
        self.draw_grid(self.grid_data, self.tile_colors)

    def draw_grid(self, grid_data, tile_colors):
        self.grid_data = grid_data
        self.tile_colors = tile_colors
        self.canvas.delete("all")
        if self.grid_data is None:
            return
        if self.draw_callback:
            self.draw_callback(self.canvas, self.grid_data, self.current_tile_size, self.tile_colors)

    def on_left_click(self, event):
        col = event.x // self.current_tile_size
        row = event.y // self.current_tile_size
        if self.click_callbacks.get("left"):
            self.click_callbacks["left"](row, col)

    def on_middle_click(self, event):
        col = event.x // self.current_tile_size
        row = event.y // self.current_tile_size
        if self.click_callbacks.get("middle"):
            self.click_callbacks["middle"](row, col)

    def on_right_click(self, event):
        col = event.x // self.current_tile_size
        row = event.y // self.current_tile_size
        if self.click_callbacks.get("right"):
            self.click_callbacks["right"](row, col)