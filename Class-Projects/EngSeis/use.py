from EngSeis.proc import Signal
import numpy as np
import matplotlib.pyplot as plt


fname = 'I1.KRD..HNN.D.20171112.181816.X.ACC.ASC'
sigO = Signal()
sigO.read1(fname)
sigO.Dmean()


sig_vel = sigO.copy()
sig_vel.Differentiation()


sigF = sig_vel.copy()
sigB = sig_vel.copy()
sigC = sig_vel.copy()


sigF.Derivative(method='forward')
sigB.Derivative(method='backward')
sigC.Derivative(method='central')


dif_F = sigO.data - sigF.data
dif_B = sigO.data - sigB.data
dif_C = sigO.data - sigC.data


# compare plot
plt.plot(sigO.data, 'k', linewidth=0.3, label='Origin')
plt.plot(sigF.data, 'r', linewidth=0.3, label='Forward')
plt.plot(sigB.data, 'b', linewidth=0.3, label='Backward')
plt.plot(sigC.data, 'g', linewidth=0.3, label='Central')
plt.legend()
plt.show()


# Differences histogram
plt.subplot(311)
plt.hist(dif_F, bins=50, log=True, color='r')
plt.title('Forward')

plt.subplot(312)
plt.hist(dif_B, bins=50, log=True, color='b')
plt.title('Backward')

plt.subplot(313)
plt.hist(dif_C, bins=50, log=True, color='g')
plt.title('Central')

plt.suptitle('Differences histogram')
plt.subplots_adjust(hspace=0.6)
plt.show()


# Differences signals
plt.subplot(311)
plt.plot(sigO.simpletime, dif_F, color='r')
plt.title('Forward')

plt.subplot(312)
plt.plot(sigO.simpletime, dif_B, color='b')
plt.title('Backward')

plt.subplot(313)
plt.plot(sigO.simpletime, dif_C, color='g')
plt.title('Central')

plt.suptitle('Differences signals')
plt.subplots_adjust(hspace=0.6)
plt.show()
