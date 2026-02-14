n, m = map(int, input().split())

if 1 <= n <= 10**5 and 1 <= m <= 10**5:
    arr = list(map(int, input().split()))
    A = set(map(int, input().split()))
    B = set(map(int, input().split()))
    
    # Проверка длины массива
    if len(arr) != n:
        print("Error")
    # Проверка размеров множеств
    elif len(A) != m or len(B) != m:
        print("Error")
    # Проверка диапазона элементов массива
    elif not all(1 <= x <= 10**9 for x in arr):
        print("Error")
    # Проверка диапазона элементов A
    elif not all(1 <= x <= 10**9 for x in A):
        print("Error")
    # Проверка диапазона элементов B
    elif not all(1 <= x <= 10**9 for x in B):
        print("Error")
    # Проверка на непересекаемость множеств
    elif A & B:
        print("Error")
    else:
        happiness = 0
        for i in arr:
            if i in A:
                happiness += 1
            elif i in B:
                happiness -= 1
        print(happiness)
else:
    print("Error")