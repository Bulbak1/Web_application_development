import sys
import os

if __name__ == '__main__':
    filename = sys.argv[1]
    found = False

    for root, dirs, files in os.walk('.'):
        if filename in files:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines[:5]:
                        print(line, end='')
                    found = True
                    break
            except:
                try:
                    with open(file_path, 'r', encoding='cp1251') as f:
                        lines = f.readlines()
                        for line in lines[:5]:
                            print(line, end='')
                        found = True
                        break
                except:
                    print(f"Файл {filename} найден, но не удаётся прочитать")
                    found = True
                    break

    if not found:
        print(f"Файл {filename} не найден")