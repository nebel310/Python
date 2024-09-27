import os

'''
Этот бот нумерует все файлы в папке по порядку (1, 2, 3, 4... и т.д.)

Просто скопируйте путь до файлов в переменную path

'''

path = "PATH"  # Вставить путь до файлов
counter = 1
for filename in os.listdir(path):
    if not filename.startswith('.'):  # Строчка, которая будет игнорировать скрытые файлы
        extension = os.path.splitext(filename)[1]
        new_filename = str(counter) + extension
        os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
        counter += 1