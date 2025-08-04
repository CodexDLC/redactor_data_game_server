import tkinter as tk
from tkinter import ttk
from typing import Any
from ...base_editor_controls import BaseEditorControls


class LocationEditorControls(BaseEditorControls):
    """
    Панель управления для редактора локаций.
    """

    def __init__(self, master, parent_view: Any):
        super().__init__(master, parent_view)

    def _build_ui(self):
        # TODO: Добавить уникальные элементы управления для редактора локаций.
        tk.Label(self, text="Панель управления локациями", fg="white", bg="#333333").pack(pady=5)

        super()._build_ui()