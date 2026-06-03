class ExpenseTracker:
    """Track expenses and generate reports"""
    
    def __init__(self, budget=0):
        """Initialize tracker with optional budget"""
        self.expenses = []
        self.budget = budget
    
    def add_expense(self, name, amount):
        """Add an expense"""
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number")
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.expenses.append({"name": name, "amount": amount})
    
    def total_expenses(self):
        """Calculate total spent"""
        return sum(expense["amount"] for expense in self.expenses)
    
    def get_max_expense(self):
        """Find most expensive item"""
        if not self.expenses:
            return None
        return max(self.expenses, key=lambda x: x["amount"])
    
    def check_budget(self):
        """Check if over budget"""
        total = self.total_expenses()
        if self.budget == 0:
            return "No budget set"
        if total > self.budget:
            return f"Over budget by {total - self.budget}"
        else:
            return f"Within budget. {self.budget - total} remaining"
    
    def get_report(self):
        """Generate expense report"""
        total = self.total_expenses()
        max_expense = self.get_max_expense()
        return {
            "total": total,
            "count": len(self.expenses),
            "most_expensive": max_expense["name"] if max_expense else "No expenses",
            "budget_status": self.check_budget()
        }
    
    def display_report(self):
        """Print expense report"""
        report = self.get_report()
        print("\n--- Expense Report ---")
        print(f"Total Expenses: {report['total']}")
        print(f"Number of Items: {report['count']}")
        print(f"Most Expensive: {report['most_expensive']}")
        print(f"Budget Status: {report['budget_status']}")

# Main program with user input
tracker = ExpenseTracker(budget=int(input("Enter your budget: ")))

print("Enter expenses (type 'done' when finished):")
while True:
    name = input("Expense name (or 'done'): ").strip()
    if name.lower() == "done":
        break
    try:
        amount = float(input(f"Amount for {name}: "))
        tracker.add_expense(name, amount)
    except ValueError:
        print("Invalid amount. Please enter a number.")

tracker.display_report()
