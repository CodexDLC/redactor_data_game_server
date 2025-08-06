# File: infrastructure/ui/tkinter_views/left_panel/modules.py
import tkinter as tk
from tkinter import messagebox, ttk
from .base import BaseLeftPanel
from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.persistence.i_module_repository import IModuleRepository
from interfaces.persistence.i_node_repository import INodeRepository


class ModulesPanel(BaseLeftPanel):
    def __init__(self, master, app, module_repo: IModuleRepository, block_repo: IBlockRepository, node_repo: INodeRepository, miniature_size,
                 miniature_padding, font, frame_width):
        super().__init__(master, app, {}, miniature_size, miniature_padding, font, frame_width)

        self.module_repo = module_repo
        self.block_repo = block_repo
        self.node_repo = node_repo

        self.modules = {}

        tk.Label(self, text="Доступные модули", fg="white", bg="#333333").pack(pady=5)

        self.canvas = tk.Canvas(self, bg="#333333")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#333333")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.draw_all_miniatures()

    def on_notebook_configure(self, event):
        container_width = event.width
        if container_width > 0:
            new_num_cols = max(1, container_width // (self.frame_width + self.miniature_padding * 2))

            if new_num_cols != self.num_miniature_cols:
                self.num_miniature_cols = new_num_cols
                self.draw_all_miniatures()

    def draw_all_miniatures(self):
        all_module_names = list(self.module_repo.get_all().keys())
        self._draw_miniatures_for_modules(self.scrollable_frame, all_module_names)

    def _draw_miniatures_for_modules(self, container_frame, module_names):
        for widget in container_frame.winfo_children():
            widget.destroy()

        if self.num_miniature_cols == 0:
            return

        for i, name in enumerate(module_names):
            row = i // self.num_miniature_cols
            col = i % self.num_miniature_cols

            miniature_frame = tk.Frame(container_frame, bg="#333333", borderwidth=1, relief="solid",
                                       width=self.frame_width, height=self.miniature_size + 20)
            miniature_frame.grid(row=row, column=col, padx=self.miniature_padding, pady=self.miniature_padding,
                                 sticky="n")
            miniature_frame.pack_propagate(False)

            module_canvas = tk.Canvas(miniature_frame, width=self.miniature_size, height=self.miniature_size,
                                    bg="#222222", highlightthickness=0)
            module_canvas.pack(pady=(5, 0))

            module_data = self.module_repo.get_by_key(name)
            if not module_data:
                continue

            # TODO: Добавить логику отрисовки миниатюры модуля
            # Здесь должна быть логика, которая проходит по nodes_structure модуля
            # и отрисовывает маленькие квадраты, используя цвета из node_repo.

            module_label = tk.Label(miniature_frame, text=name, fg="white", bg="#333333", font=self.font)
            module_label.pack()

            miniature_frame.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            module_canvas.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))
            module_label.bind("<Button-1>", lambda e, n=name: self.on_miniature_click(n))

            miniature_frame.bind("<Enter>", lambda e, fr=miniature_frame: fr.config(bg="gray"))
            miniature_frame.bind("<Leave>", lambda e, fr=miniature_frame: fr.config(bg="#333333"))

    def on_miniature_click(self, module_name):
        # TODO: Реализовать логику выбора модуля в качестве кисточки
        self.app.on_module_selected(module_name)