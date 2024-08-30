import numpy as np
import scipy.io as sio
import scipy.stats
import matplotlib.pyplot as plt
#
np.random.seed(0)


# Load precomputed data
data1 = sio.loadmat(file_name='data1.mat')
data1 = data1['data1']

t = data1[:, 0]
y = data1[:, 1]
sigma = data1[:, 2]
N = len(t)

print('displaying\nt, y, sigma')
print(data1)

# Build the parabolic system matrix
G = np.ones(shape=(N, 3))
G[:, 1] = t
G[:, 2] = -0.5 * t ** 2

# Apply the weighting

yw = y / sigma
Gw = G / sigma.reshape(N, 1)

# Solve for the least-squares solution
print('Least-squares solution')
m_p1 = np.linalg.inv(np.dot(Gw.T, Gw))
m_p2 = np.dot(Gw.T, yw)
m = np.dot(m_p1, m_p2)
print(m)

# Get the covariance matrix
ginv = np.dot(np.linalg.inv(np.dot(Gw.T, Gw)), Gw.T)

print('Covariance matrix')
covm = np.dot(ginv, ginv.T)

# Get the 1.96-sigma (95#) conf intervals
print('95% parameter confidence intervals (m-, mest, m+)')
delta1 = 1.96 * np.sqrt(np.diag(covm))
print([m-delta1, m, m+delta1])

#
# Because there are 3 parameters to estimate, we have N-3 degrees
# of freedom.
#
dof = N - 3
print(f'Chi-square misfit for {dof} dof')
chi2 = np.linalg.norm((y-np.dot(G, m)) / sigma) ** 2

# Find the p-value for this data set
print('chi-square p-value')
p = scipy.stats.chi2.sf(chi2, dof)

# Find the parameter correlations
s = np.sqrt(np.diag(covm))
s = s.reshape(-1, 1)

print('correlation matrix')
r = covm / np.dot(s, s.T)

# Plot the data and model predicted data
delta2 = 0.05
xx = np.arange(min(t)-1, max(t)+1+delta2, delta2)
mm = m[0] + (m[1]*xx) - (0.5*m[2]*(xx**2))

fig1 = plt.figure()
plt.plot(xx, mm, 'k')
plt.errorbar(x=t, y=y, yerr=sigma, fmt='o', ecolor='k')
plt.xlabel('Time (s)')
plt.ylabel('Elevation (m)')
plt.show()
# bookfonts

# print('Displaying Data and Model Fit (fig 1)')
# print(-deps2 c2fparabfig.eps

# # Output covm and the eigenvalues/eigenvectors of covm.
# print('Covariance matrix for fitted parameters.')
# covm
# import scipy.linalg as la

print('Eigenvalues/eigenvectors of the covariance matrix')
lam, u = np.linalg.eig(np.linalg.inv(covm))
# lam, u = la.eig(np.linalg.inv(covm))

print('95% confidence ellipsoid semiaxis lengths')

semi_axes = np.sqrt(np.dot(scipy.stats.chi2.ppf(0.95, 3), (1/lam)))
semi_axes = abs(semi_axes)
print('95% confidence ellipsoid semiaxes')

print(semi_axes[0]*u[:, 0])
print(semi_axes[1]*u[:, 1])
print(semi_axes[2]*u[:, 2])

# Monte Carlo Section
y0 = np.dot(G, m)

chimc = np.zeros(1000)
mmc = np.zeros((1000, 3))
for nreal in range(0, 1000):
    # Generate a trial data set of perturbed, weighted data
    ytrial = y0 + sigma * np.random.randn(N)
    ywtrial = ytrial / sigma
    mmc[nreal, :] = np.linalg.lstsq(Gw, ywtrial)[0]
    chimc[nreal] = np.linalg.norm(
        (np.dot(G, mmc[nreal, :])-ytrial) / sigma) ** 2

# Plot the histogram of chi squared values
print('Displaying 1000 Monte-Carlo Chi-square Values (fig 2)')
fig2 = plt.figure()
plt.hist(chimc, 30, edgecolor='black')
plt.ylabel('N')
plt.xlabel('chi^2')

# Plot the histograms of the model parameters
print('Displaying Monte-Carlo Model Histograms (fig 3)')
fig3, axs = plt.subplots(1, 3, figsize=(9, 3))
scale_labels = ['m', 'm/s', 'm/(s^2)']
for indx in range(3):
    ax = axs[indx]
    ax.hist(mmc[:, indx], edgecolor='black')
    ax.set_title(f'm_{indx+1} ({scale_labels[indx]})')
plt.tight_layout()
plt.show()

# Plot the realizations of each pair of model parameters with the other
print('Displaying Projections of 1000 Monte-Carlo models (fig 4)')

fig4, axs = plt.subplots(1, 3, figsize=(9, 3))

m_labels = [[1, 2], [1, 3], [2, 3]]
scale_labels = ['m', 'm/s', 'm/(s^2)']

for indx in range(3):
    m_label = m_labels[indx]
    ax = axs[indx]
    #
    ax.plot(mmc[:, m_label[0]-1], mmc[:, m_label[1]-1], 'k*')
    ax.set_xlabel(f'm_{m_label[0]} ({scale_labels[m_label[0]-1]})')
    ax.set_ylabel(f'm_{m_label[1]} ({scale_labels[m_label[1]-1]})')
plt.tight_layout()
plt.show()

#
# Plot the 95# error ellipses for each pair of parameters
# Note that because we're doing pairs of parameters there are 2
# degrees of freedom in the Chi-square here, rather than 3.
#
print('Displaying 95% Confidence Ellipse projections (fig 5)')
# generate a vector of angles from 0 to 2*pi
delta = 0.01
theta = np.arange(0, 2*np.pi, delta)
# theta = theta.reshape(-1, 1)

delta = np.sqrt(scipy.stats.chi2.ppf(0.95, 2))
# the radii in each direction from the center
r = np.zeros((theta.size, 2))


C12 = covm[0:2, 0:2]              # m1, m2 ellipsoid
C13 = covm[[0, 2], :][:, [0, 2]]  # m1, m3 ellipsoid.
C23 = covm[1:, 1:]                # m2, m3 ellipsoid.
C_all = [C12, C13, C23]

m_labels = [[1, 2], [1, 3], [2, 3]]
scale_labels = ['m', 'm/s', 'm/(s^2)']

fig4, axs = plt.subplots(1, 3, figsize=(9, 3))
ax1, ax2, ax3 = axs
for indx in range(3):
    C = C_all[indx]
    m_label = m_labels[indx]
    ax = axs[indx]
    #
    lam, u = np.linalg.eig(np.linalg.inv(C))
    # calculate the x component of the ellipsoid for all angles
    r[:, 0] = (delta/np.sqrt(lam[0])) * u[0, 0] * np.cos(theta) + \
        (delta/np.sqrt(lam[1])) * u[0, 1] * np.sin(theta)
    # calculate the y component of the ellipsoid for all angles
    r[:, 1] = (delta/np.sqrt(lam[0])) * u[1, 0] * np.cos(theta) + \
        (delta/np.sqrt(lam[1])) * u[1, 1] * np.sin(theta)
    #
    _x = m[m_label[0]-1] + r[:, 0]
    _y = m[m_label[1]-1] + r[:, 1]
    ax.plot(_x, _y, 'k*')
    ax.set_xlabel(f'm_{m_label[0]} ({scale_labels[m_label[0]-1]})')
    ax.set_ylabel(f'm_{m_label[1]} ({scale_labels[m_label[1]-1]})')
plt.tight_layout()
plt.show()
