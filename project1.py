def get_grade(score):
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "F"
    if result >= 45:
        return "Pass"
    else:
        return "Fail"
def calculate_average(scores):
    total = 0
    for s in scores:
        total = total + s  
    average = total / len(scores)
    return average
# Main program
name = input("Enter student's name: ")
scores = []
for i in range(1, 6):
    s = int(input("Enter score for subject " + str(i) + ": "))
    scores.append(s)
average_score = calculate_average(scores)
grade = get_grade(average_score)

print("Student Name:", name)
print("scores:", scores)
print("Average:", average_score)
print("Grade:", grade)
print("Result:", "Pass" if average_score >= 45 else "Fail")

