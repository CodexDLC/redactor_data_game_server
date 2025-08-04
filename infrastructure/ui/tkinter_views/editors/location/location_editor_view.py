# File: infrastructure/ui/tkinter_views/editors/location/location_editor_view.py (version 0.2)
import tkinter as tk
from typing import Any, Dict
from ...base_editor_view import BaseEditorView
from .location_editor_controls import LocationEditorControls


class LocationEditorView(BaseEditorView):
    """
    Основной класс View для редактора локаций.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, app)
        self.controls = None
        self.location_canvas = None
        self._setup_ui()
        self._set_initial_data()  # <-- Добавлен вызов для установки начальных данных

    def _setup_ui(self):
        self.three_panel_layout()

        self.controls = LocationEditorControls(self.right_frame, self)
        self.controls.pack(fill=tk.BOTH, expand=True)

        self.location_canvas = tk.Canvas(self.center_frame, bg="#222222", highlightthickness=0)
        self.location_canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        self._create_context_menu_for_canvas(self.location_canvas)
        self.bind_show_code_command(self._show_code_preview_window)

    def _set_initial_data(self):
        """Устанавливает базовые значения при запуске редактора."""
        # TODO: Реализовать метод для установки данных в LocationEditorControls
        self.controls.entry_block_key.delete(0, tk.END)
        self.controls.entry_block_key.insert(0, "new_location_key")
        self.controls.entry_display_name.delete(0, tk.END)
        self.controls.entry_display_name.insert(0, "Новая Локация")

    def get_form_data(self) -> Dict[str, Any]:
        # TODO: Реализовать получение данных из формы
        return {}