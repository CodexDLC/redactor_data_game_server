# File: infrastructure/ui/tkinter_views/widgets/code_preview_window.py
import tkinter as tk
import json
from typing import Any, Dict
from .context_menu import add_editing_menu
from ..styles import *


class CodePreviewWindow(tk.Toplevel):
    def __init__(self, master, template_data: Any, object_data: Any, title: str = "Предпросмотр Кода"):
        super().__init__(master)
        self.title(title)
        self.geometry("400x500")
        self.config(bg="#333333")
        self.transient(master)
        self.attributes("-topmost", True)

        self._template_data = template_data
        self._object_data = object_data
        self._current_data = self._template_data

        self._build_ui()
        self.update_content()

    def _build_ui(self):
        toolbar = tk.Frame(self, bg=BG_SECONDARY)
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        # Кнопки для переключения вида
        tk.Button(toolbar, text="Шаблон", command=self.show_template, bg=BG_PRIMARY, fg=FG_TEXT).pack(side=tk.LEFT,
                                                                                                      padx=5)
        tk.Button(toolbar, text="Объект", command=self.show_object, bg=BG_PRIMARY, fg=FG_TEXT).pack(side=tk.LEFT,
                                                                                                    padx=5)

        self.text_widget = tk.Text(self, bg=CODE_BG, fg=CODE_FG, borderwidth=0, wrap=tk.WORD, font=CODE_FONT)
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        add_editing_menu(self.text_widget)

    def show_template(self):
        self._current_data = self._template_data
        self.update_content()

    def show_object(self):
        self._current_data = self._object_data
        self.update_content()

    def update_content(self, new_data: Any = None):
        if new_data is not None:
            self._current_data = new_data

        formatted_json = json.dumps(self._current_data, indent=4, ensure_ascii=False)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', formatted_json)
        self.text_widget.config(state='disabled')