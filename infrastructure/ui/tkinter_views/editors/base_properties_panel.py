import tkinter as tk
from typing import Any
from ..styles import *


class BasePropertiesPanel(tk.Frame):
    """
    Базовый класс для новой левой панели Свойств.
    Пока что просто заглушка, будет расширяться дочерними классами.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, bg=BG_PRIMARY, padx=5, pady=5)
        self.app = app