# File: map_editor_app.py (version 0.3)
import tkinter as tk
from infrastructure.persistence.json_node_repository import JsonNodeRepository
from infrastructure.persistence.json_block_repository import JsonBlockRepository
from infrastructure.persistence.json_location_repository import JsonLocationRepository
from infrastructure.persistence.json_schema_repository import JsonSchemaRepository
from infrastructure.ui.tkinter_views.node.node_editor_view import NodeEditorView
from core.node_editor.node_editor_service import NodeEditorService
from infrastructure.ui.tkinter_views.left_panel.universal import UniversalLeftPanel

# В будущем эти константы можно вынести в config
MINIATURE_SIZE = 50
MINIATURE_PADDING = 5
DEFAULT_FONT = ("Helvetica", 10)
FRAME_WIDTH = 100


class MapEditorApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#333333")

        self.node_repo = JsonNodeRepository()
        self.block_repo = JsonBlockRepository()
        self.location_repo = JsonLocationRepository()
        self.nodes_panel_view = None

        self.left_panel = UniversalLeftPanel(
            master=self, app=self, node_repo=self.node_repo, block_repo=self.block_repo,
            location_repo=self.location_repo, miniature_size=MINIATURE_SIZE,
            miniature_padding=MINIATURE_PADDING, font=DEFAULT_FONT, frame_width=FRAME_WIDTH
        )
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        right_area_frame = tk.Frame(self, bg="#333333")
        right_area_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.menu_frame = tk.Frame(right_area_frame, bg="#222222")
        self.menu_frame.pack(fill=tk.X, side=tk.TOP)

        self.editor_container = tk.Frame(right_area_frame, bg="#333333")
        self.editor_container.pack(fill=tk.BOTH, expand=True)

        self.create_modes_menu()
        self.show_mode_selection_screen()

    def create_modes_menu(self):
        tk.Button(self.menu_frame, text="Редактор Нод", command=self.show_node_editor).pack(side=tk.LEFT, padx=5,
                                                                                            pady=2)
        tk.Button(self.menu_frame, text="Редактор Блоков", command=self.show_block_editor).pack(side=tk.LEFT, padx=5,
                                                                                                pady=2)
        tk.Button(self.menu_frame, text="Редактор Локаций", command=self.show_location_editor).pack(side=tk.LEFT,
                                                                                                    padx=5, pady=2)

    def clear_editor_container(self):
        for widget in self.editor_container.winfo_children():
            widget.destroy()

    def show_mode_selection_screen(self):
        self.clear_editor_container()
        tk.Label(self.editor_container, text="Выберите режим в меню сверху", font=("Helvetica", 16), fg="white",
                 bg="#333333").pack(expand=True)

    def show_node_editor(self):
        self.clear_editor_container()

        # 1. Создаем репозитории
        node_repository = JsonNodeRepository()
        schema_repository = JsonSchemaRepository()  # <-- Создаем загрузчик схемы

        # 2. Загружаем схему
        node_schema = schema_repository.get_node_schema()  # <-- Читаем JSON

        # 3. Создаем View, передавая ему схему
        view = NodeEditorView(self.editor_container, self, schema=node_schema)  # <-- Передаем схему в UI

        # 4. Создаем сервис
        service = NodeEditorService(
            view=view,
            nodes_panel=self.left_panel.nodes_panel,
            repository=node_repository
        )

        view.pack(fill=tk.BOTH, expand=True)

    def show_block_editor(self):
        self.clear_editor_container()
        tk.Label(self.editor_container, text="Редактор Блоков (в разработке)", font=("Helvetica", 16), fg="white",
                 bg="#333333").pack(expand=True)

    def show_location_editor(self):
        self.clear_editor_container()
        tk.Label(self.editor_container, text="Редактор Локаций (в разработке)", font=("Helvetica", 16), fg="white",
                 bg="#333333").pack(expand=True)