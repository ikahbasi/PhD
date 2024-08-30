import numpy as np
from obspy import read
from v1 import *
from obspy import Stream, Trace
import glob
import matplotlib.pyplot as plt
import scipy
from scipy import signal
import scipy.fftpack
import numpy as np

def _fft(tr):
    npts = tr.stats.npts
    delta = tr.stats.delta
    data = tr.data
    segment = scipy.fftpack.helper.next_fast_len(npts)
    freq = np.fft.fftfreq(segment, d=delta)[:npts//2]
    ampl = scipy.fftpack.fft(data, segment) * delta
    ampl = np.abs(ampl[:npts//2]) / (segment*delta)# time of data = segment * delta
#    ampl += sum(tr.data) - ampl[0]
    return freq, ampl


def plot_fft(st):
    for tr in st:
        freq, ampl = _fft(tr)
        # for a singel frequency figure
        plt.loglog(freq, ampl, label=f'{tr.id} max: {max(ampl):.2f}')
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency [HZ]')
    plt.xlim([0, 10])
    plt.grid()
    plt.legend()
    plt.show()
#    plt.savefig(f'{tr.id}_fft.png')
#    plt.close()


def h2v(st, smoothing=1):
    freqV, amplV = _fft(st.select(channel='V*')[0])
    freqL, amplL = _fft(st.select(channel='L*')[0])
    freqT, amplT = _fft(st.select(channel='T*')[0])
    #
    box = np.ones(smoothing) / smoothing
    amplV = np.convolve(amplV, box, mode='same')
    amplL = np.convolve(amplL, box, mode='same')
    amplT = np.convolve(amplT, box, mode='same')
    amplM = np.mean(np.array([amplL, amplT]), axis=0)
    M2v = amplM / amplV
    return M2v, freqL

def find_near_value_index(array, value):
    a = np.abs(np.array(array)-value)
    idx = a.argmin()
    return idx

def plot_h2v(st):
    m2v, freq = h2v(st)
    plt.plot(freq, m2v)
    plt.xlim(left=0, right=15)
    plt.grid()
    plt.legend()
    plt.show()

#
#from matplotlib import ticker
#formatter = ticker.ScalarFormatter(useMathText=True)
#formatter.set_scientific(True) 
#formatter.set_powerlimits((-1,1)) 


#plot_h2v(st)
name = {'3168-2 .V1': 'bam',
        '5520-1.V1':  'Ahar',
        '7384-1.V1':  'Sarpolezahab',
        '9171-1.V1':   'Siyahoo',
        '9171-2.V1':   'Siyahoo2'}
v1s = glob.glob('*.V1')#[-1:]
for path in v1s:
    print(path, name[path])
    st = read_v1(path,method = 'obspystream', dt=0.005)
    st.detrend('constant');# st.plot()
    M2V, freq = h2v(st, smoothing=50)
    fig= plt.figure()
    plt.semilogx(freq, M2V)
    plt.xlim(left=0.5, right=15)
    plt.grid(visible=True, which='major', axis='both', color='k',
             linewidth=0.7, alpha=0.5)
#    grid(color='r', linestyle='-', linewidth=2)
    plt.grid(visible=True, which='minor', axis='both', color='k',
             linestyle='dashed', linewidth=0.5, alpha=0.5)
    plt.title(name[path])
    plt.ylabel('Amplification')
    plt.xlabel('Frequency [HZ]')
#    from matplotlib.ticker import FormatStrFormatter
#    plt.tick_params(axis='y', which='minor')
#    ax.yaxis.set_minor_formatter(FormatStrFormatter("%.1f"))
    plt.savefig(f'{name[path]}-1.png', dpi=200)
#    plt.show()

