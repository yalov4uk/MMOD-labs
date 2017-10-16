def testing_independence(method, n=10000, s=3):
    gen = method()
    zi = []

    for _ in xrange(n):
        value = next(gen)
        zi.append(value)

    print('Testing independence {}'.format(method.__name__))
    print('n = {}'.format(n))
    print('R = {}\n'.format(pearson(zi[:-s], zi[s:], n - s)))


def pearson(x, y, n):
    M_x_y = sum([x[i] * y[i] for i in range(n)]) / float(n)

    M_x = sum(x) / float(n)
    M_y = sum(y) / float(n)

    D_x = sum([elem ** 2 for elem in x]) / float(n) - M_x ** 2
    D_y = sum([elem ** 2 for elem in y]) / float(n) - M_y ** 2

    return (M_x_y - M_x * M_y) / float(D_x * D_y) ** 0.5
