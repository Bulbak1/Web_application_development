import sys
import os

if __name__ == '__main__':
    # Получаем путь к директории из аргументов командной строки
    target_dir = sys.argv[1]
    
    # Список для хранения имён файлов (без подпапок)
    file_list = []
    
    # Перебираем все элементы в указанной директории
    for element in os.listdir(target_dir):
        # Составляем полный путь
        element_path = os.path.join(target_dir, element)
        # Проверяем, является ли элемент файлом (не папкой)
        if os.path.isfile(element_path):
            file_list.append(element)
    
    # Словарь для группировки файлов по расширению
    grouped_files = {}
    
    # Распределяем файлы по группам
    for filename in file_list:
        # Определяем расширение файла
        if '.' in filename:
            # Берём всё, что после последней точки
            extension = filename.split('.')[-1]
        else:
            # Если точки нет, расширение пустое
            extension = "no_extension"
        
        # Добавляем файл в соответствующую группу
        if extension not in grouped_files:
            grouped_files[extension] = []
        grouped_files[extension].append(filename)
    
    # Сортируем расширения по алфавиту
    for ext in sorted(grouped_files.keys()):
        # Сортируем файлы внутри каждой группы
        for fname in sorted(grouped_files[ext]):
            print(fname)