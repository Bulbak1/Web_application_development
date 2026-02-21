def wrapper(f):
    def fun(l):
        formatted = []
        for phone in l:
            # Удаляем все нецифровые символы
            digits = ''.join(filter(str.isdigit, phone))
            
            if len(digits) >= 10:
                digits = digits[-10:]
            
            formatted_phone = f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}"
            formatted.append(formatted_phone)
        # Вызываем исходную функцию сортировки с отформатированными номерами
        return f(formatted)
    return fun

@wrapper
def sort_phone(l):
    return sorted(l)

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')
