import tkinter as tk

def add_right_click_menu(widget):
    """Добавляет стандартное контекстное меню к виджету."""
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Вырезать", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="Копировать", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Вставить", command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_separator()
    menu.add_command(label="Выделить всё", command=lambda: widget.event_generate("<<SelectAll>>"))

    def show_menu(event):
        # Показываем меню в месте клика
        menu.tk_popup(event.x_root, event.y_root)

    widget.bind("<Button-3>", show_menu) # Привязываем к правому клику мыши