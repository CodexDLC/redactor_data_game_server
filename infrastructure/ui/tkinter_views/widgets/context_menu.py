# File: infrastructure/ui/tkinter_views/widgets/context_menu.py (version 0.2)
import tkinter as tk
from tkinter import Menu

def add_editing_menu(widget: tk.Widget):
    """
    Добавляет стандартное контекстное меню и горячие клавиши
    для Cut/Copy/Paste/Delete к текстовому виджету или полю ввода.
    """
    menu = tk.Menu(widget, tearoff=0, bg="#333333", fg="white")
    menu.add_command(label="Вырезать", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="Копировать", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Вставить", command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_command(label="Удалить", command=lambda: widget.event_generate("<<Clear>>"))

    def show_menu(event):
        # Показываем меню в месте клика
        menu.tk_popup(event.x_root, event.y_root)

    widget.bind("<Button-3>", show_menu)
    # Привязываем горячие клавиши
    widget.bind("<Control-x>", lambda e: widget.event_generate("<<Cut>>"))
    widget.bind("<Control-c>", lambda e: widget.event_generate("<<Copy>>"))
    widget.bind("<Control-v>", lambda e: widget.event_generate("<<Paste>>"))