import os


def get_unique_filename(filename):
    # Извлекаем имя и расширение файла
    base, extension = os.path.splitext(filename)
    counter = 1

    # Проверяем, существует ли файл
    while os.path.exists(filename):
        # Создаем новое имя файла с суффиксом
        filename = f"{base[:-1]}{counter}{extension}"
        counter += 1

    return filename
