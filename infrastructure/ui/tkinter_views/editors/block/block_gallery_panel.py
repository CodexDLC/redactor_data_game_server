# File: infrastructure/ui/tkinter_views/editors/block/block_gallery_panel.py
import tkinter as tk
from typing import Any, Dict, List
from ..base_properties_panel import BasePropertiesPanel
from ...styles import *
from ...widgets.tag_input_widget import TagInputWidget


class BlockGalleryPanel(BasePropertiesPanel):
    TEMPLATE_KEY_MAPPING = {
        'flor': 'walkable',
        'wall': 'solid',
        'solid': 'solid',
        'walkable': 'walkable',
        'void': 'void'
    }

    def __init__(self, master, app: Any):
        super().__init__(master, app)
        self.service: Any | None = None
        self.blocks = self.app.repos.block.get_all()
        self.node_repo = self.app.repos.node
        self.miniature_size = 30
        self.selected_tags = set()

        main_frame = tk.LabelFrame(self, text="Доступные блоки", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.tag_filter_widget = TagInputWidget(main_frame, self.app.tag_filter_service, "block_tags",
                                                self.on_tags_changed)
        self.tag_filter_widget.pack(fill=tk.X, padx=5, pady=5)

        self.canvas = tk.Canvas(main_frame, bg=BG_PRIMARY)
        self.scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_PRIMARY)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self.scrollbar.pack(side="right", fill="y")

    def set_service(self, service: Any):
        self.service = service
        self.draw_all_miniatures()

    def on_tags_changed(self, tags: List[str]):
        self.selected_tags = set(tags)
        self.draw_all_miniatures()

    def on_miniature_click(self, block_key: str):
        if self.service:
            self.service.load_block_for_editing(block_key)

    def draw_all_miniatures(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        all_block_names = sorted(list(self.blocks.keys()))

        filtered_block_names = []
        for name in all_block_names:
            block_data = self.blocks.get(name, {})
            block_tags = set(block_data.get('tags', []))
            if not self.selected_tags or self.selected_tags.issubset(block_tags):
                filtered_block_names.append(name)

        for name in filtered_block_names:
            block_data_source = self.blocks.get(name, {'nodes_structure': [], 'nodes_data': {}})
            nodes_structure = block_data_source.get('nodes_structure', [])
            block_nodes_data = block_data_source.get('nodes_data', {})

            miniature_frame = tk.Frame(self.scrollable_frame, bg=BG_PRIMARY)
            miniature_frame.pack(fill=tk.X, padx=2, pady=2)

            miniature_frame.bind("<Button-1>", lambda e, key=name: self.on_miniature_click(key))

            block_canvas = tk.Canvas(miniature_frame, width=self.miniature_size, height=self.miniature_size,
                                     bg=BG_CANVAS, highlightthickness=0, borderwidth=1, relief="solid")
            block_canvas.pack(side="left", padx=(0, 5))
            block_canvas.bind("<Button-1>", lambda e, key=name: self.on_miniature_click(key))

            if nodes_structure and nodes_structure[0]:
                height = len(nodes_structure)
                width = len(nodes_structure[0])
                tile_size = min(self.miniature_size // width, self.miniature_size // height)
                if tile_size > 0:
                    for r, row_values in enumerate(nodes_structure):
                        for c, node_id in enumerate(row_values):
                            x1 = c * tile_size
                            y1 = r * tile_size
                            x2 = x1 + tile_size
                            y2 = y1 + tile_size

                            if node_id is None:
                                fill_color = BG_CANVAS
                            else:
                                node_details = block_nodes_data.get(str(node_id), {})
                                template_key = node_details.get('template_key', 'void')
                                mapped_key = self.TEMPLATE_KEY_MAPPING.get(template_key, 'void')
                                node_template_data = self.node_repo.get_by_key(mapped_key)

                                if node_template_data:
                                    fill_color = node_template_data.get('color', '#ff00ff')
                                else:
                                    fill_color = '#ff00ff'

                            block_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="")

            display_name = block_data_source.get('display_name', name)
            block_label = tk.Label(miniature_frame, text=display_name, fg=FG_TEXT, bg=BG_PRIMARY, anchor="w")
            block_label.pack(side="left", fill=tk.X, expand=True)
            block_label.bind("<Button-1>", lambda e, key=name: self.on_miniature_click(key))

            miniature_frame.bind("<Enter>", lambda e, fr=miniature_frame: fr.config(bg=BG_HIGHLIGHT))
            miniature_frame.bind("<Leave>", lambda e, fr=miniature_frame: fr.config(bg=BG_PRIMARY))
            block_label.bind("<Enter>", lambda e, fr=miniature_frame: fr.config(bg=BG_HIGHLIGHT))
            block_label.bind("<Leave>", lambda e, fr=miniature_frame: fr.config(bg=BG_PRIMARY))
            block_canvas.bind("<Enter>", lambda e, fr=miniature_frame: fr.config(bg=BG_HIGHLIGHT))
            block_canvas.bind("<Leave>", lambda e, fr=miniature_frame: fr.config(bg=BG_PRIMARY))