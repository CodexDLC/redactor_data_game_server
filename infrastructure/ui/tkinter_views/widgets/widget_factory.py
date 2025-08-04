import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple
from .context_menu import add_editing_menu
from ..styles import *


def create_widget_for_property(parent: tk.Widget, key: str, prop_info: Dict[str, Any]) -> Tuple[tk.Widget, Any]:
    """
    Создает виджет с меткой на основе схемы свойства.
    Возвращает кортеж из (виджет, ассоциированная с ним переменная/объект).
    """
    prop_type = prop_info.get("type", "string")
    label_text = prop_info.get("label", key.capitalize())
    options = prop_info.get("options", None)

    frame = tk.Frame(parent, bg=BG_PRIMARY)
    label = tk.Label(frame, text=label_text, fg=FG_TEXT, bg=BG_PRIMARY)
    label.pack(side=tk.LEFT, padx=(0, 5), anchor="w")

    if prop_type == 'boolean':
        variable = tk.BooleanVar()
        widget = tk.Checkbutton(frame, variable=variable, bg=BG_PRIMARY, selectcolor=BG_SECONDARY,
                                activebackground=BG_PRIMARY, highlightthickness=0)
        widget.pack(side=tk.LEFT)
        return frame, (variable, widget)

    elif options is not None:
        variable = tk.StringVar()
        widget = ttk.Combobox(frame, textvariable=variable, values=options, state="readonly")
        widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        return frame, (variable, widget)

    else:  # string, number, range, dropdown
        variable = tk.StringVar()
        widget = tk.Entry(frame, textvariable=variable, bg=BG_SECONDARY, fg=FG_TEXT)
        widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        add_editing_menu(widget)
        return frame, (variable, widget)