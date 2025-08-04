# File: core/node_editor/node_editor_service.py
import logging
from typing import Any

from interfaces.persistence.i_node_repository import INodeRepository
from interfaces.persistence.i_tag_repository import ITagRepository  # <--- 1. НОВЫЙ ИМПОРТ
from interfaces.ui.i_node_editor_view import INodeEditorView
from interfaces.ui.i_nodes_panel_view import INodesPanelView


class NodeEditorService:
    def __init__(self, view: INodeEditorView, nodes_panel: INodesPanelView,
                 repository: INodeRepository, tag_repository: ITagRepository, app: Any): # <--- 2. ИЗМЕНЕННЫЙ КОНСТРУКТОР
        self.view = view
        self.nodes_panel = nodes_panel
        self.repository = repository
        self.tag_repo = tag_repository  # <--- Сохраняем репозиторий тегов
        self.app = app
        self.current_node_key = None

        # --- Привязка команд ---
        self.view.bind_save_command(self._save_node)
        self.view.bind_delete_command(self._delete_node)
        self.view.bind_new_command(self._new_node)
        self.view.bind_canvas_click(self.on_canvas_click_to_edit)
        self.nodes_panel.bind_list_selection_command(self.on_node_selected_from_list)
        logging.info("NodeEditorService: Инициализация и привязка команд завершены.")

    def on_node_selected_from_list(self, event=None):
        logging.info("NodeEditorService: Вызван on_node_selected_from_list.")
        selected_key = self.nodes_panel.get_selected_node_key()
        logging.info(f"NodeEditorService: Выбран ключ из списка: {selected_key}")
        if selected_key:
            node_data = self.repository.get_by_key(selected_key)
            if node_data:
                logging.info(f"NodeEditorService: Данные для ключа '{selected_key}' найдены в репозитории.")
                full_data = node_data.copy()
                full_data['node_key'] = selected_key
                self.app.set_active_brush_node(full_data)
            else:
                logging.warning(f"NodeEditorService: Данные для ключа '{selected_key}' НЕ найдены в репозитории.")

    def on_canvas_click_to_edit(self, event=None):
        logging.info("NodeEditorService: Вызван on_canvas_click_to_edit.")
        active_brush = self.app.get_active_brush_node()
        if active_brush:
            logging.info(f"NodeEditorService: Обнаружена активная кисть. Загрузка данных в форму: {active_brush.get('node_key')}")
            self.view.set_form_data(active_brush)
            self.current_node_key = active_brush.get('node_key')
            self.app.unselect_active_brush_node()
        else:
            logging.warning("NodeEditorService: Активная кисть не выбрана, редактирование невозможно.")

    def _save_node(self) -> None:
        logging.info("NodeEditorService: Вызван _save_node.")
        data = self.view.get_form_data()
        logging.debug(f"NodeEditorService: Данные, полученные из формы: {data}")

        node_key = data.get("node_key")
        if not node_key:
            logging.error("NodeEditorService: Попытка сохранить нод без ключа (node_key). Операция отменена.")
            return

        # --- 3. НОВАЯ ЛОГИКА ДЛЯ СОХРАНЕНИЯ ТЕГА ---
        tag = data.get("tag", "").strip()
        if tag:
            logging.info(f"NodeEditorService: Добавление тега '{tag}' в библиотеку для категории 'node_tags'.")
            self.tag_repo.add_tag_to_category('node_tags', tag)
        # --- КОНЕЦ НОВОЙ ЛОГИКИ ---

        node_data_to_save = data.copy()
        if "node_key" in node_data_to_save:
            del node_data_to_save["node_key"]

        logging.info(f"NodeEditorService: Сохранение данных для ключа '{node_key}'.")
        logging.debug(f"NodeEditorService: Данные для сохранения: {node_data_to_save}")
        self.repository.upsert(node_key, node_data_to_save)
        logging.info(f"NodeEditorService: Данные для '{node_key}' успешно переданы в репозиторий.")

        logging.info("NodeEditorService: Обновление списка нодов в UI.")
        self.nodes_panel.update_node_list()
        logging.info("NodeEditorService: Нод сохранен, список обновлен.")

    def _delete_node(self) -> None:
        logging.info("NodeEditorService: Вызван _delete_node.")
        node_key = self.nodes_panel.get_selected_node_key()
        if node_key:
            logging.info(f"NodeEditorService: Удаление нода с ключом '{node_key}'.")
            self.repository.delete(node_key)
            logging.info(f"NodeEditorService: Нод '{node_key}' удален из репозитория.")
            self.nodes_panel.update_node_list()
            self.view.clear_form()
            logging.info("NodeEditorService: Форма очищена, список нодов обновлен.")
        else:
            logging.warning("NodeEditorService: Попытка удаления, но ни один нод не выбран.")

    def _new_node(self) -> None:
        logging.info("NodeEditorService: Вызван _new_node. Очистка формы.")
        self.view.clear_form()