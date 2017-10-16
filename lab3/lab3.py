import numpy as np
from matplotlib import pyplot, mlab
import math
import scipy.stats as st


def MKM(count, n=30, k=123456789, A0=2):
    """
    Function generating a number by a multiplicative congruential method.
    """
    m = 2 ** n
    A = list()
    A.append(A0)
    for i in xrange(count):
        A.append((k * A[i]) % m)

    z = [A[i] / float(m) for i in xrange(1, len(A))]
    return z


"""
Generate a continuous random variable distributed according to the exponential law by 
the inverse function method and construct the distribution histograms and the theoretical 
distribution density. Compare the results.
"""
l = 2
pyplot.figure(figsize=(16, 6))
x_min = 0.0
x_max = 6.0
n = 100
h = (x_max - x_min) / n
x = [i * h for i in xrange(n)]
lmbd = 1
y = [lmbd * (math.e ** (-lmbd * x[i])) for i in xrange(len(x))]

pyplot.subplot(1, 2, 1)
x1 = MKM(100)
y1 = [-1.0 * (1.0 / l) * math.log(1 - x1[i]) for i in xrange(len(x1))]
pyplot.hist(y1, normed=1)
M1 = sum(y1) / len(y1)
D1 = sum([y1[i] ** 2 - M1 ** 2 for i in xrange(len(y1))]) / len(y1)
pyplot.title('{0} numbers. M = {1}. D = {2}'.format(len(y1), M1, D1))
pyplot.plot(x, y)

pyplot.subplot(1, 2, 2)
x2 = MKM(10000)
y2 = [-1.0 * (1.0 / l) * math.log(1 - x2[i]) for i in xrange(len(x2))]
pyplot.hist(y2, normed=1)
M2 = sum(y2) / len(y2)
D2 = sum([y2[i] ** 2 - M2 ** 2 for i in xrange(len(y2))]) / len(y2)
pyplot.title('{0} numbers. M = {1}. D = {2}'.format(len(y2), M2, D2))
pyplot.plot(x, y)


"""
Let's construct a theoretical distribution function and empirical distribution functions for sampling volumes of 
100 and 10000, respectively. Compare the results.
"""
pyplot.figure(figsize=(16, 6))
F = [1 - math.e ** (-l * x[i]) for i in xrange(len(x))]

pyplot.subplot(1, 2, 1)
y1.sort()
F1 = [i / float(len(y1)) for i in xrange(len(y1))]
pyplot.title("theoretical exponential function with sampling : {}".format(len(y1)))
pyplot.plot(y1, F1)
pyplot.plot(x, F)

pyplot.subplot(1, 2, 2)
y2.sort()
F2 = [i / float(len(y2)) for i in xrange(len(y2))]
pyplot.title("empirical exponential function with sampling : {}".format(len(y2)))
pyplot.plot(y2, F2)
pyplot.plot(x, F)


"""
Check the Kolmogorov test of agreement.
"""
F1_teor = [1 - math.e ** (-l * y1[i]) for i in xrange(len(y1))]
F2_teor = [1 - math.e ** (-l * y2[i]) for i in xrange(len(y2))]
print math.sqrt(n) * max(abs(F2[i] - F2_teor[i]) for i in xrange(len(y2)))

"""
Let's construct a graph of the dependence of the value of the confidence interval, on the value 
of the confidence probability for the mathematical expectation.
"""
x_min = 0.01
x_max = 0.99
dx = 0.01
xlist = mlab.frange(x_min, x_max, dx)
ylist = [st.norm.ppf((i + 1) / 2) * 2 * math.sqrt(D1) / math.sqrt(n - 1) for i in xlist]
pyplot.plot(xlist, ylist, 'b')

pyplot.show()
