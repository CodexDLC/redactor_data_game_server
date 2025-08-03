import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable


class FloatingPaletteWindow(tk.Toplevel):
    """
    Базовый класс для плавающего окна-палитры, которое всегда поверх основного.
    """

    def __init__(self, master, title="Палитра", nodes_data: Dict[str, Any] = None):
        super().__init__(master)
        self.title(title)
        self.geometry("300x500")  # Размер по умолчанию
        self.config(bg="#333333")

        self.nodes_data = nodes_data
        self.on_node_selected_callback: Callable[[str], None] = None

        # Делаем окно всегда поверх родительского
        self.transient(master)
        self.attributes("-topmost", True)

        # --- Создаем базовую структуру окна ---

        # 1. Фрейм для фильтров (сверху)
        self.filter_frame = tk.Frame(self, bg="#222222")
        self.filter_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(self.filter_frame, text="Фильтры (в разработке)", fg="white", bg="#222222").pack()

        # 2. Фрейм для основного контента (списка ассетов)
        self.content_frame = tk.Frame(self, bg="#333333")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._create_node_list()

    def _create_node_list(self):
        """Создает и отображает список нодов в прокручиваемой области."""
        canvas = tk.Canvas(self.content_frame, bg="#333333")
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
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

        if self.nodes_data:
            for node_key, node_info in sorted(self.nodes_data.items()):
                item_frame = tk.Frame(scrollable_frame, bg="#333333")
                item_frame.pack(fill="x", expand=True, pady=1)

                color_label = tk.Label(item_frame, bg=node_info.get("color", "#ff00ff"), width=2, text=" ")
                color_label.pack(side="left", padx=(2, 5))

                name_label = tk.Label(item_frame, text=node_key, fg="white", bg="#333333", anchor="w")
                name_label.pack(side="left", fill="x", expand=True)

                # TODO: Добавить логику привязки к "кисточке"
                click_handler = lambda e, key=node_key: print(f"Selected node for brush: {key}")
                item_frame.bind("<Button-1>", click_handler)
                color_label.bind("<Button-1>", click_handler)
                name_label.bind("<Button-1>", click_handler)