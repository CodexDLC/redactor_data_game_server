import tkinter as tk
from tkinter import ttk


class RoomControls(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.config(bg="#333333")

        self.room_name_var = tk.StringVar(value="room_")
        self.room_type_var = tk.StringVar(value="corridor")
        self.exit_vars = {
            "N": tk.BooleanVar(value=False),
            "S": tk.BooleanVar(value=False),
            "W": tk.BooleanVar(value=False),
            "E": tk.BooleanVar(value=False)
        }

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Данные комнаты", fg="white", bg="#333333").pack(pady=10)

        tk.Label(self, text="Имя комнаты", fg="white", bg="#333333").pack()
        room_name_entry = tk.Entry(self, textvariable=self.room_name_var, bg="#444444", fg="white")
        room_name_entry.pack(fill=tk.X, padx=5, pady=2)

        tk.Label(self, text="Тип", fg="white", bg="#333333").pack(pady=(10, 0))
        room_type_frame = tk.Frame(self, bg="#333333")
        room_type_frame.pack()
        tk.Radiobutton(room_type_frame, text="Коридор", variable=self.room_type_var, value="corridor",
                       fg="white", bg="#333333", selectcolor="#333333", activebackground="#333333").pack(side=tk.LEFT)
        tk.Radiobutton(room_type_frame, text="Комната", variable=self.room_type_var, value="room",
                       fg="white", bg="#333333", selectcolor="#333333", activebackground="#333333").pack(side=tk.LEFT)

        tk.Label(self, text="Выходы", fg="white", bg="#333333").pack(pady=(10, 0))
        exits_frame = tk.Frame(self, bg="#333333")
        exits_frame.pack()

        tk.Checkbutton(exits_frame, text="С", variable=self.exit_vars["N"], fg="white", bg="#333333",
                       selectcolor="#333333").grid(row=0, column=1)
        tk.Checkbutton(exits_frame, text="З", variable=self.exit_vars["W"], fg="white", bg="#333333",
                       selectcolor="#333333").grid(row=1, column=0)
        tk.Checkbutton(exits_frame, text="В", variable=self.exit_vars["E"], fg="white", bg="#333333",
                       selectcolor="#333333").grid(row=1, column=2)
        tk.Checkbutton(exits_frame, text="Ю", variable=self.exit_vars["S"], fg="white", bg="#333333",
                       selectcolor="#333333").grid(row=2, column=1)

        control_buttons_frame = tk.Frame(self, bg="#333333")
        control_buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        tk.Button(control_buttons_frame, text="Сохранить комнату", bg="#444444", fg="white").pack(fill=tk.X, padx=5,
                                                                                                  pady=2)
        tk.Button(control_buttons_frame, text="Загрузить комнату", bg="#444444", fg="white").pack(fill=tk.X, padx=5,
                                                                                                  pady=2)
        tk.Button(control_buttons_frame, text="Удалить комнату", bg="#444444", fg="white").pack(fill=tk.X, padx=5,
                                                                                                pady=2)