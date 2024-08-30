import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel('data_sarpolzahab.xlsx')
pga = data['PGA (cm/s2)'].values
r_jb = data['R_jb (km)'].values
vs_30 = data['Vs_30 (m/s)'].values

sa = np.zeros(vs_30.size)
ss = np.zeros(vs_30.size)

msk = vs_30<360
sa[msk] = 0
ss[msk] = 1

msk = np.logical_and(360<vs_30, vs_30<750)
sa[msk] = 1
ss[msk] = 0

msk = vs_30>750
sa[msk] = 0
ss[msk] = 0

d = np.log10(pga)

G = np.ones((d.size, 4))
# G[:, 0] = 1
G[:, 1] = np.log10(r_jb)
G[:, 2] = ss
G[:, 3] = sa


m = np.linalg.inv(G.T @ G) @ G.T @ d

def Attenuation(b, r_jb, ss, sa):
    b1, b2, b3, b4 = b
    return b1 + (b2*np.log10(r_jb)) + b3*ss + b4*sa

log10_pga_estimation = Attenuation(b=m, r_jb=r_jb, ss=ss, sa=sa)

plt.plot(r_jb, d, label='Observations')
plt.plot(r_jb, log10_pga_estimation, label='Estimation')
plt.legend()
plt.show()