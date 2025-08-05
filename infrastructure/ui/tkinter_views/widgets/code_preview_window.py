# File: infrastructure/ui/tkinter_views/widgets/code_preview_window.py (version 0.3)
import tkinter as tk
import json
from typing import Any
from .context_menu import add_editing_menu


class CodePreviewWindow(tk.Toplevel):
    """Окно для отображения форматированного JSON-кода."""

    def __init__(self, master, data_to_display: Any, title: str = "Предпросмотр Кода"):
        super().__init__(master)
        self.title(title)
        self.geometry("400x500")
        self.config(bg="#333333")
        self.transient(master)
        self.attributes("-topmost", True)

        self._data = data_to_display
        self._build_ui()
        self.update_content()

    def _build_ui(self):
        toolbar = tk.Frame(self, bg="#333333")
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(toolbar, text="Обновить", command=self.update_content, bg="#444444", fg="white").pack(side=tk.LEFT)

        self.text_widget = tk.Text(self, bg="#1a1a1a", fg="white", borderwidth=0, wrap=tk.WORD, font=("Courier", 10))
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        add_editing_menu(self.text_widget)

    def update_content(self, new_data: Any = None):
        """Обновляет содержимое окна, отображая новые данные."""
        if new_data is not None:
            self._data = new_data

        formatted_json = json.dumps(self._data, indent=4, ensure_ascii=False)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', formatted_json)
        self.text_widget.config(state='disabled')