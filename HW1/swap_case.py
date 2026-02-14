s = input()
if 0 < len(s) <= 1000:
    result = ""
    for char in s:
        if char.isupper():
            result += char.lower()
        elif char.islower():
            result += char.upper()
        else:
            result += char
    print(result)
else:
    print("Ошибка: длина строки должна быть от 1 до 1000 символов")
