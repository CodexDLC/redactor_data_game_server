from abc import ABC, abstractmethod
from typing import Dict, Any

class ISchemaRepository(ABC):
    @abstractmethod
    def get_node_schema(self) -> Dict[str, Any]:
        pass