def find_second_lowest():
    n = int(input())
    
    if n < 2 or n > 5:
        print("Ошибка: количество студентов должно быть от 2 до 5")
        return
    
    records = []
    
    for _ in range(n):
        name = input()
        score = float(input())
        records.append([name, score])
    
    unique_scores = sorted(set(score for _, score in records))

    if len(unique_scores) < 2:
        print("Ошибка: недостаточно уникальных оценок")
        return
    
    second_lowest = unique_scores[1]
    
    second_lowest_students = [name for name, score in records if score == second_lowest]
    
    second_lowest_students.sort()
    
    for student in second_lowest_students:
        print(student)


if __name__ == "__main__":
    find_second_lowest()