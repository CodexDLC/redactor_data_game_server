# File: infrastructure/ui/tkinter_views/widgets/widget_factory.py
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple

from ..styles import *
from .context_menu import add_editing_menu


def create_widget_for_property(parent: tk.Widget, key: str, prop_info: Dict[str, Any]) -> Tuple[Any, tk.Label, tk.Widget]:
    """
    Создает метку и виджет на основе схемы свойства.
    НЕ размещает их, только создает.
    Возвращает кортеж из (переменная, метка, виджет).
    """
    prop_type = prop_info.get("type", "string")
    label_text = prop_info.get("label", key.capitalize())
    options = prop_info.get("options", [])

    label = tk.Label(parent, text=label_text, fg=FG_TEXT, bg=BG_PRIMARY)

    if prop_type == 'boolean':
        variable = tk.BooleanVar()
        widget = tk.Checkbutton(parent, variable=variable, bg=BG_PRIMARY, selectcolor=BG_SECONDARY,
                                activebackground=BG_PRIMARY, highlightthickness=0)
        return variable, label, widget

    elif prop_type == 'dropdown':
        variable = tk.StringVar()
        widget = ttk.Combobox(parent, textvariable=variable, values=options, state="readonly")
        return variable, label, widget

    # string, range, number и т.д.
    else:
        variable = tk.StringVar()
        widget = tk.Entry(parent, textvariable=variable, bg=BG_SECONDARY, fg=FG_TEXT, insertbackground=FG_TEXT)
        add_editing_menu(widget)
        return variable, label, widget