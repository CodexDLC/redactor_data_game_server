# File: infrastructure/ui/tkinter_views/widgets/universal_context_menu.py (version 0.2)
import tkinter as tk
from tkinter import Menu
from typing import Any, Dict, Callable


def create_universal_context_menu(widget: tk.Widget, commands: Dict[str, Callable]) -> Menu:
    """
    Создает унифицированное контекстное меню с подменю и привязывает команды.
    """
    menu = Menu(widget, tearoff=0, bg="#333333", fg="white")

    # Верхний уровень
    menu.add_command(label="Отменить кисточку", command=commands.get("unselect_brush"))
    menu.add_separator()
    menu.add_command(label="Вырезать", command=commands.get("cut"))
    menu.add_command(label="Копировать", command=commands.get("copy"))
    menu.add_command(label="Вставить", command=commands.get("paste"))
    menu.add_command(label="Удалить", command=commands.get("delete"))
    menu.add_separator()

    # Подменю "Палитра"
    palette_menu = Menu(menu, tearoff=0, bg="#333333", fg="white")
    palette_menu.add_command(label="Палитра Нодов", command=commands.get("open_node_palette"))
    palette_menu.add_command(label="Палитра Блоков", command=commands.get("open_block_palette"))
    palette_menu.add_command(label="Палитра Локаций", command=commands.get("open_location_palette"))
    menu.add_cascade(label="Палитра", menu=palette_menu)

    # Подменю "Инструменты Карты"
    map_tools_menu = Menu(menu, tearoff=0, bg="#333333", fg="white")
    map_tools_menu.add_command(label="Инструмент 1", command=commands.get("tool_1"))
    map_tools_menu.add_command(label="Инструмент 2", command=commands.get("tool_2"))
    menu.add_cascade(label="Инструменты Карты", menu=map_tools_menu)

    return menu