# File: infrastructure/persistence/initializer.py
from .json_node_repository import JsonNodeRepository
from .json_block_repository import JsonBlockRepository
from .json_location_repository import JsonLocationRepository
from .json_tag_repository import JsonTagRepository
from .json_module_repository import JsonModuleRepository
from .json_raw_location_repository import JsonRawLocationRepository


class RepositoryInitializer:
    """
    Класс для централизованной инициализации всех репозиториев.
    """
    def __init__(self):
        self.node = JsonNodeRepository()
        self.block = JsonBlockRepository()
        self.location = JsonLocationRepository()
        self.tag = JsonTagRepository()
        self.module = JsonModuleRepository()
        self.raw_location = JsonRawLocationRepository()