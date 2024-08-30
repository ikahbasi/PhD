'''
Iman Kahbasi
'''
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import os


def additional_docstring(**kwargs):
    def _wrapper(target):
        target.__doc__ = target.__doc__.format(**kwargs)
        return target
    return _wrapper


plotting_kwargs = """
    :type title: str
    :param title: Title of figure
    :type show: bool
    :param show: Whether to show the figure or not (defaults to True)
    :type save: bool
    :param save: Whether to save the figure or not (defaults to False)
    :type savefile: str
    :param savefile:
        Filename to save figure to, if `save==True` (defaults to "tmp.png")
    :type return_figure: bool
    :param return_figure:
        Whether to return the figure or not (defaults to True), if False
        then the figure will be cleared and closed.
    :type size: tuple of float
    :param size: Figure size as (width, height) in inches. Defaults to
        (10.5, 7.5)
    :type xlime: tuple of float
    :param xlime: Figure limitation as (left, right). Defaults to None.
    :type ylime: tuple of float
    :param ylime: Figure limitation as (blow, top). Defaults to None.
                  """


@additional_docstring(plotting_kwargs=plotting_kwargs)
def _finalise_figure(fig, **kwargs):  # pragma: no cover
    """
    Internal function to wrap up a figure.
    {plotting_kwargs}
    """
    size = kwargs.get("size", (10.5, 7.5))
    fig.set_size_inches(size)
    show = kwargs.get("show", True)
    save = kwargs.get("save", False)
    savefile = kwargs.get("savefile", "tmp.png")
    return_fig = kwargs.get("return_figure", False)
    title = kwargs.get("title")
    xlim = kwargs.get("xlim")
    ylim = kwargs.get("ylim")
    if title:
        plt.title(title)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    if save:
        path = os.path.dirname(savefile)
        if path:
            os.makedirs(path, exist_ok=True)
        fig.savefig(savefile, bbox_inches="tight", dpi=130)
        print("Saved figure to {0}".format(savefile))
    if show:
        plt.show()
    if return_fig:
        return fig


