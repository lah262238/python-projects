fruits = ["apple", "banana", "cherry"]
print(fruits)
print(fruits[0])
print(fruits[2])
print(len(fruits))
for fruit in fruits:
    print("I like", fruit)
friends = ["Ali", "Musa", "Fatima"]
# Add to the list
friends.append("Hassan")
print(friends)
# Remove from the list
friends.remove("Musa")
print(friends)         
# cheeck if something is in the list
if "Ali" in friends:
    print("Ali is my friend")
#sort the list
friends.sort()
print(friends)