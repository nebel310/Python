import os
import pyperclip

def generate_directory_tree(path, exclude_dirs=None, exclude_files=None, prefix=""):
    """Рекурсивно генерирует дерево директории"""
    if exclude_dirs is None:
        exclude_dirs = ['.git', '__pycache__', 'venv', '.vscode', '.idea']
    if exclude_files is None:
        exclude_files = ['.gitignore', 'README.md']
    
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

def scan_directory(path, exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = ['.git', '__pycache__', 'venv', '.vscode', '.idea', 'node_modules', 'dist', 'build']
    if exclude_files is None:
        exclude_files = ['.gitignore', 'README.md', 'Thumbs.db', 'desktop.ini']
    
    output = "*Схема директории*\n\n"
    
    # Добавляем корневую папку
    root_name = os.path.basename(path) if os.path.basename(path) else path
    output += f"{root_name}/\n"
    
    # Генерируем дерево директории
    output += generate_directory_tree(path, exclude_dirs, exclude_files)
    
    # Добавляем разделитель
    output += "\n" + "="*50 + "\n\n"
    
    # Собираем содержимое .py файлов
    py_files_content = ""
    for root, dirs, files in os.walk(path):
        # Исключаем папки из списка
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # Исключаем файлы из списка и проверяем расширение
            if file in exclude_files or not file.endswith('.py'):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                rel_path = os.path.relpath(file_path, path)
                py_files_content += f"{rel_path}:\n```python\n{content}\n```\n\n"
            except Exception as e:
                rel_path = os.path.relpath(file_path, path)
                py_files_content += f"{rel_path}:\n[Ошибка чтения: {e}]\n\n"
    
    output += py_files_content
    
    print(output)
    pyperclip.copy(output)
    print("Результат скопирован в буфер обмена!")

# Укажите путь к вашей папке здесь
path = r"D:\Projects\VKTG_parser"

# Настройте исключения здесь
exclude_dirs = ['.git', '__pycache__', 'venv', 'node_modules', 'dist', 'build']
exclude_files = ['.gitignore', 'README.md', 'Thumbs.db', 'desktop.ini']

scan_directory(path, exclude_dirs, exclude_files)