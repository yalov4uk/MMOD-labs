import matplotlib.pyplot as plot


def testing_uniformity(method, k=10, n=10000, file_name='bar_1.png'):
    plot.close()

    p1, n1, z1 = get_p(method, k, n / 100)
    p2, n2, z2 = get_p(method, k, n / 10)
    p3, n3, z3 = get_p(method, k, n)

    plot.figure(1)
    create_chart(311, n1, p1, k)
    create_chart(312, n2, p2, k)
    create_chart(313, n3, p3, k)
    plot.savefig(file_name)

    print_testing_uniformity(z1, method.__name__)
    print_testing_uniformity(z2, method.__name__)
    print_testing_uniformity(z3, method.__name__)


def get_p(method, k, n):
    gen = method()

    zi = []
    ni = {(i * 1.0 / k, (i + 1) * 1.0 / k): 0.0 for i in xrange(k)}

    for _ in xrange(n):
        value = next(gen)
        zi.append(value)
        append_to_interval(value, ni)

    pi = []

    for i, interval in enumerate(sorted(ni.keys())):
        pi.append(1.0 * ni[interval] / n)

    return pi, ni, zi


def append_to_interval(value, ni):
    for interval in ni:
        if interval[0] <= value <= interval[1]:
            ni[interval] += 1


def create_chart(id, n, p, k):
    plot.subplot(id)
    plot.bar([elem[0] for elem in sorted(n)], [elem for elem in p], width=1.0 / k)


def print_testing_uniformity(z, method_name):
    M = 1.0 / len(z) * sum(z)
    D = 1.0 / len(z) * sum([v ** 2 for v in z]) - M ** 2

    print('Testing uniformity {}'.format(method_name))
    print('n = {}'.format(len(z)))
    print('M = {}'.format(M))
    print('D = {}\n'.format(D))
