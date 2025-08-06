# File: infrastructure/ui/tkinter_views/widgets/log_console_window.py
import tkinter as tk
import logging
from logging import LogRecord
from ..styles import *


class TextWidgetHandler(logging.Handler):
    """Кастомный обработчик для перенаправления логов в текстовый виджет Tkinter."""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.text_widget.config(state=tk.DISABLED)

    def emit(self, record: LogRecord):
        msg = self.format(record)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)


class LogConsoleWindow(tk.Toplevel):
    """
    Самодостаточное окно для отображения консоли логов.
    """

    def __init__(self, master):
        super().__init__(master)
        self.title("Консоль логов")
        self.geometry("600x400")

        # Создаем и настраиваем текстовый виджет
        log_widget = tk.Text(self, bg=CODE_BG, fg=CODE_FG, font=CODE_FONT)
        log_widget.pack(fill=tk.BOTH, expand=True)

        # Создаем и подключаем обработчик логов
        self.handler = TextWidgetHandler(log_widget)  # <--- СОХРАНЯЕМ ССЫЛКУ НА ОБРАБОТЧИК
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Подключаемся к корневому логгеру
        logging.getLogger().addHandler(self.handler)

        # <--- НОВЫЙ КОД: ОБРАБАТЫВАЕМ СОБЫТИЕ ЗАКРЫТИЯ ОКНА --->
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Уведомляем, что консоль запущена
        logging.info("Консоль логов инициализирована.")

    def on_close(self):
        """
        Метод, который вызывается при закрытии окна.
        Удаляем обработчик из логгера.
        """
        logging.getLogger().removeHandler(self.handler)
        self.destroy()