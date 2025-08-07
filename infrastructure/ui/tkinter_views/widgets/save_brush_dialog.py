# File: infrastructure/ui/tkinter_views/widgets/save_brush_dialog.py
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple

from ..styles import *
from .context_menu import add_editing_menu


class SaveBrushDialog(tk.Toplevel):
    """
    Простое модальное диалоговое окно для ввода ID и имени
    при сохранении новой кисточки (шаблона модуля).
    """

    def __init__(self, master, title: str = "Сохранить как кисточку"):
        super().__init__(master)
        self.title(title)
        self.transient(master)
        self.grab_set()

        self.config(bg=BG_PRIMARY, padx=10, pady=10)

        self.result: Optional[Tuple[str, str]] = None

        # ИЗМЕНЕНИЕ: Устанавливаем положение окна по центру
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

        # --- Виджеты ---
        tk.Label(self, text="Уникальный ключ (ID):", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.id_entry = tk.Entry(self, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.id_entry.pack(fill=tk.X, pady=(0, 10))
        add_editing_menu(self.id_entry)

        tk.Label(self, text="Название для меню:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.name_entry = tk.Entry(self, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        add_editing_menu(self.name_entry)

        # --- Кнопки ---
        button_frame = tk.Frame(self, bg=BG_PRIMARY)
        button_frame.pack(fill=tk.X)

        save_button = tk.Button(button_frame, text="Сохранить", command=self._on_save, bg=BG_SECONDARY, fg=FG_TEXT)
        save_button.pack(side=tk.RIGHT, padx=(5, 0))

        cancel_button = tk.Button(button_frame, text="Отмена", command=self._on_cancel, bg=BG_SECONDARY, fg=FG_TEXT)
        cancel_button.pack(side=tk.RIGHT)

        self.id_entry.focus_set()

        self.wait_window(self)

    def _on_save(self):
        """Обработчик нажатия кнопки 'Сохранить'."""
        template_id = self.id_entry.get().strip()
        display_name = self.name_entry.get().strip()

        if not template_id or not display_name:
            messagebox.showerror("Ошибка", "Оба поля должны быть заполнены.", parent=self)
            return

        self.result = (template_id, display_name)
        self.destroy()

    def _on_cancel(self):
        """Обработчик нажатия кнопки 'Отмена'."""
        self.result = None
        self.destroy()

    @staticmethod
    def ask(master) -> Optional[Tuple[str, str]]:
        dialog = SaveBrushDialog(master)
        return dialog.result