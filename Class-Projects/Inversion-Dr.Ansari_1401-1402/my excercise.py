import numpy as np
import scipy.io as sio
import scipy.stats
import matplotlib.pyplot as plt
#


def ellipse(a, b, c, d):
    delta = 0.01
    theta = np.arange(0, 2*np.pi, delta)
    x = a * np.cos(theta) + b * np.sin(theta)
    y = c * np.cos(theta) + d * np.sin(theta)
    return x, y


#x, y = ellipse(1, -2, 3, -4)
#plt.plot(x, y)
#ax = plt.gca()
#ax.set_aspect('equal', 'box')

# Load precomputed data
data1 = sio.loadmat(file_name='data1.mat')
data1 = data1['data1']

t = data1[:, 0]
y = data1[:, 1]
sigma = data1[:, 2]

plt.plot(t, y)

m_dim = t.size
n_dim = 3

G = np.ones((m_dim, n_dim))
G[:, 1] = t
G[:, 2] = -0.5 * t**2
G = G/sigma.reshape((-1, 1))
y = y/sigma

m = np.linalg.inv(G.T@G) @ G.T @ y
print(m)
def make_equation(m, t):
    return m[0] + m[1]*t - (1/2)*m[2]*(t**2)

y_fit = make_equation(m=m, t=t)


plt.scatter(t, y)
plt.plot(t, y_fit)
plt.show()

###
r = y - y_fit
plt.plot(t, r, 'o')

###

# cov(ml2) = cov() <- Gm=d
# cov(ml2) = (sigma^2) * (G'@G)^-1
cov = (sigma[0]**2) * np.linalg.inv(G.T@G)

################
#import seaborn as sns
#import matplotlib.pyplot as plt
#
#labs = ['m', 'm/s', 'm/s^2']
#
#sns.heatmap(cov, annot=True, fmt='g', xticklabels=labs, yticklabels=labs)
#plt.show()



chi2 = sum(r**2/sigma**2)
dof = m_dim - n_dim # degree_of_freedom

def gamma(n):
    # print(n)
    if n==1:
        return 1
    return gamma(n-1)*n

def f_chi2(x, v):
    '''
    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    v : int
        degrees of freedom (v = m - n).

    Returns
    -------
    int.

    '''
    return (x**(0.5*v-1) * np.exp(-x/2)) / ((2**(v/2) * gamma(v/2)))

# def
from scipy import stats
########### which???
p1 = 1 - stats.chi2.cdf(4.2, 7)
p2 = scipy.stats.chi2.sf(chi2, dof)
