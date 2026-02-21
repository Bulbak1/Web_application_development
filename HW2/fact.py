import timeit

def fact_it(n: int) -> int:
    if n < 1 or n >= 1000:
        return "Error"
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fact_rec(n: int) -> int:
    if n < 1 or n >= 1000:
        return "Error"
    if n == 1:
        return 1
    return n * fact_rec(n - 1)

if __name__ == '__main__':
    n = 300
    number = 5000  # количество запусков для замера

    it_time = timeit.timeit(lambda: fact_it(n), number=number)
    rec_time = timeit.timeit(lambda: fact_rec(n), number=number)

    print(f"Итеративная функция: {it_time:.6f} сек на {number} запусков")
    print(f"Рекурсивная функция: {rec_time:.6f} сек на {number} запусков")
    # Комментарий: рекурсивная функция работает медленнее из-за накладных расходов
    
    #Итеративная функция: 0.134306 сек на 5000 запусков
    #Рекурсивная функция: 0.323092 сек на 5000 запусков