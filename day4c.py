# writing to a file
file = open("myfile.txt", "w")
file.write("My name is Abdulkadir\n")
file.write("I am learning Python\n")
file.write("My goal is AI Engineering\n")
file.close()
print("file saved successfully")

# Reading from a file
file = open("myfile.txt", "r")
content = file.read()
print(content)
file.close()