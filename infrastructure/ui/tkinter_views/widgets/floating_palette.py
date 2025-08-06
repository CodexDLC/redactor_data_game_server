# File: infrastructure/ui/tkinter_views/widgets/floating_palette.py
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Optional
from ..widgets.context_menu import add_editing_menu
from ..styles import *
import logging


class FloatingPaletteWindow(tk.Toplevel):
    """Плавающее окно для отображения и выбора элементов (нодов, блоков)."""

    def __init__(self, master, title: str, app: Any, items_data: Dict[str, Any], x: Optional[int] = None,
                 y: Optional[int] = None, palette_type: str = "nodes", node_data_source: Optional[Dict[str, Any]] = None):
        super().__init__(master)
        self.app = app
        self.title(title)
        self.items_data = items_data
        self.palette_type = palette_type
        self.node_data_source = node_data_source
        self._selected_item_frame = None
        self._selected_item_original_color = None
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.attributes("-topmost", True)
        self.overrideredirect(True)

        if x is not None and y is not None:
            self.geometry(f"+{x}+{y}")
        else:
            self.geometry("200x300")

        self.create_widgets()
        self.update_list()

        self.bind("<Button-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)
        self._x = 0
        self._y = 0

    def create_widgets(self):
        main_frame = tk.Frame(self, bg=BG_PRIMARY, relief="raised", bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = tk.Frame(main_frame, bg=BG_SECONDARY)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(header_frame, text=self.title(), fg=FG_TEXT, bg=BG_SECONDARY,
                               font=("Helvetica", 10, "bold"))
        title_label.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(header_frame, text="X", command=self.hide, bg="red", fg=FG_TEXT, relief="flat")
        close_button.pack(side=tk.RIGHT)

        self.filter_frame = tk.LabelFrame(main_frame, text="Фильтры", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        self.filter_frame.pack(fill=tk.X, padx=5, pady=5)

        filter_content_frame = tk.Frame(self.filter_frame, bg=BG_PRIMARY)
        filter_content_frame.pack(fill=tk.X)

        self.miniature_indicator = tk.Canvas(filter_content_frame, width=20, height=20, bg=BG_PRIMARY, bd=1,
                                             relief=tk.SUNKEN, highlightthickness=0)
        self.miniature_indicator.pack(side=tk.LEFT, padx=(0, 5))

        tk.Label(filter_content_frame, text="Место для будущих фильтров...", fg=FG_TEXT, bg=BG_PRIMARY).pack(
            side=tk.LEFT)

        close_list_button = tk.Button(main_frame, text="Закрыть", command=self.hide, bg=BG_SECONDARY, fg=FG_TEXT)
        close_list_button.pack(fill=tk.X, padx=5, pady=5)

        list_frame = tk.Frame(main_frame, bg=BG_PRIMARY)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.list_canvas = tk.Canvas(list_frame, bg=BG_CANVAS)
        self.scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.list_canvas.yview)
        self.scrollable_frame = tk.Frame(self.list_canvas, bg=BG_PRIMARY)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.list_canvas.configure(
                scrollregion=self.list_canvas.bbox("all")
            )
        )

        self.list_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.list_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.list_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def update_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for name, data in sorted(self.items_data.items()):
            item_frame = tk.Frame(self.scrollable_frame, bg=BG_PRIMARY)
            item_frame.pack(fill="x", pady=1)

            miniature_canvas = tk.Canvas(item_frame, width=20, height=20, bg="#222222", highlightthickness=0)
            miniature_canvas.pack(side="left", padx=(2, 5))

            self._draw_item_miniature(miniature_canvas, data)

            name_label = tk.Label(item_frame, text=data.get('display_name', name), fg=FG_TEXT, bg=BG_PRIMARY,
                                  anchor="w")
            name_label.pack(side="left", fill="x", expand=True)

            click_handler = lambda e, key=name, data=data, frame=item_frame: self._on_item_click(key, data, frame)
            item_frame.bind("<Button-1>", click_handler)
            miniature_canvas.bind("<Button-1>", click_handler)
            name_label.bind("<Button-1>", click_handler)

            item_frame.bind("<Enter>", lambda e, fr=item_frame: fr.config(bg=BG_HIGHLIGHT))
            item_frame.bind("<Leave>", lambda e, fr=item_frame: fr.config(bg=BG_PRIMARY))

    def _draw_item_miniature(self, canvas: tk.Canvas, data: Dict[str, Any]):
        canvas.delete("all")
        if self.palette_type == "nodes":
            color = data.get('color', ACCENT_COLOR)
            canvas.create_rectangle(0, 0, 20, 20, fill=color, outline="")
        elif self.palette_type == "blocks":
            nodes_structure = data.get('nodes_structure', [])
            nodes_data_map = data.get('nodes_data', {})
            if nodes_structure and self.node_data_source:
                block_size_cells = len(nodes_structure[0])
                tile_size = 20 // block_size_cells

                for r in range(block_size_cells):
                    for c in range(block_size_cells):
                        node_id = nodes_structure[r][c]
                        if node_id is not None:
                            node_template_key = nodes_data_map.get(str(node_id), {}).get('template_key')
                            node_color = self.node_data_source.get(node_template_key, {}).get('color', '#888888')
                        else:
                            node_color = '#000000'

                        x1 = c * tile_size
                        y1 = r * tile_size
                        x2 = x1 + tile_size
                        y2 = y1 + tile_size

                        canvas.create_rectangle(x1, y1, x2, y2, fill=node_color, outline="")

    def _on_item_click(self, key: str, data: Dict[str, Any], frame: tk.Frame):
        logging.info(f"Выбран элемент: {key}")

        if self._selected_item_frame:
            self._selected_item_frame.config(bg=BG_PRIMARY)
            for child in self._selected_item_frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=BG_PRIMARY)

        self._selected_item_frame = frame
        frame.config(bg=BG_HIGHLIGHT)
        for child in frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=BG_HIGHLIGHT)

        selected_item_data = data.copy()

        if self.palette_type == "nodes":
            selected_item_data['node_key'] = key
            self.app.set_active_brush_node(selected_item_data)
        elif self.palette_type == "blocks":
            selected_item_data['block_key'] = key
            self.app.set_active_brush_block(selected_item_data)

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def stop_move(self, event):
        self._x = None
        self._y = None

    def do_move(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def hide(self):
        self.withdraw()

    def show(self):
        self.deiconify()