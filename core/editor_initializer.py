# File: core/editor_initializer.py
from typing import Any

from infrastructure.ui.tkinter_views.editors.block.block_editor_body import BlockEditorBody
from infrastructure.ui.tkinter_views.editors.location.location_editor_body import LocationEditorBody # ИЗМЕНЕНИЕ: Используем новый класс
from infrastructure.ui.tkinter_views.editors.prebuffer.prebuffer_editor_body import PrebufferEditorBody
from core.block_editor.block_editor_service import BlockEditorService
from core.location_editor.location_editor_service import LocationEditorService # ИЗМЕНЕНИЕ: Сервис для новой логики
from core.prebuffer_editor.prebuffer_editor_service import PrebufferEditorService


class EditorInitializer:
    def __init__(self, app: Any):
        self.app = app

    def create_block_editor(self):
        view = BlockEditorBody(self.app.body_container, self.app)
        service = BlockEditorService(view=view, repository=self.app.repos.block,
                                     node_repo=self.app.repos.node, app=self.app)
        view.set_service(service)
        return view

    def create_location_editor(self):
        # ИЗМЕНЕНИЕ: Создаем новый редактор локаций
        view = LocationEditorBody(self.app.body_container, self.app)
        service = LocationEditorService(view=view, app=self.app)
        view.set_service(service)
        return view

    def create_prebuffer_editor(self):
        view = PrebufferEditorBody(self.app.body_container, self.app)
        service = PrebufferEditorService(view=view, block_repo=self.app.repos.block,
                                         node_repo=self.app.repos.node, app=self.app,
                                         prebuffer_template_repo=self.app.repos.prebuffer_template,
                                         prebuffer_object_repo=self.app.repos.prebuffer_object)
        view.set_service(service)
        return view