# File: infrastructure/ui/tkinter_views/widgets/widget_factory.py
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple

from ..styles import *
from .context_menu import add_editing_menu


def create_widget_for_property(parent: tk.Widget, key: str, prop_info: Dict[str, Any]) -> Tuple[tk.Widget, Any]:
    """
    Создает готовую рамку (Frame) с меткой и виджетом.
    Возвращает кортеж из (рамка, (переменная, виджет)).
    """
    prop_type = prop_info.get("type", "string")
    label_text = prop_info.get("label", key.capitalize())
    options = prop_info.get("options", [])

    # --- ИСПРАВЛЕНИЕ: Создаем рамку-контейнер ---
    frame = tk.Frame(parent, bg=BG_PRIMARY)
    label = tk.Label(frame, text=label_text, fg=FG_TEXT, bg=BG_PRIMARY, width=25, anchor="w") # Задаем ширину для выравнивания
    label.pack(side=tk.LEFT, padx=(0, 5))

    if prop_type == 'boolean':
        variable = tk.BooleanVar()
        widget = tk.Checkbutton(frame, variable=variable, bg=BG_PRIMARY, selectcolor=BG_SECONDARY,
                                activebackground=BG_PRIMARY, highlightthickness=0)
        widget.pack(side=tk.LEFT)
        return frame, (variable, widget)

    elif prop_type == 'dropdown':
        variable = tk.StringVar()
        widget = ttk.Combobox(frame, textvariable=variable, values=options, state="readonly")
        widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        return frame, (variable, widget)

    else:  # string, range, number
        variable = tk.StringVar()
        widget = tk.Entry(frame, textvariable=variable, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        add_editing_menu(widget)
        return frame, (variable, widget)
