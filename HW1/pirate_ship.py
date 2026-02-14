n, m = map(int, input().split())
items = []

for _ in range(m):
    name, w, v = input().split()
    w, v = int(w), int(v)
    items.append((name, w, v, v / w))

items.sort(key=lambda x: x[3], reverse=True)

space = n
for name, w, v, ratio in items:
    if space == 0:
        break
    if w <= space:
        print(f"{name} {w} {v}")
        space -= w
    else:
        print(f"{name} {space} {ratio * space:.2f}")
        space = 0