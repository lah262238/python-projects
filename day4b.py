patient = {
    "name": "Abdulkadir",
    "age": 30,
    "blood group": "O+",
    "diagnosis": "Healthy",
}
for key, value in patient.items():
    print(key, ":", value)
print(patient["name"])
print(patient["age"])  
print(patient["blood group"])
print(patient["diagnosis"])