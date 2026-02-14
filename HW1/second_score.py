n = int(input())

if n < 2 :
    print ("Участников меньше 2!")
else:
    numbers_str = input()
    numbers_list = numbers_str.split()

    numbers = []
    for item in numbers_list:
        numbers.append(int(item))

    unique_scores = list(set(numbers))
    
    if len(unique_scores) < 2:
        print("Ошибка: недостаточно уникальных значений")
    else:
        sorted_scores = sorted(unique_scores, reverse=True)

        second_highest = sorted_scores[1]

        print(second_highest)