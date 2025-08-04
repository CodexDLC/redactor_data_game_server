# File: core/node_editor/node_editor_service.py (version 0.7)
from interfaces.persistence.i_node_repository import INodeRepository
from interfaces.ui.i_node_editor_view import INodeEditorView
from interfaces.ui.i_nodes_panel_view import INodesPanelView
from typing import Any


class NodeEditorService:
    def __init__(self, view: INodeEditorView, nodes_panel: INodesPanelView, repository: INodeRepository, app: Any):
        self.view = view
        self.nodes_panel = nodes_panel
        self.repository = repository
        self.app = app
        self.current_node_key = None

        self.view.bind_save_command(self._save_node)
        self.view.bind_delete_command(self._delete_node)
        self.view.bind_new_command(self._new_node)
        self.view.bind_canvas_click(self.on_canvas_click_to_edit)

        self.nodes_panel.bind_list_selection_command(self.on_node_selected_from_list)

    def on_node_selected_from_list(self, event=None):
        selected_key = self.nodes_panel.get_selected_node_key()
        if selected_key:
            node_data = self.repository.get_by_key(selected_key)
            if node_data:
                full_data = node_data.copy()
                full_data['node_key'] = selected_key
                self.app.set_active_brush_node(full_data)

    def on_canvas_click_to_edit(self, event=None):
        active_brush = self.app.get_active_brush_node()
        if active_brush:
            self.view.set_form_data(active_brush)
            self.current_node_key = active_brush['node_key']
            print(f"Нода '{self.current_node_key}' загружена для редактирования.")
            self.app.unselect_active_brush_node()
        else:
            print("Ошибка: Активная нода-кисточка не выбрана.")

    def _save_node(self) -> None:
        data = self.view.get_form_data()
        node_key = data.get("node_key")

        if not node_key:
            print("Ошибка: Ключ ноды не может быть пустым.")
            return

        node_data_to_save = data.copy()
        del node_data_to_save["node_key"]

        self.repository.upsert(node_key, node_data_to_save)
        print(f"Нода '{node_key}' сохранена.")
        self.nodes_panel.update_node_list()

    def _delete_node(self) -> None:
        node_key = self.nodes_panel.get_selected_node_key()
        if node_key:
            self.repository.delete(node_key)
            self.nodes_panel.update_node_list()
            self.view.clear_form()
            print(f"Нода '{node_key}' успешно удалена.")

    def _new_node(self) -> None:
        self.view.clear_form()