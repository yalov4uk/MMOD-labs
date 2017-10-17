import math

import scipy.stats as st
from matplotlib import pyplot, mlab

from lab1.lab1 import method_2_


class Lab3:
    def __init__(self):
        self.l = 1.5
        self.x_min = 0.0
        self.x_max = 5.0
        self.n = 100
        self.h = (self.x_max - self.x_min) / self.n
        self.x = [i * self.h for i in xrange(self.n)]
        self.y = [self.l * (math.e ** (-self.l * self.x[i])) for i in xrange(self.n)]
        self.F = [1 - math.e ** (-self.l * self.x[i]) for i in xrange(self.n)]

    def run(self):
        pyplot.figure(figsize=(15, 5))
        y1 = self.generate_contineous_law(1, 100)
        y2 = self.generate_contineous_law(2, 10000)

        pyplot.figure(figsize=(15, 5))
        F1 = self.generate_function_distribution(1, y1)
        F2 = self.generate_function_distribution(2, y2)

        k2 = self.kolmogorov(y2, F2)
        print k2

        pyplot.figure(figsize=(15, 5))
        self.confidence(1, y1)

        pyplot.show()

    def generate_contineous_law(self, i, n):
        pyplot.subplot(1, 2, i)
        gen = method_2_()
        xn = [next(gen) for _ in xrange(n)]
        yn = [-1.0 * (1.0 / self.l) * math.log(1 - xn[i]) for i in xrange(n)]
        pyplot.hist(yn, normed=1)
        M = self.calculate_M(yn)
        D = self.calculete_D(yn, M)
        pyplot.title('n = {},  M = {}. D = {}'.format(n, M, D))
        pyplot.plot(self.x, self.y)
        return yn

    def generate_function_distribution(self, i, y):
        pyplot.subplot(1, 2, i)
        y.sort()
        F = [i / float(len(y)) for i in xrange(len(y))]
        pyplot.title("Exponential function {}".format(len(y)))
        pyplot.plot(y, F)
        pyplot.plot(self.x, self.F)
        return F

    def kolmogorov(self, y, F):
        F_teor = [1 - math.e ** (-self.l * y[i]) for i in xrange(len(y))]
        return math.sqrt(self.n) * max(abs(F[i] - F_teor[i]) for i in xrange(len(y)))

    def confidence(self, i, y):
        pyplot.subplot(1, 2, i)
        x_min = 0.01
        x_max = 0.99
        dx = 0.01
        xlist = mlab.frange(x_min, x_max, dx)
        ylist = [
            st.norm.ppf((i + 1) / 2) * 2 * math.sqrt(self.calculete_D(y, self.calculate_M(y))) / math.sqrt(self.n - 1)
            for i in xlist]
        pyplot.plot(xlist, ylist, 'b')

    def calculate_M(self, y):
        """ M = 1/lambda """
        return sum(y) / len(y)

    def calculete_D(self, y, M):
        """ D = 1/lambda^2 """
        return sum([y[i] ** 2 - M ** 2 for i in xrange(len(y))]) / len(y)
