# File: infrastructure/ui/tkinter_views/editors/block/block_editor_controls.py
import tkinter as tk
from typing import Any, Dict

from ...base_editor_controls import BaseEditorControls
from ...styles import *
from ...widgets.context_menu import add_editing_menu


class BlockEditorControls(BaseEditorControls):
    """
    Простая панель управления для Редактора Блоков (Тайлов).
    Отображает ТОЛЬКО метаданные самого блока.
    """

    def __init__(self, master, parent_view: Any):
        # Объявляем переменные до вызова super(), который запускает _build_ui
        self.entry_block_key: tk.Entry | None = None
        self.entry_display_name: tk.Entry | None = None
        self.entry_block_tags: tk.Entry | None = None

        super().__init__(master, parent_view)

    def _build_ui(self):
        """Строит UI только для свойств самого блока."""
        frame = tk.LabelFrame(self, text="Свойства Тайла", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        tk.Label(frame, text="Ключ (block_key):", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.entry_block_key = tk.Entry(frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.entry_block_key.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_block_key)

        tk.Label(frame, text="Имя для UI:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.entry_display_name = tk.Entry(frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.entry_display_name.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_display_name)

        tk.Label(frame, text="Теги (через запятую):", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.entry_block_tags = tk.Entry(frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.entry_block_tags.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_block_tags)

        # Вызываем родительский метод, чтобы создать кнопки "Сохранить", "Удалить" и т.д.
        super()._build_ui()

    def set_data(self, block_data: Dict[str, Any]):
        """Заполняет поля данными блока."""
        if self.entry_block_key:
            self.entry_block_key.delete(0, tk.END)
            self.entry_block_key.insert(0, block_data.get('block_key', ''))

        if self.entry_display_name:
            self.entry_display_name.delete(0, tk.END)
            self.entry_display_name.insert(0, block_data.get('display_name', ''))

        if self.entry_block_tags:
            tags_list = block_data.get('tags', [])
            tags_str = ', '.join(tags_list)
            self.entry_block_tags.delete(0, tk.END)
            self.entry_block_tags.insert(0, tags_str)

    def get_data(self) -> Dict[str, Any]:
        """Собирает данные из полей ввода."""
        tags_str = self.entry_block_tags.get().strip() if self.entry_block_tags else ""
        tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()] if tags_str else []

        return {
            "block_key": self.entry_block_key.get() if self.entry_block_key else "",
            "display_name": self.entry_display_name.get() if self.entry_display_name else "",
            "tags": tags_list
        }