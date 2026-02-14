n = int(input())
passengers = []

for i in range(n):
    a, b = map(int, input().split())
    
    if a >= b:
        print(f"Ошибка: время входа ({a}) должно быть меньше времени выхода ({b})")
        exit()
    
    passengers.append((a, b))

t = int(input())

count = 0
for a, b in passengers:
    if a <= t <= b:
        count += 1

print(count)