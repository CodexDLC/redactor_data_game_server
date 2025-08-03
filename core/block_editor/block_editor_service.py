from interfaces.persistence.i_block_repository import IBlockRepository
from interfaces.ui.i_block_editor_view import IBlockEditorView
# Нам также понадобится доступ к нодам для палитры
from interfaces.persistence.i_node_repository import INodeRepository


class BlockEditorService:
    """
    Класс-сервис, содержащий основную бизнес-логику редактора блоков.
    """

    def __init__(self, view: IBlockEditorView, block_repo: IBlockRepository, node_repo: INodeRepository):
        self._view = view
        self._block_repo = block_repo
        self._node_repo = node_repo  # Репозиторий нод для палитры

        self._bind_commands()
        self._load_initial_data()

    def _bind_commands(self) -> None:
        """Привязывает методы этого класса к событиям в UI."""
        # self._view.bind_save_command(self._save_block)
        # self._view.bind_delete_command(self._delete_block)
        # self._view.bind_grid_click_command(self._on_grid_click)
        # self._view.bind_block_selection_command(self._on_block_selected)
        pass

    def _load_initial_data(self) -> None:
        """Загружает начальные данные и обновляет UI."""
        all_blocks = self._block_repo.get_all()
        all_nodes = self._node_repo.get_all()

        # self._view.update_block_list_in_palette(list(all_blocks.keys()))
        # self._view.update_node_palette(all_nodes)
        print("DEBUG: Block and Node data loaded for Block Editor.")

    def _save_block(self):
        """Сохраняет текущий блок."""
        # block_key = self._view.get_block_key()
        # block_data = self._view.get_block_data() # Включая структуру сетки
        # if block_key:
        #     self._block_repo.upsert(block_key, block_data)
        #     self._load_initial_data() # Обновляем список
        pass

    def _delete_block(self):
        """Удаляет выбранный блок."""
        # block_key = self._view.get_selected_block_key()
        # if block_key:
        #     self._block_repo.delete(block_key)
        #     self._load_initial_data()
        pass

    def _on_grid_click(self, row, col):
        """Обрабатывает клик по сетке."""
        # selected_node = self._view.get_selected_node_from_palette()
        # self._view.update_grid_cell(row, col, selected_node)
        pass

    def _on_block_selected(self):
        """Загружает данные выбранного блока в редакторы."""
        # block_key = self._view.get_selected_block_key()
        # if block_key:
        #     all_blocks = self._block_repo.get_all()
        #     block_data = all_blocks.get(block_key)
        #     if block_data:
        #         self._view.set_form_data(block_data)
        #         self._view.draw_grid(block_data.get('structure'))
        pass