def compute_average_scores(scores):
    if not scores:
        return "Error"
    
    # Проверка количества X
    if len(scores) > 100:
        return "Error"
    
    # Проверка количества N
    num_students = len(scores[0])
    if num_students <= 0 or num_students > 100:
        return "Error"
    
    for subject_scores in scores:
        if len(subject_scores) != num_students:
            return "Error"

    averages = []
    for i in range(num_students):
        total = sum(score[i] for score in scores)
        avg = total / len(scores)
        averages.append(avg)
    
    return tuple(averages)

if __name__ == '__main__':
    n, x = map(int, input().split())
    scores = []
    for _ in range(x):
        scores.append(tuple(map(float, input().split())))

    result = compute_average_scores(scores)
    
    if result == "Error":
        print("Error")
    else:
        for avg in result:
            print(f"{avg:.1f}")