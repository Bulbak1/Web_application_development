import csv

def main():
    try:
        with open('products.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            adult_sum = 0.0  # Взрослый
            senior_sum = 0.0  # Пенсионер
            child_sum = 0.0   # Ребенок
            
            for row in reader:
                # row - это словарь, где ключи - названия столбцов из заголовка
                adult_sum += float(row['Взрослый'])
                senior_sum += float(row['Пенсионер'])
                child_sum += float(row['Ребенок'])
            
            print(f"{adult_sum:.2f} {senior_sum:.2f} {child_sum:.2f}")
    except FileNotFoundError:
        print("Файл products.csv не найден")

if __name__ == '__main__':
    main()