import tkinter as tk
from tkinter import ttk


class BaseEditor(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.three_panel_layout()

    def three_panel_layout(self):
        self.main_paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, bg="#333333")
        self.main_paned_window.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_paned_window, bg="#333333")
        self.main_paned_window.add(self.left_frame, minsize=200)

        self.center_frame = tk.Frame(self.main_paned_window, bg="#333333")
        self.main_paned_window.add(self.center_frame, stretch="always")

        self.right_frame = tk.Frame(self.main_paned_window, bg="#333333")
        self.main_paned_window.add(self.right_frame, minsize=200)