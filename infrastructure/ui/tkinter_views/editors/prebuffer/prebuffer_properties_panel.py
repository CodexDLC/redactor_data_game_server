# File: infrastructure/ui/tkinter_views/editors/prebuffer/prebuffer_properties_panel.py
import tkinter as tk
from typing import Any, Dict

from .prebuffer_gallery_panel import PrebufferGalleryPanel
from ..base_properties_panel import BasePropertiesPanel
from ...styles import *
from ...widgets.context_menu import add_editing_menu
from ...widgets.tag_input_widget import TagInputWidget


class PrebufferPropertiesPanel(BasePropertiesPanel):
    """
    Панель свойств для Редактора Пре-буферов.
    Содержит метаданные и галерею существующих пре-буферов.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, app)
        self.service: Any | None = None
        self.tag_input_widget: TagInputWidget | None = None
        self.prebuffer_gallery_panel: PrebufferGalleryPanel | None = None
        self.entry_prebuffer_key: tk.Entry | None = None
        self.entry_display_name: tk.Entry | None = None
        self._build_ui()

    def _build_ui(self):
        main_frame = tk.LabelFrame(self, text="Свойства Пре-буфера", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        main_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)

        tk.Label(main_frame, text="Ключ (prebuffer_key):", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.entry_prebuffer_key = tk.Entry(main_frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.entry_prebuffer_key.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_prebuffer_key)

        tk.Label(main_frame, text="Имя для UI:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.entry_display_name = tk.Entry(main_frame, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.entry_display_name.pack(fill=tk.X, pady=(0, 5))
        add_editing_menu(self.entry_display_name)

        tk.Label(main_frame, text="Теги:", fg=FG_TEXT, bg=BG_PRIMARY).pack(anchor="w")
        self.tag_input_widget = TagInputWidget(main_frame, self.app.tag_filter_service, "prebuffer_tags")
        self.tag_input_widget.pack(fill=tk.X, pady=(0, 5))

        # НОВОЕ: Панель галереи для предпросмотра существующих пре-буферов
        self.prebuffer_gallery_panel = PrebufferGalleryPanel(self, self.app)
        self.prebuffer_gallery_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, side=tk.TOP)

    def set_service(self, service: Any):
        self.service = service
        if self.prebuffer_gallery_panel:
            self.prebuffer_gallery_panel.set_service(service)

    def set_data(self, prebuffer_data: Dict[str, Any]):
        if self.entry_prebuffer_key:
            self.entry_prebuffer_key.delete(0, tk.END)
            self.entry_prebuffer_key.insert(0, prebuffer_data.get('prebuffer_key', ''))

        if self.entry_display_name:
            self.entry_display_name.delete(0, tk.END)
            self.entry_display_name.insert(0, prebuffer_data.get('display_name', ''))

        if self.tag_input_widget:
            self.tag_input_widget.set_tags(prebuffer_data.get('tags', []))

        if self.prebuffer_gallery_panel:
            self.prebuffer_gallery_panel.draw_all_miniatures()

    def get_data(self) -> Dict[str, Any]:
        tags_list = self.tag_input_widget.get_tags() if self.tag_input_widget else []
        return {
            "prebuffer_key": self.entry_prebuffer_key.get() if self.entry_prebuffer_key else "",
            "display_name": self.entry_display_name.get() if self.entry_display_name else "",
            "tags": tags_list
        }