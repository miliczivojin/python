def odd_or_even():
    print("Neparan" if int(input("Unesite broj: ")) % 2 else "Paran")


def factorial(n):
    return 1 if n == 1 else n * factorial(n - 1)


def nth_lowest(items, n):
    return sorted(items)[n - 1] if 0 < n <= len(items) else min(items)


def list_stats(numbers):
    s, p = 0, 1
    for number in numbers:
        if number < 0:
            p *= number
        else:
            s += number

    return min(numbers, key=abs), max(numbers, key=abs), s, p


def list_operations(numbers, threshold):
    novalista = []
    for number in numbers:
        if number < threshold and number not in novalista:
            novalista.append(number)

    print(f"Number of elements in the new list: {len(novalista)}")

    for number in sorted(novalista, reverse=True):
        print(number)


def guessing_game():
    from random import randint
    broj = randint(1, 9)

    print("""
        Welcome to the Guessing Game!
        Your task is to guess the number that has been randomly selected among numbers 1 to 9.
        You may try 3 times. Good luck!
    """)

    pokusaji = 1
    while True:
        broj_pokusaj = input("Your guess is: ")
        if not broj_pokusaj.isdigit() or int(broj_pokusaj) > 9 or int(broj_pokusaj) < 1:
            print("Only digits (1-9) are allowed! Please try again, entering a valid value")
            continue
        broj_pokusaj = int(broj_pokusaj)
        if broj_pokusaj == broj:
            print(f"Congrats! You have correctly guessed - the number is {broj_pokusaj}")
            break
        if pokusaji < 3:
            print(f"Wrong! Please try again - you still have {3 - pokusaji} attempts")
            pokusaji += 1
        else:
            print("Wrong! Sorry, you've made use of all three attempts. More luck next time")
            break
