# File: infrastructure/ui/tkinter_views/editors/block/block_actions_panel.py
from typing import Any
from ..base_actions_panel import BaseActionsPanel


class BlockActionsPanel(BaseActionsPanel):
    """
    Панель действий для Редактора Блоков.
    """

    def __init__(self, master, app: Any):
        # ИЗМЕНЕНИЕ: Вызываем конструктор родителя, передавая список только с одной палитрой
        super().__init__(master, app, palettes_to_show=['nodes'])