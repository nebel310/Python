import os
import pyperclip

# Глобальные списки исключений
DEFAULT_EXCLUDE_DIRS = [
    '.git',
    '__pycache__',
    'venv',
    'node_modules',
    'dist', 'build',
    'frontend_react',
    '.venv',
    '.vscode',
    '.idea'
]

DEFAULT_EXCLUDE_FILES = [
    '.gitignore',
    'README.md',
    'Thumbs.db',
    'desktop.ini'
]

def generate_directory_tree(path, exclude_dirs=None, exclude_files=None, prefix=""):
    """Рекурсивно генерирует дерево директории"""
    if exclude_dirs is None:
        exclude_dirs = DEFAULT_EXCLUDE_DIRS
    if exclude_files is None:
        exclude_files = DEFAULT_EXCLUDE_FILES
    
    tree = ""
    items = []
    
    # Получаем все элементы в директории
    try:
        items = os.listdir(path)
    except PermissionError:
        return f"{prefix}[Отказано в доступе]\n"
    
    # Фильтруем элементы
    filtered_items = []
    for item in items:
        if item in exclude_files:
            continue
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path) and item in exclude_dirs:
            continue
        filtered_items.append(item)
    
    # Сортируем: сначала папки, потом файлы
    filtered_items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x))
    
    for i, item in enumerate(filtered_items):
        full_path = os.path.join(path, item)
        is_last = i == len(filtered_items) - 1
        
        if os.path.isdir(full_path):
            # Это папка
            tree += f"{prefix}{'└── ' if is_last else '├── '}{item}/\n"
            extension = "    " if is_last else "│   "
            tree += generate_directory_tree(full_path, exclude_dirs, exclude_files, prefix + extension)
        else:
            # Это файл
            tree += f"{prefix}{'└── ' if is_last else '├── '}{item}\n"
    
    return tree

def scan_directory(path, extensions, exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = DEFAULT_EXCLUDE_DIRS
    if exclude_files is None:
        exclude_files = DEFAULT_EXCLUDE_FILES
    
    output = "*Схема директории*\n\n"
    
    # Добавляем корневую папку
    root_name = os.path.basename(path) if os.path.basename(path) else path
    output += f"{root_name}/\n"
    
    # Генерируем дерево директории
    output += generate_directory_tree(path, exclude_dirs, exclude_files)
    
    # Добавляем разделитель
    output += "\n" + "="*50 + "\n\n"
    
    # Собираем содержимое файлов с указанными расширениями
    files_content = ""
    for root, dirs, files in os.walk(path):
        # Исключаем папки из списка
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # Исключаем файлы из списка и проверяем расширение
            if file in exclude_files:
                continue
            
            # Проверяем, имеет ли файл нужное расширение
            has_extension = False
            for ext in extensions:
                if file.endswith(f'.{ext}'):
                    has_extension = True
                    break
            
            if not has_extension:
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                rel_path = os.path.relpath(file_path, path)
                files_content += f"{rel_path}:\n```\n{content}\n```\n\n"
            except Exception as e:
                rel_path = os.path.relpath(file_path, path)
                files_content += f"{rel_path}:\n[Ошибка чтения: {e}]\n\n"
    
    output += files_content
    
    print(output)
    pyperclip.copy(output)
    print("Результат скопирован в буфер обмена!")

# Укажите путь к вашей папке здесь
path = str(input("Введите путь до папки -> "))

# Запрашиваем расширения файлов
extensions_input = str(input("Список расширений файлов (через пробел): "))
# Разделяем строку по пробелам и удаляем пустые элементы
extensions = [ext.strip() for ext in extensions_input.split() if ext.strip()]

# Если пользователь не ввел расширения, используем стандартные
if not extensions:
    extensions = ['py']
    print("Используются стандартные расширения: py")

scan_directory(path, extensions)
