# File Sorter
Утилита для автоматической сортировки файлов по расширениям.

## Установка
1. Python версии 3.6 и выше  
2. Установка зависимостей `pip install -r requirements.txt`

## Команды
`python main init <config_path>` - Создание базового конфига  
`python main sort <config_path>` - Запуск сортировки

## Использование

### 1. Создание конфига
`python main.py init <config_path>`

### 2. Настройка конфига
Откройте `<config_path>.yaml` и отредактируйте под ваши настройки:
```
default:
  delete_unsorted: false
  final_path: 'test'
  initial_path: 'test'
  sort:
  - text
text:
  extensions:
  - '*.txt'
  save_dir: /text
```
**delete_unsorted** - Удалять файлы не подходящие под правила  
**final_path** - Куда сохранять отсортированные файлы  
**initial_path** - Откуда брать файлы для сортировки  
**sort** - Список категорий для сортировки

Для каждой категории:  
**extensions** - расширение файлов (\*.расширение)  
**save_dir** - подпапка для сохранения

### 3. Сортировка файлов
`python main.py sort <config_path>`