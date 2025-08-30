import os
import pyperclip

def generate_tree(path, indent='', is_last=True, prefix='', ignore_list=None, ignore_hidden=False):
    """Рекурсивно генерирует дерево каталогов с игнорированием указанных папок"""
    if ignore_list is None:
        ignore_list = ['venv', '.git', '__pycache__', '.idea', 'node_modules']
    
    if not os.path.exists(path):
        return "Ошибка: путь не существует"
    
    base_name = os.path.basename(path)
    
    # Пропускаем скрытые файлы/папки если включена опция
    if ignore_hidden and base_name.startswith('.'):
        return ''
    
    # Пропускаем папки из списка игнорирования
    if base_name in ignore_list:
        return ''
    
    if indent == '':
        tree_string = prefix + base_name + '\\\n'
    else:
        tree_string = indent + ('└── ' if is_last else '├── ') + base_name + ('\\' if os.path.isdir(path) else '') + '\n'
    
    if os.path.isdir(path):
        try:
            items = sorted(os.listdir(path))
            # Фильтруем элементы по списку игнорирования и скрытые файлы
            filtered_items = []
            for item in items:
                if item in ignore_list:
                    continue
                if ignore_hidden and item.startswith('.'):
                    continue
                filtered_items.append(item)
            
            for i, item in enumerate(filtered_items):
                full_path = os.path.join(path, item)
                is_last_item = (i == len(filtered_items) - 1)
                new_indent = indent + ('    ' if is_last else '│   ')
                tree_string += generate_tree(
                    full_path, 
                    new_indent, 
                    is_last_item, 
                    '', 
                    ignore_list, 
                    ignore_hidden
                )
        except PermissionError:
            tree_string += indent + '    └── [Доступ запрещен]\n'
    
    return tree_string

if __name__ == "__main__":
    # Настройки
    IGNORE_LIST = ['venv', '.git', '__pycache__', '.idea', 'node_modules', '.vscode', 'frontend', 'test_frontend']
    IGNORE_HIDDEN = True  # Игнорировать скрытые файлы/папки
    
    #target_path = input("Введите путь к директории: ").strip().strip('"')
    target_path = 'D:\Projects\ExpoMusic'
    
    print("\nНастройки игнорирования:")
    print(f"Игнорируемые папки: {', '.join(IGNORE_LIST)}")
    print(f"Игнорировать скрытые файлы: {'Да' if IGNORE_HIDDEN else 'Нет'}")
    print("\nСтруктура директории:\n")
    
    result = generate_tree(target_path, ignore_list=IGNORE_LIST, ignore_hidden=IGNORE_HIDDEN)
    print(result)
    
    pyperclip.copy(result)
    print("Результат скопирован в буфер обмена!")
