student = {
    "name": "Abdulkadir",
    "age": 30,
    "city": "Keffi",
    "course": "AI Engineering"
}
print(student["name"])
print(student["age"])
print(student["city"])
print(student["course"])
# Add a new item
student["grade"] = "A"
print(student) 
# Update an existing item
student["city"] = "Abuja"
print(student["city"])
# Remove an item
del student["age"]
print(student)
#loop through the dictionary
for key, value in student.items():
    print(key, ":", value)