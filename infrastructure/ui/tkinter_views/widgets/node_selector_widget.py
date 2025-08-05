# File: infrastructure/ui/tkinter_views/widgets/node_selector_widget.py
import tkinter as tk
from tkinter import ttk
from typing import Callable, List

from infrastructure.ui.tkinter_views.styles import *


class NodeSelectorWidget(tk.LabelFrame):
    """
    Самодостаточный виджет для выбора нода из выпадающего списка.
    """

    def __init__(self, master, on_selection_changed: Callable[[str], None]):
        """
        Инициализирует виджет.

        :param master: Родительский виджет.
        :param on_selection_changed: Функция (callback), которая будет вызвана
                                     с ID выбранного нода при изменении выбора.
        """
        super().__init__(master, text="Выбор нода для редактирования", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)

        # Сохраняем callback-функцию, чтобы вызывать ее при выборе
        self.on_selection_changed_callback = on_selection_changed

        # Переменная для хранения текущего выбора в Combobox
        self.selected_node_str = tk.StringVar()

        # Создаем сам Combobox
        self.node_selector_combo = ttk.Combobox(self, textvariable=self.selected_node_str, state="readonly")
        self.node_selector_combo.pack(fill=tk.X)

        # Привязываем событие выбора в списке к нашему внутреннему обработчику
        self.node_selector_combo.bind("<<ComboboxSelected>>", self._on_select)

    def update_list(self, node_list: List[str]):
        """
        Публичный метод для обновления списка нодов в Combobox.
        :param node_list: Список строк для отображения.
        """
        print(f"NodeSelectorWidget.update_list: Получен список нодов: {node_list}") # <-- ДОБАВЛЕНО
        self.node_selector_combo['values'] = node_list
        # Очищаем текущий выбор, чтобы избежать путаницы
        self.selected_node_str.set("")
        print(f"NodeSelectorWidget.update_list: Значения Combobox после обновления: {self.node_selector_combo['values']}")

    def _on_select(self, event=None):
        """
        Внутренний обработчик, который срабатывает при выборе элемента в списке.
        Он извлекает чистый ID нода и передает его "наружу" через callback.
        """
        selection = self.selected_node_str.get()
        if not selection:
            return

        try:
            # Извлекаем ID нода из строки, например, из "[0,1] wall (new_block_key_0_1)"
            # получаем "new_block_key_0_1"
            node_id = selection.split('(')[-1][:-1]

            # Вызываем внешнюю функцию, которую нам передали при создании
            if self.on_selection_changed_callback:
                self.on_selection_changed_callback(node_id)
        except IndexError:
            # Обработка случая, если строка имеет неожиданный формат
            print(f"Ошибка: Не удалось извлечь ID из строки '{selection}'")