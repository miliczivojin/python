def concat_index_wise(lista1, lista2):
    return [i + j for i, j in zip(lista1, lista2)]


def digits_in_string(text):
    return [ch for ch in text if ch.isdigit()]


def palindrom(text):
    text = [ch.lower() for ch in text if ch.isalnum()]
    return text == text[::-1]


def passwords_check(password):
    passwords = [p.strip() for p in password.split(",")]
    valid_passwords = []
    for password in passwords:
        if 6 <= len(password) <= 12:
            valid = [False] * 4
            for ch in password:
                if ch.islower():
                    valid[0] = True
                elif ch.isdigit():
                    valid[1] = True
                elif ch.isupper():
                    valid[2] = True
                elif ch in "$#@":
                    valid[3] = True
            if all(valid):
                valid_passwords.append(password)

    print("Valid passwords: " + ", ".join(valid_passwords))


def server_status(state_log):
    logs = [line.strip() for line in state_log.split("\n") if line != ""]
    all_servers = []
    defect_servers = []
    for state_log in reversed(logs):
        _, server_name, _, status = state_log.split()
        if server_name not in all_servers:
            all_servers.append(server_name)
            if status == "down":
                defect_servers.append(server_name)

    print(len(all_servers))
    print(len(defect_servers) / len(all_servers))
    if len(defect_servers) > 0:
        print("Servers currently down: " + ", ".join(defect_servers))
    else:
        print("All servers are up and running!")


def anagram(string1, string2):
    string1 = [ch.lower() for ch in string1 if ch.isalnum()]
    string2 = [ch.lower() for ch in string2 if ch.isalnum()]

    return len(string1) == len(string2) and all(ch in string2 for ch in string1)


def are_all_even(number):
    return not (number // 100 % 2 or number // 10 % 2 or number % 2)


def all_even_digits():
    numbers = [number for number in range(100, 401) if are_all_even(number)]
    print("These are your numbers: " + ", ".join(str(number) for number in numbers))


all_even_digits()
