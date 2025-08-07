# File: core/editor_initializer.py
from typing import Any

from infrastructure.ui.tkinter_views.editors.block.block_editor_body import BlockEditorBody
from infrastructure.ui.tkinter_views.editors.location.location_editor_view import LocationEditorView
from core.block_editor.block_editor_service import BlockEditorService
from core.location_editor.location_editor_service import LocationEditorService


class EditorInitializer:
    """
    Класс для централизованной инициализации и связывания редакторов (View и Service).
    """

    def __init__(self, app: Any):
        self.app = app

    def create_block_editor(self):
        """
        Создает View и Service для Редактора Блоков и связывает их.
        """
        view = BlockEditorBody(self.app.body_container, self.app)
        service = BlockEditorService(view=view, repository=self.app.repos.block,
                                     node_repo=self.app.repos.node, app=self.app)
        view.set_service(service)
        return view

    def create_location_editor(self):
        """
        Создает View и Service для Редактора Локаций и связывает их.
        """
        view = LocationEditorView(self.app.body_container, self.app)
        service = LocationEditorService(view=view, app=self.app)
        view.service = service
        return view