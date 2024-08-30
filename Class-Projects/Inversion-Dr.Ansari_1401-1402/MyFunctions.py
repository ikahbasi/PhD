import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
from sympy.matrices import Matrix # symbolic math package


def SVD(G):
    # equivalent of matlab command [U,S,V] = svd(G)
    U, svec, VH = la.svd(G)
    S = la.diagsvd(svec, *G.shape)
    V = VH.T
    #svec = np.reshape(s,(len(s),1))
    return U, S, V, svec


def G_dager(G, p):
    U, S, V, svec = svdmat(G)
    Up = U[:, :p]
    Vp = V[:, :p]
    Sp = S[:p, :p]
    #
    Sp_inv = np.linalg.inv(Sp)
    G_d = Vp @ Sp_inv @ Up.T
    #
    return G_d


def Picard(U, S, V, y, p=None):
    S_inv = np.linalg.inv(S)
    #
    plt.plot(np.diag(S), 'ko', label='Si')
    plt.plot(abs(U.T@y), 'bo', label='|UTi.d|')
    plt.plot(S_inv@abs(U.T@y), 'r*', label='|UTi.d|/Si')
    if p:
        plt.vlines(p)
        plt.hlines(S[p])
    plt.yscale('log')
    # plt.axis('tight')
    plt.xlabel('i')
    plt.ylabel(r'$s_i$')
    plt.legend()
    # plt.xlim([-1, 15])


def ModelResolutionMatrix():
    pass

def ConditionNumber(svec):
    return svec[0] / svec[-1]
