import numpy as np
from matplotlib import pyplot

from lab1.lab1 import method_2_


class Lab4(object):
    def __init__(self):
        self.X = [6.0, 2.0, 7.0, 5.0]
        self.Y = [4.0, 1.0, 3.0]
        self.matrix_distribution = np.array(
            [[0.05, 0.1, 0.07, 0.02],
             [0.08, 0.17, 0.0, 0.1],
             [0.03, 0.11, 0.2, 0.07]]
        )
        self.m, self.n = self.matrix_distribution.shape

    def run(self):
        self.check_matrix_probability()

        p_x = self.calculate_distribution_row()
        f_x = self.calculate_distribution_function(p_x)

        p_y = self.calculate_conditional_distribution_row(p_x)
        f_y = self.calculate_conditional_distribution_function(p_y)

        empirical_matrix_distribution = self.generate_empirical_matrix(f_x, f_y)

        p_x_empirical = self.bar_chart_x(p_x, empirical_matrix_distribution)
        p_y_empirical = self.bar_chart_y(p_y, empirical_matrix_distribution, p_x_empirical)

        pyplot.show()

    def check_matrix_probability(self):
        if sum(sum(self.matrix_distribution)) != 1.0:
            raise AttributeError("Sum of matrix != 1")

    def calculate_distribution_row(self):
        return [sum(self.matrix_distribution[i, j] for i in xrange(self.m)) for j in xrange(self.n)]

    def calculate_distribution_function(self, p_x):
        f_x = [0.0]
        for i in xrange(len(p_x)):
            f_x.append(f_x[i] + p_x[i])
        return f_x

    def calculate_conditional_distribution_row(self, p_x):
        p_y = np.array(self.matrix_distribution)
        for j in xrange(self.n):
            for i in xrange(self.m):
                p_y[i, j] /= p_x[j]
        return p_y

    def calculate_conditional_distribution_function(self, p_y):
        f_y = np.zeros((self.m + 1, self.n))
        for j in xrange(self.n):
            for i in xrange(self.m):
                f_y[i + 1, j] = f_y[i, j] + p_y[i, j]
        return f_y

    def generate_empirical_matrix(self, f_x, f_y):
        empirical_matrix_distribution = np.zeros((self.m, self.n))
        N, k, l = 10000, 0, 0
        gen = method_2_()
        z = [next(gen) for _ in xrange(N * 2)]
        for i in xrange(0, len(z), 2):
            for j in xrange(self.n + 1):
                if z[i] <= f_x[j]:
                    k = j - 1
                    break
            for j in xrange(self.m + 1):
                if z[i + 1] <= f_y[j, k]:
                    l = j - 1
                    break
            empirical_matrix_distribution[l, k] += 1

        for i in xrange(self.m):
            for j in xrange(self.n):
                empirical_matrix_distribution[i, j] /= N
        return empirical_matrix_distribution

    def bar_chart_x(self, p_x, empirical_matrix_distribution):
        width = 0.1

        p_x_empirical = [sum(empirical_matrix_distribution[i, j] for i in xrange(self.m)) for j in xrange(self.n)]
        o_x = [self.X[i] + width for i in xrange(self.n)]

        pyplot.bar(self.X, p_x, width, color='green')
        pyplot.bar(o_x, p_x_empirical, width, color='red')
        pyplot.title('X distribution probability')
        return p_x_empirical

    def bar_chart_y(self, p_y, empirical_matrix_distribution, p_x_empirical):
        p_y_empirical = np.array(empirical_matrix_distribution)
        for j in xrange(self.n):
            for i in xrange(self.m):
                p_y_empirical[i, j] /= p_x_empirical[j]

        width = 0.1
        o_y = [self.Y[i] + width for i in xrange(self.m)]

        pyplot.figure(figsize=(22, 6))

        for k in xrange(1, self.n + 1):
            pyplot.subplot(1, self.n, k)
            pyplot.bar(self.Y, p_y[:, k - 1], width, color='green')
            pyplot.bar(o_y, p_y_empirical[:, k - 1], width, color='red')
            pyplot.title('Y for X = {}'.format(self.X[k - 1]))

        return p_y_empirical
