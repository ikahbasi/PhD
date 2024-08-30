import numpy as np
import matplotlib.pyplot as plt


def func(x):
    return (3*x**3) - (5*x**2) + (10*x) - 67


n_points = 1000

x = np.arange(-4, 6, 0.01)
y = func(x=x)

y_lim = [y.min(), y.max()]
x_lim = [-4, 6]


x_random = np.random.uniform(low=x_lim[0], high=x_lim[1], size=n_points)
x_random.sort()
y_random = np.random.uniform(low=y_lim[0], high=y_lim[1], size=n_points)
y_true = func(x_random)





mask = y_true > 0
positive = y_random[mask] < y_true[mask]

mask = y_true < 0
negative = y_random[mask] > y_true[mask]

n_points_under_curve = positive.sum() + negative.sum()

area_of_square = (x_lim[1]-x_lim[0]) * (y_lim[1]-y_lim[0])

area_under_curve = (n_points_under_curve/n_points) * area_of_square


print(area_under_curve)


plt.plot(x, y, 'r')
plt.hlines(0, -4, 6, 'k')
plt.scatter(x_random, y_random)
plt.fill_between(x=x_random,
                 y1=0,
                 y2=y_true,
                 color='green', alpha=0.5)
plt.show()