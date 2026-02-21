import sys

def my_sum(*args):
    return sum(args)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Ошибка: не переданы числа")
        sys.exit(1)

    try:
        numbers = [float(x) for x in sys.argv[1:]]
        result = my_sum(*numbers)
        if result.is_integer():
            print(int(result))
        else:
            print(result)
    except ValueError:
        print("Ошибка: все аргументы должны быть числами")
        sys.exit(1)