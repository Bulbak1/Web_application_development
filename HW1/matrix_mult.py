# размерность матрицы
n = int(input())

if 2 <= n <= 10:
    A = []
    for _ in range(n):
        row = list(map(int, input().split()))
        A.append(row)

    B = []
    for _ in range(n):
        row = list(map(int, input().split()))
        B.append(row)

    C = []
    for i in range(n):           
        row = []                  
        for j in range(n):        
            total = 0 
            for k in range(n):
                total += A[i][k] * B[k][j]
            row.append(total)
        C.append(row)

    for row in C:
        print(' '.join(map(str, row)))
else:
    print("Error")