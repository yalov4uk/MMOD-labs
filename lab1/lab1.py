def method_1(seed):
    capacity = 8
    start, end = capacity / 2, capacity / 2 + capacity
    while True:
        seed = str(seed ** 2)
        if len(seed) < end:
            seed += '0' * end
        seed = int(seed[start:end])
        yield seed


def method_2(m, k, a0=1):
    ai = a0
    while True:
        ai = (k * ai) % m
        yield ai


def method_1_():
    seed = 39916801
    capacity = 8

    gen = method_1(seed)
    while True:
        value = next(gen) / float('1' + '0' * capacity)
        yield value


def method_2_():
    k = 39916801
    capacity = 8

    gen = method_2(float('1' + '0' * capacity), k)
    while True:
        value = next(gen) / float('1' + '0' * capacity)
        yield value
