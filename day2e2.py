secret = 7
guess = int(input("Guess the secret number: "))
while guess != secret:
    print("Wrong guess. Try again.")
    guess = int(input("Guess the secret number: "))
print("Correct!")    