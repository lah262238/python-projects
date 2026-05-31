# Expense tracking with predefined items and amounts
names = []
Amounts = []
name = input("Enter the name of the expense (or type 'done' to finish): ")
while name.lower() != 'done':
    names.append(name)
    try:
        amount = float(input("Enter the amount for this expense: "))
        Amounts.append(amount)
    except ValueError:
        print("Invalid amount. Please enter a number.")
    name = input("Enter the name of the expense (or type 'done' to finish): ")
total = sum(Amounts)
print("Total expenses:", total)
max_expenses = max(Amounts)
print("Maximum expense:", max_expenses)
for i in range(len(names)):
    if Amounts[i] == max_expenses:
        print("Expense with the maximum amount:", names[i], "with amount", Amounts[i])
# Budget Status
if total_budget := 10000:
    if total > total_budget:
        print("Over budget! You have exceeded your budget by:", total - total_budget)
    else:
        print("You are within your budget. Remaining budget:", total_budget - total)

# Save results to a file
file = open("expenses.txt", "w")
file.write("Total expenses: " + str(total) + "\n")
file.write("Maximum expense: " + str(max_expenses) + "\n")
for i in range(len(names)):
    file.write(names[i] + ": " + str(Amounts[i]) + "\n")
file.close()
print("Results saved to expenses.txt")