cities = ["Keffi", "Abuja", "Kano"]
print(cities)
#adding a city to the list
cities.append("Lagos")
print(cities)
# Removing a city from the list
cities.remove("Kano")
print(cities)
for city in cities:
    print("I want to visit", city)