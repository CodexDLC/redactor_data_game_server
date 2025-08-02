import tkinter as tk
from tkinter import Menu
from editor_logic.core.block_editor import BlockEditor
from editor_logic.core.room_editor import RoomEditor


class MapEditorApp:
    def __init__(self, root):
        print("DEBUG: Initializing MapEditorApp...")
        self.root = root
        self.root.title("Редактор Карт Подземелий")
        self.root.geometry("1200x800")

        self.main_frame = tk.Frame(self.root, bg="#333333")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.active_editor = None

        self.create_menu()
        self.show_mode_selection()

        self.root.bind("<Key>", self.on_global_key_press)
        print("DEBUG: MapEditorApp initialized.")

    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=self.root.quit)

        modes_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Режимы", menu=modes_menu)
        modes_menu.add_command(label="Конструктор блоков", command=self.show_block_editor)
        modes_menu.add_command(label="Конструктор комнат", command=self.show_room_editor)
        modes_menu.add_command(label="Генератор карты")

    def on_global_key_press(self, event):
        if self.active_editor and hasattr(self.active_editor, 'on_key_press'):
            self.active_editor.on_key_press(event)

    def show_mode_selection(self):
        print("DEBUG: Showing mode selection screen.")
        self.clear_main_frame()
        self.active_editor = None

        selection_frame = tk.Frame(self.main_frame, bg="#333333")
        selection_frame.pack(expand=True)

        tk.Label(selection_frame, text="Выберите режим работы:", fg="white", bg="#333333", font=("Helvetica", 16)).pack(
            pady=20)

        block_editor_button = tk.Button(selection_frame, text="Конструктор блоков", command=self.show_block_editor,
                                        font=("Helvetica", 14), width=30, height=2, bg="#444444", fg="white")
        block_editor_button.pack(pady=10)

        room_editor_button = tk.Button(selection_frame, text="Конструктор комнат", command=self.show_room_editor,
                                       font=("Helvetica", 14), width=30, height=2, bg="#444444", fg="white")
        room_editor_button.pack(pady=10)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_block_editor(self):
        print("DEBUG: Launching BlockEditor...")
        self.clear_main_frame()
        self.active_editor = BlockEditor(self.main_frame, self)
        self.active_editor.pack(fill=tk.BOTH, expand=True)
        print("DEBUG: BlockEditor launched.")

    def show_room_editor(self):
        print("DEBUG: Launching RoomEditor...")
        self.clear_main_frame()
        self.active_editor = RoomEditor(self.main_frame, self)
        self.active_editor.pack(fill=tk.BOTH, expand=True)
        print("DEBUG: RoomEditor launched.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MapEditorApp(root)
    root.mainloop()