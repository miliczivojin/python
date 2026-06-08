import string
from operator import itemgetter
from collections import defaultdict
from statistics import mean
from collections import Counter


def create_print_numeric_dict(n):
    sums = {x: x * (x + 1) // 2 for x in range(1, n + 1)}
    for key, value in reversed(sums.items()):
        print(f"{key}: {"+".join(str(i) for i in range(1, key + 1))}={value}")


# def lists_to_dict(lista1, lista2):
#     from itertools import zip_longest
#     dictionary = dict()
#     for items1, items2 in zip_longest(lista1, lista2, fillvalue="unknown"):
#         dictionary[items1] = items2
#
#     for key, value in sorted(dictionary.items(), key=itemgetter(1)):
#         print(f"{key}: {value}")


def lists_to_dict(lista1, lista2):
    dictionary = {l1: l2 for l1, l2 in zip(lista1, lista2)}
    for key, value in sorted(dictionary.items(), key=itemgetter(1)):
        print(f"{key}: {value}")


def string_stats(text):
    dictionary = defaultdict(int)
    for ch in text:
        if ch.isdigit():
            dictionary["digits"] += 1
        elif ch.isalpha():
            dictionary["letters"] += 1
        elif ch in ".,!?;:":
            dictionary["punctuation_marks"] += 1
    return dict(dictionary)


def password_check(password):
    dictionary = dict()
    passwords = [p.strip() for p in password.split(",")]
    for password in passwords:
        valid = [False] * 4 + [6 <= len(password) <= 12]
        problems = ["not a single lowercase letter",
                    "not a single digit",
                    "not a single uppercase letter",
                    "not a single special character",
                    "inappropriate length"]
        for ch in password:
            if ch.islower():
                valid[0] = True
            elif ch.isdigit():
                valid[1] = True
            elif ch.isupper():
                valid[2] = True
            elif ch in "$#@":
                valid[3] = True
        dictionary |= {password: ["valid"] if all(valid) else
        [problem for problem, condition in zip(problems, valid) if not condition]}
    return dictionary


def team_stats(members):
    mean_age = mean(member["age"] for member in members)
    print(f"Mean age of team members: {mean_age}")

    # best_under_21 = max((member for member in members if member["age"] < 21), key=lambda member: member["score"])
    best_under_21 = max((member for member in members if member["age"] < 21), key=itemgetter("score"))
    print(f"Best player under 21 years of age: {best_under_21['name']}")

    average_result = mean(member["score"] for member in members)
    list_of_above_average = [member["name"] for member in members if member["score"] > average_result]
    print(f"Average score: {average_result}")
    print("Players with above average score: " + ', '.join(list_of_above_average))

    for member in sorted(members, key=itemgetter("score"), reverse=True):
        print(f"{member["name"]}, {member["age"]}, {member["score"]}")


def token_frequency(text):
    dictionary = defaultdict(int)
    for token in text.split():
        new_token = "".join(ch.lower() for ch in token if ch not in string.punctuation)
        if len(new_token) > 2:
            dictionary[new_token] += 1

    for key, value in sorted(dictionary.items(), key=lambda t: (-t[1], t[0])):
        print(f"{key} : {value}")


def classroom_stats(classrooms):
    # dictionary = defaultdict(int)
    # for cls, pupil_count in classrooms:
    #     dictionary[cls] += pupil_count

    classes = []
    for cls, pupil_count in classrooms:
        classes.extend([cls] * pupil_count)

    dictionary = dict(Counter(classes))

    for key, value in sorted(dictionary.items(), key=itemgetter(1), reverse=True):
        print(f"{key}: {value}")


def website_stats(websites):
    dictionary = defaultdict(int)
    for website in websites:
        domain = website.rstrip("/")
        _, domain = domain.rsplit(".", maxsplit=1)
        dictionary[domain] += 1
    return dict(dictionary)
