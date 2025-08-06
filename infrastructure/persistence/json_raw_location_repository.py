import json
import os
from typing import Dict, Any, Optional
from interfaces.persistence.i_raw_location_repository import IRawLocationRepository


class JsonRawLocationRepository(IRawLocationRepository):
    """
    Конкретная реализация репозитория для временного файла-черновика.
    """
    _FILE_PATH = "session.tmp.json"

    def upsert(self, location_data: Dict[str, Any]) -> None:
        """
        Сохраняет или обновляет данные всей локации в едином временном файле.
        """
        with open(self._FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(location_data, f, indent=4, ensure_ascii=False)

    def load(self) -> Optional[Dict[str, Any]]:
        """
        Загружает данные локации из временного файла.
        Возвращает None, если файл не существует.
        """
        if not os.path.exists(self._FILE_PATH):
            return None
        try:
            with open(self._FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def delete(self) -> None:
        """
        Удаляет временный файл-черновик.
        """
        if os.path.exists(self._FILE_PATH):
            os.remove(self._FILE_PATH)