import random
import math

def circle_square_mk(r, n):
    points_inside = 0
    for _ in range(n):
        x = random.uniform(-r, r)
        y = random.uniform(-r, r)
        if x*x + y*y <= r*r:
            points_inside += 1
    return (points_inside / n) * (4 * r * r)

if __name__ == '__main__':
    r = float(input())
    n = int(input())
    print(circle_square_mk(r, n))