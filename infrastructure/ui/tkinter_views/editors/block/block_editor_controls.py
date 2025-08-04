import tkinter as tk
from tkinter import ttk
from typing import Any, Callable
from ...widgets.code_preview_window import CodePreviewWindow
from ...widgets.context_menu import add_editing_menu # <-- Заменено на новую функцию
from ...base_editor_controls import BaseEditorControls


class BlockEditorControls(BaseEditorControls):
    """
    Панель управления для редактора блоков.
    """

    def __init__(self, master, parent_view: Any):
        self._code_preview_window = None
        super().__init__(master, parent_view)

    def _build_ui(self):
        # --- Зона 1: Основные Свойства Блока ---
        main_props_frame = tk.LabelFrame(self, text="Основные свойства", fg="white", bg="#333333", padx=5, pady=5)
        main_props_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        tk.Label(main_props_frame, text="Ключ блока (block_key):", fg="white", bg="#333333").pack(anchor="w")
        self.entry_block_key = tk.Entry(main_props_frame, bg="#444444", fg="white")
        self.entry_block_key.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_block_key) # <-- Обновлено

        tk.Label(main_props_frame, text="Имя для UI:", fg="white", bg="#333333").pack(anchor="w")
        self.entry_display_name = tk.Entry(main_props_frame, bg="#444444", fg="white")
        self.entry_display_name.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_display_name) # <-- Обновлено

        # --- Зона 2: Настраиваемые Свойства Нода ---
        self.custom_props_frame = tk.LabelFrame(self, text="Настраиваемые свойства", fg="white", bg="#333333", padx=5,
                                                pady=5)
        self.custom_props_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(self.custom_props_frame, text="ID нода:", fg="white", bg="#333333").pack(anchor="w")
        self.entry_node_id = tk.Entry(self.custom_props_frame, bg="#444444", fg="white", state='readonly')
        self.entry_node_id.pack(fill=tk.X, pady=(0, 5))

        # TODO: Логика загрузки настраиваемых свойств из схемы

        # Вызываем родительский метод для создания общих кнопок
        super()._build_ui()

    def _show_code_preview(self):
        """Открывает или обновляет окно с кодом данных блока."""
        data = self.parent_view.get_form_data()

        if self._code_preview_window and self._code_preview_window.winfo_exists():
            self._code_preview_window.update_content(data)
            self._code_preview_window.lift()  # Поднимаем окно наверх
        else:
            self._code_preview_window = CodePreviewWindow(self.parent_view, data, "Код данных блока")

    def clear_custom_properties(self):
        """Очищает панель настраиваемых свойств."""
        # TODO: Обновить эту логику
        self.set_selected_node_id(None)

    def display_node_properties(self, node_data: dict):
        """Динамически отображает свойства нода."""
        # TODO: Реализовать логику для динамических полей
        pass

    def set_selected_node_id(self, node_id: str | None):
        """Обновляет нередактируемое поле с ID нода."""
        self.entry_node_id.config(state='normal')
        self.entry_node_id.delete(0, tk.END)
        if node_id:
            self.entry_node_id.insert(0, node_id)
        self.entry_node_id.config(state='readonly')

    def bind_show_code_command(self, command: Callable[[Any], None]) -> None:
        self.show_code_button.config(command=self._show_code_preview)