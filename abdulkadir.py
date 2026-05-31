import datetime
name = "Abdulkadir"
age = 30
country = "Nigeria"
today = datetime.date.today()
print ("My name is", name)
print ("My age is", age, "years old")
print ("My country is", country)
print ("Today's date is", today)
name = input("What is your name? ")
age = input("How old are you? ")
print ("Hello", name)
print ("You are", age, "years old")
full_name = "Lawal Abdulkadir Hassan"
print ("My full name is", full_name)
working_place = input ("Where are you working? ")
print ("You are working at", working_place)

age = int(input("How old are you? "))
if age >= 18:
    print ("You are an adult.")
else:    print ("You are not an adult.")