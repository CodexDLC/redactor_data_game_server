import json
from typing import Dict, Any
from interfaces.persistence.i_schema_repository import ISchemaRepository

class JsonSchemaRepository(ISchemaRepository):
    _FILE_PATH = "data/node_schema.json"

    def get_node_schema(self) -> Dict[str, Any]:
        try:
            with open(self._FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Возвращаем пустую схему в случае ошибки
            return {"common_properties": {}, "type_specific_properties": {}}