class Signal:
    def __init__(self,
                 data=None, unit=None,
                 network='', station='', location='', channel='', event_id='',
                 starttime=None, starttime_format=None,
                 sps=None, gain=None):
        '''
        :type data: numpy.ndarray
        :param data: numpy array of signal (defaults to None).
        :type unit: str
        :param unit: string of unit input.
            For dicplacement, velocity and acceleration must
            set to cm, cm/s, cm/s^2 respectively (defaults to None).
        :type network: str
        :param network: network of station  (defaults to '')
        :type station: str
        :param station: station name  (defaults to '')
        :type location:  str
        :param location: location of station  (defaults to '')
        :type channel: str
        :param channel: channel of station  (defaults to '')
        :type event_id: str
        :param event_id: string of an arbitrary code for event
            (defaults to '').
        :type starttime_foramt: str
        :param starttime_format: string of format of input time
            (defaults to None).
        :type starttime: str
        :param starttime: string of start time with arbitrary foramt
            (defaults to None).
            make a string with blow sign according to your time.
            %Y for year
            %m for month
            %d for day
            %H for hour
            %M for minute
            %S for second
        :type sps: int
        :param sps: sampling rate of signal  (defaults to None).
        :type gain: float
        :param gain: value of instrumental gain.
            if you data has been corrected, left this parameter to be
            None  (defaults to None).

        .. note::
            format of starttime parameter must set in starttime_foramt.
        '''
        # signal
        if isinstance(data, np.ndarray):
            self.data = data
        else:
            self.data = np.array([])
        self.unit = unit
        # metadata
        self.network = network
        self.station = station
        self.location = location
        self.channel = channel
        self.event_id = event_id
        self.starttime = starttime
        self.starttime_format = starttime_format
        self.sps = sps
        self.gain = gain
        # sync variable
        self.npts = None
        self._sync()

    def _sync(self):
        sps = self.sps
        stime = self.starttime
        stime_frmt = self.starttime_format
        #
        if self.data.any():
            self.npts = len(self.data)
            self.pga_value = max(self.data, key=abs)
            self.pga_index = np.where(self.data == self.pga_value)[0][0]
        if stime and stime_frmt:
            self.starttime = dt.datetime.strptime(stime, stime_frmt)
        if sps:
            self.delta = 1 / sps
            self.timedelta = dt.timedelta(seconds=self.delta)
        if sps and self.npts:
            self.simpletime = list(np.arange(0, self.npts/sps, 1/sps))
        if self.starttime and self.timedelta and self.npts:
            self.timelist = [self.starttime + self.timedelta*ii
                             for ii in range(self.npts)]
            self.date = self.starttime.date

    def read1(self, fname):
        '''
        method for read data in specific text file.

        :type fname: str
        :param fname: file name of import text file.
        '''
        header = {}
        with open(fname) as inp:
            line = inp.readline()
            numberline = 0
            while ":" in line:
                line = line.split(':')
                key = line[0]
                val = ':'.join(line[1:]).strip()
                header[key] = val
                line = inp.readline()
                numberline += 1
        date = header['EVENT_DATE_YYYYMMDD']
        time = header['EVENT_TIME_HHMMSS']
        starttime = f'{date} {time}'
        data = np.genfromtxt(fname, skip_header=numberline)
        sps = 1/float(header['SAMPLING_INTERVAL_S'])
        event_id = header['EVENT_ID']
        network = header['NETWORK']
        station = header['STATION_CODE']
        location = None
        channel = header['STREAM']
        unit = header['UNITS']
        self.__init__(
            data=data, starttime=starttime, starttime_format='%Y%m%d %H%M%S',
            sps=sps, gain=None,
            network=network, station=station, location=location,
            channel=channel, event_id=event_id,
            unit=unit)

    @property
    def id(self):
        '''
        return an id of network.station.location.channel name.
        '''
        return f'{self.network}.{self.station}.{self.location}.{self.channel}'

    def Dmean(self, s=None):
        '''
        remove mean of signal

        :type s: float
        :param s: first seconds of signal to calculate mean (defaults to None).

        .. note::
                if you want to remove mean of whole signal, left it to defualt.
        '''
        if not s:
            mean = self.data.mean()
        else:
            indx = int(s*self.sps)
            mean = self.data[:indx].mean()
        self.data = self.data - mean

    def Differentiation(self, method='trapz'):
        '''
        method that calculate integrate of signal.

        :type method: str
        :param method: string of name of desired method to calculate
            integration. some of avilable method are trapz (defaults to trapz).
        '''
        if method == 'trapz':
            from scipy.integrate import cumtrapz
            self.data = cumtrapz(y=self.data, x=self.simpletime, initial=0)
        # update unit
        if self.unit == 'cm/s^2':
            self.unit = 'cm/s'
        elif self.unit == 'cm/s':
            self.unit = 'cm'
        else:
            self.unit = None

    def Derivative(self, method='forward'):
        '''
        method to calculate derivative of signal.

        :type method: str
        :param method: string that show what kind of method you want.
            avilable method is: forward, backward, centeral (defaults to
            forward).
        '''
        y = self.data
        #
        if method == 'forward':
            dyf = [y[i+1]-y[i] for i in range(self.npts-1)]
            dyf.append(y[-1]-y[-2])  # end sample has left sided derivative
            dyf = np.array(dyf) / self.delta
            result = dyf
        elif method == 'backward':
            dyb = [y[i]-y[i-1] for i in range(1, self.npts)]
            dyb.insert(0, y[0]-y[1])  # first sample has right sided derivative
            dyb = np.array(dyb) / self.delta
            result = dyb
        elif method == 'central':
            dyc = [(y[i+1]-y[i-1])/(2*self.delta) for i in range(1, self.npts-1)]
            # first sample has right sided derivative
            dyc.insert(0, (y[0]-y[1])/self.delta)
            # end sample has left sided derivative
            dyc.insert(-1, (y[-1]-y[-2])/self.delta)
            dyc = np.array(dyc)
            result = dyc
        self.data = result
        # update unit
        if self.unit == 'cm':
            self.unit = 'cm/s'
        elif self.unit == 'cm/s':
            self.unit = 'cm/s^2'
        else:
            self.unit = None

    @additional_docstring(plotting_kwargs=plotting_kwargs)
    def Plot(self, pga=False, **kwargs):
        '''
        plot signal

        :type pga: bool
        :param pga: if you want to show peak ground motion of signal, set it to
            True (defaults to False).
        {plotting_kwargs}
        '''
        import matplotlib.pyplot as plt
        fig = plt.figure()
        plt.plot(self.timelist, self.data, 'g', label=self.id, linewidth=0.8)
        if pga:
            plt.plot(self.timelist[self.pga_index], self.pga_value, 'ro',
                     label=f'PGA: {round(self.pga_value, 2)} [{self.unit}]')
        plt.ylabel(f"Acceleration [{self.unit}]")
        plt.xlabel(f"Time in {self.starttime.strftime('%Y-%m-%d')}")
        plt.legend()
        plt.grid()
        _finalise_figure(fig, title=f'Event ID: {self.event_id}', **kwargs)

    def copy(self):
        """
        Doc
        """
        import copy
        return copy.deepcopy(self)
