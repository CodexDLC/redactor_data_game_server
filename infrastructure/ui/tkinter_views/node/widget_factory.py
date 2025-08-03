import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple


def create_widget_for_property(parent: tk.Widget, key: str, prop_info: Dict[str, Any]) -> Tuple[tk.Widget, Any]:
    """
    Создает виджет с меткой на основе схемы свойства.
    Возвращает кортеж из (виджет, ассоциированная с ним переменная/объект).
    """
    prop_type = prop_info.get("type", "string")
    label_text = prop_info.get("label", key.capitalize())

    frame = tk.Frame(parent, bg="#333333")
    label = tk.Label(frame, text=label_text, fg="white", bg="#333333")
    label.pack(side=tk.LEFT, padx=(0, 5), anchor="w")

    if prop_type == 'boolean':
        variable = tk.BooleanVar()
        widget = tk.Checkbutton(frame, variable=variable, bg="#333333", selectcolor="#444444",
                                activebackground="#333333", highlightthickness=0)
        widget.pack(side=tk.LEFT)
        return frame, (variable, widget)

    # Для range, dropdown и других типов пока используем простое текстовое поле.
    # В будущем мы можем расширить эту фабрику.
    else:  # string, number, range, dropdown
        variable = tk.StringVar()
        widget = tk.Entry(frame, textvariable=variable, bg="#444444", fg="white")
        widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        return frame, (variable, widget)