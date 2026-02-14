def main():
    try:
        with open('example.txt', 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print("Файл example.txt не найден")
        return

    # Разбиваем текст на слова, состоящие только из букв
    words = []
    current = []
    for char in text:
        if char.isalpha():
            current.append(char)
        else:
            if current:
                words.append(''.join(current))
                current = []
    if current:
        words.append(''.join(current))

    if not words:
        return

    max_len = max(len(w) for w in words)
    max_words = [w for w in words if len(w) == max_len]

    print('\n'.join(max_words))

if __name__ == '__main__':
    main()