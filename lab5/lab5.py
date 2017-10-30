import numpy
from matplotlib import pyplot

from lab1.lab1 import method_2_


class Lab5(object):
    def __init__(self):
        self.a = 2
        self.b = 12
        self.n = 10000

    def run(self):
        xy_gen = self.generate_xy()
        xy_list = self.get_list(xy_gen)

        x_list, y_list = zip(*xy_list)
        x_list, y_list = numpy.array(x_list), numpy.array(y_list)

        print 'M[X] = {}, theoretical = {}'.format(x_list.mean(), (self.a + self.b) / 2.0)
        print 'D[X] = {}, theoretical = {}'.format(x_list.std() ** 2, (self.b - self.a) ** 2 / 12.0)

        print 'M[Y] = {}'.format(y_list.mean())
        print 'D[Y] = {}'.format(y_list.std() ** 2)

        print 'r = {}'.format(numpy.corrcoef(x_list, y_list)[0][0])

        pyplot.hist(x_list, normed=True)
        pyplot.show()

        pyplot.hist(y_list, normed=True)
        pyplot.show()

    def generate_xy(self):
        uniform_distribution_gen = self.uniform_distribution()
        while True:
            x = uniform_distribution_gen.next()
            lmbd = x * 3
            y = self.exponential_distribution(lmbd).next()
            yield x, y

    def uniform_distribution(self):
        """
            x = y * (b - a) + a
            y = (x - a) / (b - a)
            """
        gen = method_2_()
        while True:
            x = gen.next()
            yield x * (self.b - self.a) + self.a

    def exponential_distribution(self, lmbd):
        """
            y = 1 - exp(-lambda * x)
            x = -(1 / lmbd) * ln(1 - y)
            """
        gen = method_2_()
        while True:
            x = gen.next()
            yield -(1.0 / lmbd) * numpy.log(1 - x)

    def get_list(self, gen):
        lst = []
        for i in xrange(self.n):
            lst.append(gen.next())
        return lst
