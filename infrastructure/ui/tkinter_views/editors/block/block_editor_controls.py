# File: infrastructure/ui/tkinter_views/editors/block/block_editor_controls.py
import tkinter as tk
from tkinter import scrolledtext
from typing import Any, Dict

from ...base_editor_controls import BaseEditorControls
from ...styles import *
from ...widgets.context_menu import add_editing_menu
from ...widgets.tag_input_widget import TagInputWidget


class BlockEditorControls(BaseEditorControls):
    """
    Простая панель управления для Редактора Блоков (Тайлов).
    Отображает ТОЛЬКО метаданные самого блока.
    """

    def __init__(self, master, parent_view: Any):
        # Объявляем переменные до вызова super(), который запускает _build_ui
        self.entry_block_key: tk.Entry | None = None
        self.entry_display_name: tk.Entry | None = None
        # --- ИСПРАВЛЕНО: Теперь используем TagInputWidget ---
        self.tag_input_widget: TagInputWidget | None = None
        self.exits_text_widget: scrolledtext.ScrolledText | None = None

        super().__init__(master, parent_view)

    def _build_ui(self):
        """Строит UI только для свойств самого блока."""
        main_frame = tk.LabelFrame(self, text="Свойства Тайла", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        main_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        tk.Label(main_frame, text="Ключ (block_key):", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.entry_block_key = tk.Entry(main_frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.entry_block_key.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_block_key)

        tk.Label(main_frame, text="Имя для UI:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.entry_display_name = tk.Entry(main_frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.entry_display_name.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_display_name)

        tk.Label(main_frame, text="Теги:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        # --- ИСПРАВЛЕНО: Теперь используем новый виджет ---
        self.tag_input_widget = TagInputWidget(main_frame, self.parent_view.app.tag_filter_service, "block_tags")
        self.tag_input_widget.pack(fill=tk.X, pady=(0, 5))

        self._create_exits_panel()

        super()._build_ui()

    def _create_exits_panel(self):
        """Создает и размещает панель для отображения связей нодов."""
        exits_frame = tk.LabelFrame(self, text="Связи нодов", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        exits_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, side=tk.TOP)

        self.exits_text_widget = scrolledtext.ScrolledText(exits_frame, bg=CODE_BG, fg=CODE_FG, font=CODE_FONT,
                                                           wrap=tk.WORD)
        self.exits_text_widget.pack(fill=tk.BOTH, expand=True)
        self.exits_text_widget.config(state=tk.DISABLED)

    def set_data(self, block_data: Dict[str, Any]):
        """Заполняет поля данными блока."""
        if self.entry_block_key:
            self.entry_block_key.delete(0, tk.END)
            self.entry_block_key.insert(0, block_data.get('block_key', ''))

        if self.entry_display_name:
            self.entry_display_name.delete(0, tk.END)
            self.entry_display_name.insert(0, block_data.get('display_name', ''))

        # --- ИСПРАВЛЕНО: Используем новый виджет для установки тегов ---
        if self.tag_input_widget:
            tags_list = block_data.get('tags', [])
            self.tag_input_widget.set_tags(tags_list)

        if self.exits_text_widget:
            self.set_exits_data(block_data.get('calculated_exits', {}))

    def set_exits_data(self, exits_data: Dict[str, Any]):
        """Отображает данные о связях в текстовом виджете."""
        if self.exits_text_widget:
            self.exits_text_widget.config(state=tk.NORMAL)
            self.exits_text_widget.delete('1.0', tk.END)
            if exits_data:
                for node_id, exits in exits_data.items():
                    self.exits_text_widget.insert(tk.END, f"Нод {node_id}:\n")
                    for direction, target_node in exits.items():
                        self.exits_text_widget.insert(tk.END, f"  - {direction}: {target_node}\n")
                    self.exits_text_widget.insert(tk.END, "\n")
            self.exits_text_widget.config(state=tk.DISABLED)

    def get_data(self) -> Dict[str, Any]:
        """Собирает данные из полей ввода."""
        # --- ИСПРАВЛЕНО: Получаем теги из нового виджета ---
        tags_list = self.tag_input_widget.get_tags() if self.tag_input_widget else []

        return {
            "block_key": self.entry_block_key.get() if self.entry_block_key else "",
            "display_name": self.entry_display_name.get() if self.entry_display_name else "",
            "tags": tags_list
        }