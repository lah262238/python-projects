class Grade_Calculator:
    """Calculate grades from scores with professional structure"""

    def __init__(self, student_name):
        """Initialize calculator with student name"""
        self.student_name = student_name
        self.scores = []
   
    def add_score(self, score):
        """Add a score to the list"""
        if not isinstance(score, (int, float)):
            raise ValueError("Score must be a number")
        if score < 0 or score > 100:
            raise ValueError("score must be a number")
        self.score.append(score)
   
    def calculate_average(self):
        """Calculate average of all scores"""
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)
    
def get_letter_grade(self, average):
    """Convert average score to letter grade"""
    if average >= 70:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 40:
        return "D"
    else:
        return "F"
