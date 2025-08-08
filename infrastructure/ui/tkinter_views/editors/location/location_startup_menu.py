# File: infrastructure/ui/tkinter_views/editors/location/location_startup_menu.py
import tkinter as tk
from tkinter import messagebox
from typing import Any, Optional, Tuple, Dict, Callable
# ИЗМЕНЕНИЕ: Убираем некорректный импорт BaseEditorControls
from ...styles import *


class LocationStartupMenu(tk.Toplevel):
    def __init__(self, master, app: Any, on_create_callback: Callable):
        super().__init__(master)
        self.app = app
        self.on_create_callback = on_create_callback

        self.title("Создание/Загрузка локации")
        self.config(bg=BG_PRIMARY, padx=10, pady=10)
        self.transient(master)
        self.grab_set()

        self._build_ui()

        self.update_idletasks()
        master_x = master.winfo_x()
        master_y = master.winfo_y()
        master_width = master.winfo_width()
        master_height = master.winfo_height()

        win_width = self.winfo_width()
        win_height = self.winfo_height()

        x = master_x + (master_width - win_width) // 2
        y = master_y + (master_height - win_height) // 2

        self.geometry(f'+{x}+{y}')

        self.wait_window(self)

    def _build_ui(self):
        main_frame = tk.LabelFrame(self, text="Новая локация", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Ключ локации:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.key_entry = tk.Entry(main_frame, bg=BG_SECONDARY, fg=FG_TEXT)
        self.key_entry.pack(fill=tk.X, pady=(0, 5))

        tk.Label(main_frame, text="Название:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.name_entry = tk.Entry(main_frame, bg=BG_SECONDARY, fg=FG_TEXT)
        self.name_entry.pack(fill=tk.X, pady=(0, 5))

        tk.Label(main_frame, text="Размеры (ширина x высота):", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        size_frame = tk.Frame(main_frame, bg=BG_PRIMARY)
        size_frame.pack(fill=tk.X)
        self.width_entry = tk.Entry(size_frame, width=5, bg=BG_SECONDARY, fg=FG_TEXT)
        self.width_entry.pack(side=tk.LEFT)
        tk.Label(size_frame, text="x", fg=FG_TEXT, bg=BG_PRIMARY).pack(side=tk.LEFT)
        self.height_entry = tk.Entry(size_frame, width=5, bg=BG_SECONDARY, fg=FG_TEXT)
        self.height_entry.pack(side=tk.LEFT)

        tk.Button(main_frame, text="Создать", command=self._on_create, bg=BG_SECONDARY, fg=FG_TEXT).pack(pady=10)

        tk.Label(self, text="или", fg=FG_TEXT, bg=BG_PRIMARY).pack(pady=5)

        tk.Button(self, text="Загрузить существующую", command=self._on_load, bg=BG_SECONDARY, fg=FG_TEXT).pack(
            fill=tk.X)

    def _on_create(self):
        key = self.key_entry.get().strip()
        name = self.name_entry.get().strip()
        width = self.width_entry.get().strip()
        height = self.height_entry.get().strip()

        if not key or not name or not width or not height:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.", parent=self)
            return

        try:
            width = int(width)
            height = int(height)
            if width % 3 != 0 or height % 3 != 0 or width <= 0 or height <= 0:
                messagebox.showerror("Ошибка", "Размеры должны быть положительными числами, кратными 3.", parent=self)
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Размеры должны быть числами.", parent=self)
            return

        self.on_create_callback(key, name, (width, height))
        self.destroy()

    def _on_load(self):
        self.app.set_status_message("Загрузка локации пока не реализована.", is_error=True)