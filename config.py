import os
import yaml

from pathlib import Path
from logger import setup_logger
from typing import Dict, Any, Optional

logger = setup_logger()

class Config:
    """Класс для управления конфигурационными файлами"""
    
    defaul_config: Dict[str, Any] = {
        'default': {
            'final_path': '',
            'initial_path': '',
            'delete_unsorted': False,
            'sort': ['text']
        },
        'text': {
            'save_dir': '/text',
            'extensions': ['*.txt']
        }
    }

    @classmethod
    def create_config(cls, config_name: str = 'sort_config') -> bool:
        """
        Создает YAML файл конфигурации

        Args:
            config_name (str): Название файла конфигурации

        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            config_path: Path = Path(f'{config_name}.yaml')

            if config_path.exists():
                logger.warning(f'Конфигурационный файл {config_path} уже существует')
                return False

            with open(config_path, 'w', encoding='utf-8') as file:
                yaml.dump(cls.defaul_config, file, allow_unicode=True, default_flow_style=False)

            logger.info(f'Конфигурационный файл создан: {config_path}')
            return True

        except Exception as e:
            logger.error(f'Ошибка при создании конфигурации: {e}')
            return False

    @classmethod
    def load_config(cls, config_name: str = 'sort_config') -> Optional[Dict[str, Any]]:
        """
        Загружает конфигурацию из YAML файла

        Args:
            config_name (str): Название файла конфигурации

        Returns:
            Dict: Загруженная конфигураци или None при ошибке
        """
        try:
            config_path: Path = Path(f'{config_name}.yaml')

            if not config_path.exists():
                config_path = Path(config_name)
                if not config_path.exists():
                    logger.error(f'Конфигурационный файл не найден: {config_name}')
                    return None

            with open(config_path, 'r', encoding='utf-8') as file:
                config: Dict[str, Any] = yaml.safe_load(file)

            logger.info(f'Конфигурация загружена из: {config_path}')
            return config

        except Exception as e:
            logger.error(f'Ошибка при загрузке конфигурации: {e}')
            return None
