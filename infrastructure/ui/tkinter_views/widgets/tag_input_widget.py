# File: infrastructure/ui/tkinter_views/widgets/tag_input_widget.py
import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional
from ..styles import *
# --- ИСПРАВЛЕНО: Добавляем импорт для контекстного меню ---
from .context_menu import add_editing_menu


class TagInputWidget(tk.Frame):
    """
    Виджет для ввода тегов с функцией автозаполнения,
    использующий Listbox для постоянного отображения подсказок.
    """

    def __init__(self, master, tag_filter_service, category: str, on_tags_changed: Optional[Callable] = None):
        super().__init__(master, bg=BG_PRIMARY)
        self.tag_filter_service = tag_filter_service
        self.category = category
        self.on_tags_changed = on_tags_changed
        self.tags = set()

        entry_frame = tk.Frame(self, bg=BG_PRIMARY)
        entry_frame.pack(fill=tk.X, expand=True)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(entry_frame, textvariable=self.entry_var, bg=BG_SECONDARY, fg=FG_TEXT,
                              insertbackground=FG_TEXT)
        self.entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.entry_var.trace("w", self._on_input_changed)

        # --- ИСПРАВЛЕНО: Применяем контекстное меню и горячие клавиши ---
        add_editing_menu(self.entry)

        self.tags_frame = tk.Frame(self, bg=BG_PRIMARY)
        self.tags_frame.pack(fill=tk.X)

        listbox_frame = tk.Frame(self, bg=BG_PRIMARY)
        listbox_frame.pack(fill=tk.X, padx=2, pady=2)

        self.listbox = tk.Listbox(listbox_frame, height=5, bg=BG_SECONDARY, fg=FG_TEXT, selectbackground=BG_HIGHLIGHT,
                                  selectforeground=FG_TEXT)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._select_tag_from_listbox)
        self.listbox.bind("<Return>", self._add_tag)
        self.listbox.bind("<Tab>", self._add_tag)

        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.entry.bind("<Return>", self._add_tag)
        self.entry.bind("<Tab>", self._add_tag)
        self._update_listbox()

    def _on_input_changed(self, *args):
        input_text = self.entry_var.get()
        self._update_listbox(input_text)

    def _update_listbox(self, search_query: str = ""):
        self.listbox.delete(0, tk.END)
        filtered_tags = self.tag_filter_service.filter_tags(self.category, search_query)
        for tag in filtered_tags:
            self.listbox.insert(tk.END, tag)

    def _select_tag_from_listbox(self, event):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            tag = self.listbox.get(selected_indices[0])
            self.tags.add(tag)
            self._update_display()
            self.entry_var.set("")
            self.entry.focus_set()

    def _add_tag(self, event):
        tag = self.entry_var.get().strip().lower()
        if tag and tag not in self.tags:
            self.tags.add(tag)
            self._update_display()
            self.entry_var.set("")
        return "break"

    def _remove_tag(self, tag_to_remove: str):
        self.tags.discard(tag_to_remove)
        self._update_display()

    def _update_display(self):
        for widget in self.tags_frame.winfo_children():
            widget.destroy()

        for tag in sorted(list(self.tags)):
            tag_frame = tk.Frame(self.tags_frame, bg=BG_SECONDARY, padx=5, pady=2)
            tag_frame.pack(side=tk.LEFT, padx=(0, 5), pady=2)

            tag_label = tk.Label(tag_frame, text=tag, bg=BG_SECONDARY, fg=FG_TEXT)
            tag_label.pack(side=tk.LEFT)

            close_button = tk.Button(tag_frame, text="x", command=lambda t=tag: self._remove_tag(t), bg=BG_SECONDARY,
                                     fg=FG_TEXT, relief="flat", padx=2, pady=0)
            close_button.pack(side=tk.LEFT)

        if self.on_tags_changed:
            self.on_tags_changed(list(self.tags))

    def get_tags(self) -> List[str]:
        return list(self.tags)

    def set_tags(self, tags: List[str]):
        self.tags = set(tags)
        self._update_display()