# File: infrastructure/ui/tkinter_views/editors/prebuffer/prebuffer_gallery_panel.py
import tkinter as tk
from typing import Any, Dict, List
from ...styles import *
from ..base_properties_panel import BasePropertiesPanel


class PrebufferGalleryPanel(BasePropertiesPanel):
    """
    Панель для отображения всех существующих пре-буферов в виде миниатюр 9x9.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, app)
        self.service: Any | None = None

        # ИЗМЕНЕНИЕ: Используем правильное имя репозитория - prebuffer_template
        self.prebuffers = self.app.repos.prebuffer_template.get_all()

        self.miniature_size = 60
        self._build_ui()

    def _build_ui(self):
        main_frame = tk.LabelFrame(self, text="Доступные пре-буферы", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main_frame, bg=BG_PRIMARY)
        self.scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_PRIMARY)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self.scrollbar.pack(side="right", fill="y")

    def set_service(self, service: Any):
        self.service = service
        self.draw_all_miniatures()

    def on_miniature_click(self, prebuffer_key: str):
        if self.service:
            print(f"Клик по миниатюре: {prebuffer_key}")

    def draw_all_miniatures(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Пока просто заглушка с одним элементом
        miniature_frame = tk.Frame(self.scrollable_frame, bg=BG_PRIMARY)
        miniature_frame.pack(fill=tk.X, padx=2, pady=2)
        tk.Label(miniature_frame, text="Предпросмотр 9x9 будет здесь", fg=FG_TEXT, bg=BG_PRIMARY).pack()