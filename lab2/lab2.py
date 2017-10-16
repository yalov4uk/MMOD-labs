# coding=utf-8
from collections import Counter

from lab1.lab1 import method_2_


def simple_event(gen=method_2_(), n=1000, p=0.3):
    x = [next(gen) for _ in xrange(n)]
    result = [1 if x[i] <= p else 0 for i in xrange(len(x))]
    M = 1.0 / len(result) * sum(result)
    D = 1.0 / len(result) * sum([v ** 2 for v in result]) - M ** 2
    count = sum(result)

    print "1. simple_event."
    print " A: {}, {}% ".format(count, float(count) / n)
    print " !A : {}, {}%".format(n - count, float(n - count) / n)
    print " M : {}, D : {}\n".format(M, D)


def independent_events(gen=method_2_(), n=1000, pa=0.8, pb=0.5):
    xa = [next(gen) for _ in xrange(n)]
    xb = [next(gen) for _ in xrange(n)]

    a, b, a_b, a_not_b, not_a_b, not_a_not_b = 0, 0, 0, 0, 0, 0

    for i in xrange(n):
        if xa[i] <= pa:
            if xb[i] <= pb:
                a_b += 1
                b += 1
            else:
                a_not_b += 1
            a += 1
        else:
            if xb[i] <= pb:
                not_a_b += 1
                b += 1
            else:
                not_a_not_b += 1

    print "2. independent_events"
    print " A: {}, {}%".format(a, float(a) / n)
    print " B: {}, {}%".format(b, float(b) / n)
    print " A and B: {}, {}%".format(a_b, float(a_b) / n)
    print " !A and !B: {}, {}%".format(not_a_not_b, float(not_a_not_b) / n)
    print " !A and B: {}, {}%".format(not_a_b, float(not_a_b) / n)
    print " A and !B: {}, {}%\n".format(a_not_b, float(a_not_b) / n)


def dependent_events(gen=method_2_(), n=1000, pa=0.8, pb=0.5, pb_a=0.3):
    x1 = [next(gen) for _ in xrange(n)]
    x2 = [next(gen) for _ in xrange(n)]
    a, b, a_and_b, a_and_not_b, not_a_and_b, not_a_and_not_b = 0, 0, 0, 0, 0, 0
    for i in range(n):
        if x1[i] <= pa:
            if x2[i] <= pb_a:
                a_and_b += 1
                b += 1
            else:
                a_and_not_b += 1
            a += 1
        else:
            if x2[i] <= (pb - pb_a * pa) / (1 - pa):
                not_a_and_b += 1
                b += 1
            else:
                not_a_and_not_b += 1

    print "3. dependent_events"
    print " A: {}, {}".format(pa, a)
    print " B: {}, {}".format(pb, b)
    print " B_A: {}".format(pb_a)
    print " A and B: {}, {}%".format(a_and_b, float(a_and_b) / n)
    print " !A and !B: {}, {}%".format(not_a_and_not_b, float(not_a_and_not_b) / n)
    print " !A and B: {}, {}%".format(not_a_and_b, float(not_a_and_b) / n)
    print " A and !B: {}, {}%\n".format(a_and_not_b, float(a_and_not_b) / n)


def full_group_events(gen=method_2_(), p=(0.05, 0.1, 0.1, 0.3, 0.2, 0.25), n=1000):
    y = [next(gen) for _ in xrange(n)]

    pn = list(accumulate(p))

    result = [num(i, pn) for i in y]

    counts = Counter(result)
    print "4. full_group_events"
    print "p: {}, n: {}".format(p, n)
    for k in counts:
        print " {}: {}, {}%".format(k, counts[k], counts[k] / float(len(y)))


def accumulate(iterable):
    total = 0
    for item in iterable:
        total = total + item
        yield total


def num(n, pn):
    for i, e in enumerate(pn):
        if e >= n:
            return i
