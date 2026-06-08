from functools import reduce
import functools
from time import perf_counter


def compute_product(*numbers, squared=False):
    # p = 1
    # for number in numbers:
    #     p *= number ** 2 if squared else number
    # return p
    return reduce(lambda x, y: x * y, [number ** 2 if squared else number for number in numbers])


def select_strings(*strings, threshold=3):
    # lista = []
    # for string in strings:
    #     if string[0].lower() == string[-1].lower() and len(set(string)) > threshold:
    #         lista.append(string)
    # return lista
    # return [string for string in strings if string[0].lower() == string[-1].lower() and len(set(string)) > threshold]
    return list(filter(lambda s: s[0].lower() == s[-1].lower() and len(set(s)) > threshold, strings))


def process_product_orders(orders, discount=None, shipping=10):
    def compute_tot_price(qnt, ppi):
        total_price = qnt * ppi * (1 - discount / 100 if discount else 1)
        return total_price + (shipping if total_price < 100 else 0)

    # dictionary = dict()
    # for order in orders:
    #     order_id, _, quantity, price_per_item = order
    #     dictionary[order_id] = compute_tot_price(quantity, price_per_item)
    # return dictionary
    # return {order_id: compute_tot_price(quantity, price_per_item) for order_id, _, quantity, price_per_item in orders}
    return dict(map(lambda o: (o[0], compute_tot_price(o[2], o[3])), orders))


def timer(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        start = perf_counter()
        value = func(*args, **kwargs)
        end = perf_counter() - start

        print(f"Funkcija {func.__name__} se izvrsila za {end:.4f}s")

        return value

    return wrapper_decorator


@timer
def compute_sum(n):
    # s = 0
    # for x in range(1, n + 1):
    #     s += x * (x + 1) / 2
    # return s

    # return sum([x * (x + 1) / 2 for x in range(1, n + 1)])

    # return reduce(lambda x, y: x + y, map(lambda x: x * (x + 1) / 2, [x for x in range(1, n + 1)]))

    return sum(map(lambda x: x * (x + 1) / 2, [x for x in range(1, n + 1)]))


def standardiser(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        if all(isinstance(arg, (int, float)) for arg in args):
            from statistics import mean, stdev
            m = mean(args)
            std = stdev(args)
            args = [(arg - m) / std for arg in args]
            # args = list(map(lambda arg: (arg - m) / std, args))
        else:
            print("Standardizacija ulaznih argumenata nije uradjena jer nisu svi brojevi")

        print(f"Poziva se funkcija {func.__name__} sa sledecim ulaznim argumentima:")
        print("\t- pozicioni argumenti:" + ", ".join([f"{arg:.4f}" for arg in args]))
        print("\t- imenovani argumenti: " + ", ".join([f"{name}={val}" for name, val in kwargs.items()]))

        value = round(func(*args, **kwargs), 4)

        return value

    return wrapper_decorator


@standardiser
def sum_of_sums(*numbers, n=10):
    return sum(sum(number ** i for i in range(0, n + 1)) for number in numbers)
