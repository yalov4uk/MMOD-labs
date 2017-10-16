import numpy as np
from matplotlib import pyplot


def MKM(count, n=30, k=123456789, A0=2):
    """
    A function that generates numbers by a multiplicative congruential method
    :param count: 4
    :param n:
    :param k:
    :param A0:
    :return:
    """
    m = 2 ** n
    A = list()
    A.append(A0)
    for i in xrange(count):
        A.append((k * A[i]) % m)

    z = [A[i] / float(m) for i in xrange(1, len(A))]
    return z


X = [1.0, 3.0, 5.0, 7.0]
Y = [2.0, 4.0, 6.0]

"""
Allocation matrix of a discrete random variable
"""
matrix_distribution = np.array([[0.05, 0.1, 0.07, 0.02],
                                [0.08, 0.17, 0.0, 0.1],
                                [0.03, 0.11, 0.2, 0.07]])
m, n = matrix_distribution.shape

new_matrix_distribution = sum(matrix_distribution)
print "Check for the sum of a two-dimensional probability matrix : {} ".format(sum(new_matrix_distribution))
print "----------------------------------------------------------------------------------------------------"

"""
Series and the distribution function for the component X
"""
p_X = [sum(matrix_distribution[i, j] for i in xrange(m)) for j in xrange(n)]

F_X = [0.0]
for i in xrange(len(p_X)):
    F_X.append(F_X[i] + p_X[i])

print p_X
print F_X
print "----------------------------------------------------------------------------------------------------"

"""
Conditional series of the distribution of the component Y.
"""
p_Y = np.array(matrix_distribution)
for j in xrange(n):
    for i in xrange(m):
        p_Y[i, j] /= p_X[j]

print "conditional distribution series : " \
      "{} ".format(p_Y)
print "----------------------------------------------------------------------------------------------------"

"""
Conditional distribution functions of the Y component.
"""
F_Y = np.zeros((m + 1, n))

for j in xrange(n):
    for i in xrange(m):
        F_Y[i + 1, j] = F_Y[i, j] + p_Y[i, j]

print "conditional distribution functions :" \
      " {}".format(F_Y)
print "----------------------------------------------------------------------------------------------------"

"""
The empirical distribution matrix (capacity of 20.000).
"""
matrix_distribution_practical = np.zeros((m, n))
z = MKM(20000)
k = 0
l = 0
for i in xrange(0, len(z), 2):
    for j in xrange(n + 1):
        if z[i] > F_X[j]:
            pass
        else:
            k = j - 1
            break

    for j in xrange(m + 1):
        if z[i + 1] > F_Y[j, k]:
            pass
        else:
            l = j - 1
            break

    matrix_distribution_practical[l, k] += 1

for i in xrange(m):
    for j in xrange(n):
        matrix_distribution_practical[i, j] /= 10000

print matrix_distribution_practical

"""
Theoretical and empirical series of the distribution of the component X in the form of bar charts
"""
width = 0.1

p_X_practical = [sum(matrix_distribution_practical[i, j] for i in xrange(m)) for j in xrange(n)]
XX = [X[i] + width for i in xrange(n)]

pyplot.bar(X, p_X, width, color='C1')
pyplot.bar(XX, p_X_practical, width, color='C2')
pyplot.title('probability distribution X components')

"""
Theoretical and empirical series of the distribution of the component Y for all values 
of the component X in the form of bar charts
"""
p_Y_practical = np.array(matrix_distribution_practical)
for j in xrange(n):
    for i in xrange(m):
        p_Y_practical[i, j] /= p_X_practical[j]

width = 0.1
YY = [Y[i] + width for i in xrange(m)]

pyplot.figure(figsize=(22, 6))

for k in xrange(1, n + 1):
    pyplot.subplot(1, n, k)
    pyplot.bar(Y, p_Y[:, k - 1], width, color='C1')
    pyplot.bar(YY, p_Y_practical[:, k - 1], width, color='C2')
    pyplot.title('prob. distr. Y components for X = {0}'.format(X[k - 1]))

pyplot.show()
