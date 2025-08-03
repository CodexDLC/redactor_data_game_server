# File: infrastructure/ui/tkinter_views/left_panel/nodes.py (version 0.7)
import tkinter as tk
from typing import Any, Callable

from .base import BaseLeftPanel
from interfaces.ui.i_nodes_panel_view import INodesPanelView
from interfaces.persistence.i_node_repository import INodeRepository
from ..widgets.floating_palette import FloatingPaletteWindow


class NodesPanel(BaseLeftPanel, INodesPanelView):
    def __init__(self, master, app, node_repo: INodeRepository, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master, app, {}, miniature_size, miniature_padding, font, frame_width)
        # --- ИСПРАВЛЕНИЕ: Добавляем строку для сохранения node_repo ---
        self.node_repo = node_repo

        tk.Label(self, text="Доступные ноды", fg="white", bg="#333333").pack(pady=5)

        self.main_frame = tk.Frame(self, bg="#333333")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._item_widgets = []
        self.selected_key = None
        self._selection_callback = None

        self.update_node_list()

    def update_node_list(self):
        """Запрашивает данные и перерисовывает кастомный список."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self._item_widgets = []

        all_nodes = self.node_repo.get_all()

        previously_selected_key = self.selected_key
        self.selected_key = None

        for name, data in sorted(all_nodes.items()):
            item_frame = tk.Frame(self.main_frame, bg="#333333")
            item_frame.pack(fill="x", pady=1)

            color_label = tk.Label(item_frame, bg=data.get("color", "#ff00ff"), width=2, text=" ")
            color_label.pack(side="left", padx=(2, 5))

            name_label = tk.Label(item_frame, text=name, fg="white", bg="#333333", anchor="w")
            name_label.pack(side="left", fill="x", expand=True)

            click_handler = lambda e, key=name, frame=item_frame: self._on_item_select(key, frame)
            item_frame.bind("<Button-1>", click_handler)
            color_label.bind("<Button-1>", click_handler)
            name_label.bind("<Button-1>", click_handler)

            self._item_widgets.append((name, item_frame))

            if name == previously_selected_key:
                self._on_item_select(name, item_frame)

    def _on_item_select(self, key, frame):
        for item_key, item_frame in self._item_widgets:
            original_color = self.node_repo.get_by_key(item_key).get("color", "#333333")
            color_label = item_frame.winfo_children()[0]
            name_label = item_frame.winfo_children()[1]

            item_frame.config(bg="#333333")
            name_label.config(bg="#333333")
            color_label.config(bg=original_color)

        frame.config(bg="#555555")
        frame.winfo_children()[1].config(bg="#555555")

        self.selected_key = key

        if self._selection_callback:
            self._selection_callback(None)

    def get_selected_node_key(self) -> str | None:
        return self.selected_key

    def bind_list_selection_command(self, command: Callable[[Any], None]) -> None:
        self._selection_callback = command