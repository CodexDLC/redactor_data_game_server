# File: infrastructure/ui/tkinter_views/editors/location/location_properties_panel.py
import tkinter as tk
from typing import Any, Dict
from ..base_properties_panel import BasePropertiesPanel
from ...styles import *


class LocationPropertiesPanel(BasePropertiesPanel):
    """
    Панель свойств для Редактора Локаций.
    """

    def __init__(self, master, app: Any):
        super().__init__(master, app)
        self.service: Any | None = None
        self._build_ui()

    def _build_ui(self):
        main_frame = tk.LabelFrame(self, text="Свойства Локации", fg=FG_TEXT, bg=BG_PRIMARY, padx=5, pady=5)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(main_frame, text="Здесь будут свойства локации", fg=FG_TEXT, bg=BG_PRIMARY).pack(pady=10)

    def set_service(self, service: Any):
        self.service = service
        # Здесь будет логика, если нужно что-то обновить после установки сервиса

    def set_data(self, location_data: Dict[str, Any]):
        # Здесь будет логика для заполнения полей данными
        pass

    def get_data(self) -> Dict[str, Any]:
        # Здесь будет логика для сбора данных из полей
        return {}