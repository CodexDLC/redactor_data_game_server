import tkinter as tk
from map_editor_app import MapEditorApp


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Главное Меню")
        self.geometry("1200x800")
        self.config(bg="#333333")

        self._container = tk.Frame(self)
        self._container.pack(fill="both", expand=True)

        self._current_frame = None
        self.show_main_menu()

    def switch_frame(self, frame_class):
        """Уничтожает старый фрейм и показывает новый."""
        if self._current_frame:
            self._current_frame.destroy()

        # Передаем контейнер в качестве родителя для нового фрейма
        self._current_frame = frame_class(self._container)
        self._current_frame.pack(fill="both", expand=True)

    def show_main_menu(self):
        """Показывает главный экран с выбором редакторов."""
        self.switch_frame(MainMenuFrame)

    def show_map_editor(self):
        """Показывает редактор карт."""
        self.switch_frame(MapEditorApp)


class MainMenuFrame(tk.Frame):
    """Фрейм для главного меню."""

    def __init__(self, master):
        super().__init__(master, bg="#333333")

        app_controller = master.master  # Получаем доступ к MainApplication

        tk.Label(self, text="Выберите редактор:", font=("Helvetica", 16), fg="white", bg="#333333").pack(pady=20)

        tk.Button(self, text="Редактор Карт", command=app_controller.show_map_editor, font=("Helvetica", 14),
                  width=30, height=2, bg="#444444", fg="white").pack(pady=10)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()