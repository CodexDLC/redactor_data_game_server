# File: infrastructure/ui/tkinter_views/block_editor_view.py
import tkinter as tk
from tkinter import ttk
from interfaces.ui.i_block_editor_view import IBlockEditorView


class BlockEditorView(tk.Frame, IBlockEditorView):
    def __init__(self, master):
        super().__init__(master, bg="#333333")
        self.master = master

        self.block_canvas = None
        self.entry_name = None
        self.entry_size = None
        self.save_button = None
        self.delete_button = None
        self.new_button = None

        self._setup_ui()

    def _setup_ui(self):
        # Фрейм для полей ввода и кнопок
        form_frame = tk.LabelFrame(self, text="Свойства блока", fg="white", bg="#333333", padx=10, pady=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        # Имя блока
        tk.Label(form_frame, text="Имя:", fg="white", bg="#333333").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_name = tk.Entry(form_frame, bg="#555555", fg="white", insertbackground="white")
        self.entry_name.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        # Размер блока
        tk.Label(form_frame, text="Размер:", fg="white", bg="#333333").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_size = tk.Entry(form_frame, bg="#555555", fg="white", insertbackground="white")
        self.entry_size.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        form_frame.grid_columnconfigure(1, weight=1)

        # Фрейм для кнопок
        button_frame = tk.Frame(self, bg="#333333")
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        self.new_button = tk.Button(button_frame, text="Новый", bg="#444444", fg="white")
        self.new_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.save_button = tk.Button(button_frame, text="Сохранить", bg="#444444", fg="white")
        self.save_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.delete_button = tk.Button(button_frame, text="Удалить", bg="#444444", fg="white")
        self.delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Канва для рисования блока
        self.block_canvas = tk.Canvas(self, bg="#222222", highlightthickness=0)
        self.block_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def set_form_data(self, data: dict) -> None:
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, data.get('name', ''))

        self.entry_size.delete(0, tk.END)
        self.entry_size.insert(0, data.get('size', ''))

    def get_form_data(self) -> dict:
        return {
            'name': self.entry_name.get(),
            'size': self.entry_size.get()
        }

    def clear_form(self) -> None:
        self.entry_name.delete(0, tk.END)
        self.entry_size.delete(0, tk.END)
        self.block_canvas.delete("all")

    def bind_save_command(self, command: Callable[[Any], None]) -> None:
        self.save_button.config(command=command)

    def bind_delete_command(self, command: Callable[[Any], None]) -> None:
        self.delete_button.config(command=command)

    def bind_new_command(self, command: Callable[[Any], None]) -> None:
        self.new_button.config(command=command)