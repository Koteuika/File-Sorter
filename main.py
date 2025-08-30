import click

from config import Config
from sorter import Sorter
from logger import setup_logger

logger = setup_logger()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', default='sort_config', help='Название конфигурационного файла')
def init(name: str):
    """Создать конфигурационный файл"""
    logger.info(f'Создание конфигурационного файла: {name}')
    success = Config.create_config(name)

    if success:
        logger.info('Конфигурация успешно создана')
    else:
        logger.error('Не удалось создать конфигурацию')

@cli.command()
@click.option('--name', default='sort_config', help='Название конфигурационного файла')
def sort(name: str):
    """Начать сортировку файлов"""
    logger.info(f'Загрузка конфигурации: {name}')
    config = Config.load_config(name)

    if not config:
        return
    if not config['default']['initial_path'] or not config['default']['final_path']:
        return

    logger.info('Запуск сортировки файлов')

    sorter = Sorter(config)
    success = sorter.sort_files()

    if success:
        logger.info('Сортировка завершена успешно')

if __name__ == '__main__':
    cli()



