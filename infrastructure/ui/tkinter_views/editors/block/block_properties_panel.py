# File: infrastructure/ui/tkinter_views/editors/block/block_properties_panel.py
import tkinter as tk
from typing import Any, Dict

from ..base_properties_panel import BasePropertiesPanel
from ...styles import *
from ...widgets.context_menu import add_editing_menu
from ...widgets.tag_input_widget import TagInputWidget
from .block_gallery_panel import BlockGalleryPanel


class BlockPropertiesPanel(BasePropertiesPanel):
    """
    Панель свойств для Редактора Блоков.
    Отображает метаданные самого блока (ключ, имя, теги) и галерею всех блоков.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, app)
        self.service: Any | None = None

        # --- Атрибуты для виджетов ---
        self.entry_block_key: tk.Entry | None = None
        self.entry_display_name: tk.Entry | None = None
        self.tag_input_widget: TagInputWidget | None = None
        self.block_gallery_panel: BlockGalleryPanel | None = None

        self._build_ui()

    def _build_ui(self):
        """Строит UI для отображения свойств блока."""
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
        self.tag_input_widget = TagInputWidget(main_frame, self.app.tag_filter_service, "block_tags")
        self.tag_input_widget.pack(fill=tk.X, pady=(0, 5))

        # ИЗМЕНЕНИЕ: Убрали self.service из вызова
        self.block_gallery_panel = BlockGalleryPanel(self, self.app)
        self.block_gallery_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, side=tk.TOP)

    def set_service(self, service: Any):
        """
        Метод для передачи сервиса после инициализации.
        """
        self.service = service
        if self.block_gallery_panel:
            self.block_gallery_panel.set_service(service)

    def set_data(self, block_data: Dict[str, Any]):
        """Заполняет поля данными блока."""
        if self.entry_block_key:
            self.entry_block_key.delete(0, tk.END)
            self.entry_block_key.insert(0, block_data.get('block_key', ''))

        if self.entry_display_name:
            self.entry_display_name.delete(0, tk.END)
            self.entry_display_name.insert(0, block_data.get('display_name', ''))

        if self.tag_input_widget:
            tags_list = block_data.get('tags', [])
            self.tag_input_widget.set_tags(tags_list)

        if self.block_gallery_panel:
            self.block_gallery_panel.draw_all_miniatures()

    def get_data(self) -> Dict[str, Any]:
        """Собирает данные из полей ввода."""
        tags_list = self.tag_input_widget.get_tags() if self.tag_input_widget else []

        return {
            "block_key": self.entry_block_key.get() if self.entry_block_key else "",
            "display_name": self.entry_display_name.get() if self.entry_display_name else "",
            "tags": tags_list
        }