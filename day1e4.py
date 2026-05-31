name = input("What is your name? ")
print (name)
age = int(input("How old are you? "))
if age < 18:
    print ("You are too young to vote.")
elif age >= 18 and age <= 60:
    print ("You are eligible to vote.")
else:    print ("You are a senior citizen.")