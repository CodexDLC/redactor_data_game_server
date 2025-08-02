import tkinter as tk
from tkinter import ttk
from editor_logic.helpers import utils


class BaseLeftPanel(tk.Frame):
    def __init__(self, master, app, blocks_dict, miniature_size, miniature_padding, font, frame_width):
        super().__init__(master)
        self.app = app
        self.blocks = blocks_dict
        self.miniature_size = miniature_size
        self.miniature_padding = miniature_padding
        self.font = font
        self.frame_width = frame_width
        self.num_miniature_cols = 0
        self.selected_block_name = None

        tk.Label(self, text="Доступные блоки", fg="white", bg="#333333").pack(pady=5)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.notebook.bind("<Configure>", self.on_notebook_configure)
        
    def on_notebook_configure(self, event):
        container_width = event.width
        if container_width > 0:
            new_num_cols = max(1, container_width // (self.frame_width + self.miniature_padding * 2))

            if new_num_cols != self.num_miniature_cols:
                self.num_miniature_cols = new_num_cols
                self.draw_all_miniatures()

    def group_blocks_by_category(self):
        grouped_blocks = {}
        for name in sorted(self.blocks.keys()):
            parts = name.split('_')
            category = parts[1] if len(parts) > 1 else "other"
            if category not in grouped_blocks:
                grouped_blocks[category] = []
            grouped_blocks[category].append(name)
        return grouped_blocks

    def draw_all_miniatures(self):
        grouped_blocks = self.group_blocks_by_category()

        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        for category, block_names in grouped_blocks.items():
            tab_frame = tk.Frame(self.notebook, bg="#333333")
            self.notebook.add(tab_frame, text=category.capitalize())

            canvas = tk.Canvas(tab_frame, bg="#333333")
            scrollbar = tk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#333333")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            self.draw_miniatures_for_category(scrollable_frame, block_names)

    def draw_miniatures_for_category(self, container_frame, block_names):
        for widget in container_frame.winfo_children():
            widget.destroy()

        if self.num_miniature_cols == 0:
            return

        for i, name in enumerate(block_names):
            row = i // self.num_miniature_cols
            col = i % self.num_miniature_cols

            miniature_frame = tk.Frame(container_frame, bg="#333333", borderwidth=1, relief="solid",
                                       width=self.frame_width, height=self.miniature_size + 20)
            miniature_frame.grid(row=row, column=col, padx=self.miniature_padding, pady=self.miniature_padding,
                                 sticky="n")
            miniature_frame.pack_propagate(False)

            block_canvas = tk.Canvas(miniature_frame, width=self.miniature_size, height=self.miniature_size,
                                     bg="#222222", highlightthickness=0)
            block_canvas.pack(pady=(5, 0))

            block_data = self.blocks[name]
            block_size = len(block_data)

            tile_colors = {1: "#7f7f7f", 0: "#000000", 2: "#ff0000", 3: "#ffff00"}  # Задаем цвета здесь

            for r in range(block_size):
                for c in range(block_size):
                    tile_x1 = c * (self.miniature_size // block_size)
                    tile_y1 = r * (self.miniature_size // block_size)
                    tile_x2 = tile_x1 + (self.miniature_size // block_size)
                    tile_y2 = tile_y1 + (self.miniature_size // block_size)

                    fill_color = tile_colors.get(block_data[r][c], "#7f7f7f")
                    block_canvas.create_rectangle(tile_x1, tile_y1, tile_x2, tile_y2, fill=fill_color, outline="")

            block_label = tk.Label(miniature_frame, text=name, fg="white", bg="#333333", font=self.font)
            block_label.pack()

            miniature_frame.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            block_canvas.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            block_label.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))

            miniature_frame.bind("<Enter>", lambda e, fr=miniature_frame: fr.config(bg="gray"))
            miniature_frame.bind("<Leave>", lambda e, fr=miniature_frame: fr.config(bg="#333333"))

    def on_miniature_click(self, block_name):
        self.selected_block_name = block_name
        self.highlight_selected_miniature()
        if hasattr(self.app, 'on_block_selected'):
            self.app.on_block_selected(block_name)

    def highlight_selected_miniature(self):
        for tab_frame_id in self.notebook.tabs():
            tab_frame = self.notebook.nametowidget(tab_frame_id)
            scroll_canvas = tab_frame.winfo_children()[0]
            scrollable_frame = scroll_canvas.winfo_children()[0]
            for widget in scrollable_frame.winfo_children():
                widget.config(bg="#333333")
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg="#333333")

        if self.selected_block_name:
            grouped_blocks = self.group_blocks_by_category()
            for category, block_names in grouped_blocks.items():
                if self.selected_block_name in block_names:
                    for tab_frame_id in self.notebook.tabs():
                        if self.notebook.tab(tab_frame_id, "text").lower() == category:
                            tab_frame = self.notebook.nametowidget(tab_frame_id)
                            scroll_canvas = tab_frame.winfo_children()[0]
                            scrollable_frame = scroll_canvas.winfo_children()[0]
                            for widget in scrollable_frame.winfo_children():
                                label = next((w for w in widget.winfo_children() if isinstance(w, tk.Label)), None)
                                if label and label.cget("text") == self.selected_block_name:
                                    widget.config(bg="blue")
                                    label.config(bg="blue")
                                    return