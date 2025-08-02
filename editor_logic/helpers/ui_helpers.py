import tkinter as tk
from tkinter import ttk


def create_button_style(master):
    style = ttk.Style(master)
    style.configure("TButton",
                    background="#444444",
                    foreground="white",
                    font=("Helvetica", 12),
                    borderwidth=1)
    style.map("TButton",
              background=[('active', '#555555')])
    return style