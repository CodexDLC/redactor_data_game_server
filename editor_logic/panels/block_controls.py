import tkinter as tk
from tkinter import scrolledtext, messagebox


class BlockControls(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.config(bg="#333333")

        self.block_name_var = tk.StringVar(value="block_")
        self.cycle_mode_var = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        # Секция управления текущим блоком
        current_block_frame = tk.LabelFrame(self, text="Управление блоком", fg="white", bg="#333333")
        current_block_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(current_block_frame, text="Имя блока", fg="white", bg="#333333").pack(pady=5)
        self.block_name_entry = tk.Entry(current_block_frame, textvariable=self.block_name_var, bg="#444444",
                                         fg="white")
        self.block_name_entry.pack(fill=tk.X, padx=5, pady=2)

        save_load_frame = tk.Frame(current_block_frame, bg="#333333")
        save_load_frame.pack(fill=tk.X)
        tk.Button(save_load_frame, text="Сохранить", command=self.app.save_all_blocks, bg="#444444", fg="white").pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=5)
        tk.Button(save_load_frame, text="Загрузить", command=self.app.load_all_blocks, bg="#444444", fg="white").pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=5)

        # Секция доступных блоков
        available_blocks_frame = tk.LabelFrame(self, text="Доступные блоки", fg="white", bg="#333333")
        available_blocks_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.blocks_listbox = tk.Listbox(available_blocks_frame, bg="#444444", fg="white", height=10)
        self.blocks_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        self.blocks_listbox.bind("<<ListboxSelect>>", self.app.on_block_select)

        tk.Button(available_blocks_frame, text="Удалить блок", command=self.app.delete_selected_block, bg="#444444",
                  fg="white").pack(fill=tk.X, pady=5)

        # Секция опций
        options_frame = tk.LabelFrame(self, text="Опции", fg="white", bg="#333333")
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Checkbutton(options_frame, text="Режим цикла", variable=self.cycle_mode_var,
                       fg="white", bg="#333333", selectcolor="#333333", activebackground="#333333").pack(anchor=tk.W,
                                                                                                         pady=5, padx=2)