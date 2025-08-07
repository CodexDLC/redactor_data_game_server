# File: core/location_editor/location_editor_service.py
import logging
from typing import Any, Dict, Optional
import copy


class LocationEditorService:
    """
    Основной класс-сервис, управляющий всей логикой Редактора Локаций.
    """

    def __init__(self, view: Any, app: Any):
        self.view = view
        self.app = app
        self.current_location_data: Optional[Dict[str, Any]] = None
        self._bind_commands()
        logging.info("LocationEditorService: Сервис инициализирован.")
        self.new_location()

    def _bind_commands(self):
        """Привязывает методы сервиса к кнопкам в UI."""
        self.view.bind_save_command(self.save_location)
        self.view.bind_delete_command(self.delete_location)
        self.view.bind_new_command(self.new_location)
        self.view.bind_expand_command(self.expand_location)
        logging.debug("LocationEditorService: Команды управления привязаны.")

    def new_location(self):
        """Создает новую, пустую локацию для редактирования."""
        logging.info("LocationEditorService: Создание новой локации (уровень 0)...")
        self.current_location_data = {
            "location_id": "new_location",
            "root_module": self._create_void_module(0)
        }
        self.view.clear_form()
        self.view.set_form_data(self.current_location_data)
        logging.info("LocationEditorService: Новая локация успешно создана и отображена.")

    def expand_location(self):
        """
        Увеличивает уровень вложенности карты, помещая текущую карту
        в центр новой, более крупной карты.
        """
        logging.info("LocationEditorService: Получен запрос на увеличение масштаба.")
        current_root = self.current_location_data.get("root_module", {})
        current_level = current_root.get("level", 0)
        logging.info(f"LocationEditorService: Текущий уровень: {current_level}.")

        # --- ИЗМЕНЕНИЕ ЗДЕСЬ: Ограничиваем расширение одним уровнем ---
        if current_level >= 1:
            logging.warning(
                f"LocationEditorService: Достигнут максимальный уровень вложенности (1). Операция отменена.")
            self.app.set_status_message("Ошибка: Достигнут максимальный уровень вложенности.", is_error=True)
            return

        logging.info(f"LocationEditorService: Расширение карты до уровня {current_level + 1}.")
        central_module_instance = copy.deepcopy(current_root)
        new_blocks_data = {}
        for r in range(3):
            for c in range(3):
                block_key = f"{r}_{c}"
                if r == 1 and c == 1:
                    new_blocks_data[block_key] = central_module_instance
                else:
                    new_blocks_data[block_key] = self._create_void_module(current_level)

        new_root_module = {
            "level": current_level + 1,
            "structure": [[f"{r}_{c}" for c in range(3)] for r in range(3)],
            "blocks_data": new_blocks_data
        }
        self.current_location_data["root_module"] = new_root_module
        self.app.set_status_message(f"Карта расширена до уровня {current_level + 1}.")
        self.view.set_form_data(self.current_location_data)
        logging.info("LocationEditorService: Карта успешно расширена.")

    def on_node_selected(self, global_row: int, global_col: int):
        """Обрабатывает выбор ноды на холсте."""
        logging.info(f"LocationEditorService: Получен клик по холсту в координатах ({global_row}, {global_col}).")
        active_brush = self.app.get_active_brush()
        root_module = self.current_location_data.get("root_module", {})

        if active_brush and active_brush[0] == "block":
            brush_data = active_brush[1]
            logging.info(
                f"LocationEditorService: Активна кисточка-блок '{brush_data.get('block_key')}'. Запускаем замену блока...")
            self._apply_brush_recursive(root_module, global_row, global_col, brush_data)
            self.view.set_form_data(self.current_location_data)
            logging.info("LocationEditorService: Применение кисти завершено, холст обновлен.")
        else:
            logging.info("LocationEditorService: Кисточка не активна. Определяем путь для отображения...")
            display_path, _ = self._find_display_path(root_module, global_row, global_col)
            if display_path:
                self.view.controls.update_path_display(display_path)
                logging.info(f"LocationEditorService: Путь для отображения: {display_path}")
            else:
                logging.warning(
                    f"LocationEditorService: Не удалось построить путь для координат ({global_row}, {global_col}).")

    def _apply_brush_recursive(self, current_module: Dict, target_row: int, target_col: int, brush_data: Dict):
        """Рекурсивно находит и заменяет блок на данные из кисточки."""
        level = current_module.get('level', 0)
        child_size_nodes = 3 ** level

        child_row = target_row // (child_size_nodes * 3)
        child_col = target_col // (child_size_nodes * 3)
        child_key = f"{child_row}_{child_col}"

        logging.debug(f"ApplyBrush (L:{level}): Ищем дочерний элемент с ключом '{child_key}'")
        child_item = current_module.get("blocks_data", {}).get(child_key)
        if not child_item:
            logging.error(f"ApplyBrush (L:{level}): Дочерний элемент '{child_key}' не найден в blocks_data.")
            return

        if 'level' in child_item:
            logging.debug(f"ApplyBrush (L:{level}): Элемент '{child_key}' - модуль. Уходим в рекурсию.")
            remaining_row = target_row % (child_size_nodes * 3)
            remaining_col = target_col % (child_size_nodes * 3)
            self._apply_brush_recursive(child_item, remaining_row, remaining_col, brush_data)
        else:
            logging.info(f"ApplyBrush (L:{level}): Дошли до блока '{child_key}'. Заменяем его данными кисточки.")
            new_block_instance = copy.deepcopy(brush_data)
            new_block_instance.pop('block_key', None)
            current_module['blocks_data'][child_key] = new_block_instance

    def _find_display_path(self, current_module: Dict, target_row: int, target_col: int, path=None) -> (list, dict):
        """Находит путь к ноде для отображения в UI (не для модификации)."""
        if path is None: path = []
        level = current_module.get('level', 0)
        child_size_nodes = 3 ** level

        child_row = target_row // (child_size_nodes * 3)
        child_col = target_col // (child_size_nodes * 3)
        child_key = f"{child_row}_{child_col}"

        child_item = current_module.get("blocks_data", {}).get(child_key)
        if not child_item: return [], None

        path.append(("Модуль" if 'level' in child_item else "Блок", child_key))

        if 'level' in child_item:
            remaining_row = target_row % (child_size_nodes * 3)
            remaining_col = target_col % (child_size_nodes * 3)
            return self._find_display_path(child_item, remaining_row, remaining_col, path)
        else:
            local_node_row = (target_row % (child_size_nodes * 3)) // child_size_nodes
            local_node_col = (target_col % (child_size_nodes * 3)) // child_size_nodes
            node_key = f"{local_node_row}_{local_node_col}"
            path.append(("Нода", node_key))
            return path, child_item

    def _create_void_module(self, level: int) -> Dict[str, Any]:
        """Создает пустой модуль-заполнитель."""
        logging.debug(f"Создание 'пустого' модуля уровня {level}.")
        structure = [[f"{r}_{c}" for c in range(3)] for r in range(3)]
        blocks_data = {}
        if level == 0:
            for key in [item for sublist in structure for item in sublist]:
                blocks_data[key] = {"template_key": "void"}
        else:
            for key in [item for sublist in structure for item in sublist]:
                blocks_data[key] = self._create_void_module(level - 1)

        return {"level": level, "structure": structure, "blocks_data": blocks_data}

    def save_location(self):
        """Сохраняет текущую локацию."""
        logging.info("LocationEditorService: Команда 'Сохранить' вызвана.")
        pass

    def delete_location(self):
        """Удаляет текущую локацию."""
        logging.info("LocationEditorService: Команда 'Удалить' вызвана.")
        pass