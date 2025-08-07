# File: infrastructure/ui/tkinter_views/editors/block/block_actions_panel.py
from typing import Any
from ..base_actions_panel import BaseActionsPanel


class BlockActionsPanel(BaseActionsPanel):
    """
    Панель действий для Редактора Блоков.
    На данный момент наследует все универсальные кнопки без добавления новых.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, app)

        # В будущем здесь можно будет добавлять специфичные кнопки для этого редактора
        # Например: self.some_specific_button = tk.Button(...)
        # self.some_specific_button.pack(...)

