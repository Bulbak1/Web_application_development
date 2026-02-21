import timeit

def process_list(arr):
    if not (1 <= len(arr) <= 10**3):
        return "Error"
    result = []
    for i in arr:
        if i % 2 == 0:
            result.append(i**2)
        else:
            result.append(i**3)
    return result

def process_list_lc(arr):
    if not (1 <= len(arr) <= 10**3):
        return "Error"
    
    return [i**2 if i % 2 == 0 else i**3 for i in arr]

def process_list_gen(arr):
    if not (1 <= len(arr) <= 10**3):
        yield "Error"
        return
    
    for i in arr:
        if i % 2 == 0:
            yield i**2
        else:
            yield i**3

if __name__ == '__main__':
    arr = list(range(1, 1001))
    
    time_regular = timeit.timeit(lambda: process_list(arr), number=100)
    
    time_lc = timeit.timeit(lambda: process_list_lc(arr), number=100)
    
    time_gen = timeit.timeit(lambda: list(process_list_gen(arr)), number=100)
    
    print(f"Обычная функция: {time_regular:.6f} сек на 100 запусков")
    print(f"List comprehension: {time_lc:.6f} сек на 100 запусков")
    print(f"Генератор (с преобразованием в список): {time_gen:.6f} сек на 100 запусков")

    #Обычная функция: 0.009139 сек на 100 запусков
    #List comprehension: 0.008357 сек на 100 запусков
    #Генератор (с преобразованием в список): 0.010053 сек на 100 запусков