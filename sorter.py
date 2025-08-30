import os
import shutil

from pathlib import Path
from fnmatch import fnmatch
from logger import setup_logger
from typing import Optional, Dict, Any, List

logger = setup_logger()

class Sorter:
    """Класс для сортировки файлов"""

    def __init__(self, config: Dict[str, Any]):
        """
        Инициализация сортировщика файлов

        Args:
            config (dict): Конфигурация для сортировки
        """
        self.config = config
        self.initial_path = Path(config['default']['initial_path'])
        self.final_path = Path(config['default']['final_path'])
        self.delete_unsorted = bool(config['default']['delete_unsorted'])

    def _get_file_type(self, filename: str) -> Optional[str]:
        """
        Определяет тип файла

        Args:
            filename (str): Имя файла

        Returns:
            str: Название типа или None если не найдено
        """
        for type, settings in self.config.items():
            if type == 'default':
                continue

            extensions = settings.get('extensions', [])
            for pattern in extensions:
                if fnmatch(filename, pattern):
                    return type

        return None

    def sort_files(self) -> bool:
        """
        Выполняет сортировку файлов

        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            if not self.initial_path.exists():
                logger.error(f'Исходная директория не существует: {self.initial_path}')
                return False

            self.final_path.mkdir(parents=True, exist_ok=True)

            processed = 0
            sorted_count = 0
            unsorted_count = 0

            for file_path in self.initial_path.iterdir():
                if file_path.is_file():
                    processed += 1
                    type = self._get_file_type(file_path.name)
                    
                    if type:
                        type_settings = self.config[type]
                        save_dir: Path = self.final_path / type_settings['save_dir'].lstrip('/')
                        
                        save_dir.mkdir(parents=True, exist_ok=True)
                        
                        destination: Path = save_dir / file_path.name
                        shutil.move(str(file_path), str(destination))
                        sorted_count += 1
                        logger.info(f'Отсортирован: {file_path.name} -> {save_dir}')
                    
                    else:
                        unsorted_count += 1
                        logger.warning(f'Не удалось определить категорию для: {file_path.name}')
                        
                        if self.delete_unsorted:
                            file_path.unlink()
                            logger.info(f'Удален неотсортированный файл: {file_path.name}')
            
            logger.info(
                f'Сортировка завершена. '
                f'Обработано: {processed}, '
                f'Отсортировано: {sorted_count}, '
                f'Не отсортировано: {unsorted_count}'
            )
            
            return True
            
        except Exception as e:
            logger.error(f'Ошибка при сортировке файлов: {e}')
            return False