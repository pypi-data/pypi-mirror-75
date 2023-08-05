import datetime
import warnings

import numpy as np
import matplotlib

from hapiclient.plot.datetick import datetick

# https://github.com/pandas-dev/pandas/issues/18301
# Suppresses depreciation warning.
# TODO: determine what version of pandas this is needed for.
# Observed in Matplotlib 3.0, pandas 0.25.3, Python 3.5.
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
    
def timeseries(t, y, **kwargs):
    '''Plot a time series

    '''

    opts = {
                'logging': False,
                'title': '',
                'xlabel': '',
                'ylabel': '',
                'logx': '',
                'logy': '',
                'backend': 'default',
                'returnimage': False,
                'transparent': False,
                'legendlabels': []
            }

    for key, value in kwargs.items():
        if key in opts:
            opts[key] = value
        else:
            warnings.warn('Warning: Ignoring invalid keyword option "%s".' % key, SyntaxWarning)

    if opts['returnimage']:
        # When returnimage=True, the Matplotlib OO API is used b/c it is thread safe.
        # Otherwise, the pyplot API is used. Ideally would always use the OO API,
        # but this has problems with notebooks and showing figure when executing
        # a script from the command line.
        # TODO: Document issues.
        #
        # API differences description:
        # https://www.saltycrane.com/blog/2007/01/how-to-use-pylab-api-vs-matplotlib-api_3134/
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    else:
        from matplotlib import pyplot as plt
        if opts['logging']: print("timeseries(): Using Matplotlib back-end " + matplotlib.get_backend())

    if y.shape[0] < 11:
        props = {'linestyle': 'none', 'marker': '.', 'markersize': 16}
    elif y.shape[0] < 101:
        props = {'lineStyle': '-', 'linewidth': 2, 'marker': '.', 'markersize': 8}
    else:
        props = {}

    ylabels = []

    if issubclass(y.dtype.type, np.flexible):
        # See https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.scalars.html
        # for diagram of subclasses.
        # Find unique strings and give each an integer value.
        # Modify tick labels to correspond to unique strings
        yu = np.unique(y)
        if len(yu) > 20:
            # Too many labels in this case. One option is to find
            # number of unique first characters and change labels to
            # "first character" and then warn. If number of unique first
            # characters < 21, try number of unique second characters, etc.
            raise ValueError('Can only plot strings if number of unique strings < 21')
        yi = np.zeros((y.shape))
        for i in range(0, len(yu)):
            yi[y == yu[i]] = i
        ylabels = yu
        y = yi

    # Can't use matplotlib.style.use(style) because not thread safe.
    # Set context using 'with'.
    # Setting stylesheet method: https://stackoverflow.com/a/22794651/1491619
    if opts['returnimage']:
        # See note above about OO API for explanation for why this is
        # done differently if returnimage=True
        fig = Figure()
        FigureCanvas(fig) # Not used directly, but calling attaches canvas to fig which is needed by datetick and hapiplot.
        ax = fig.add_subplot(111)
        ax.plot(t, y, **props)
        ax.set(ylabel=opts['ylabel'], xlabel=opts['xlabel'], title=opts['title'])
        try:
            ax.ticklabel_format(axis='y', style='sci', scilimits=(-3,3), useMathText=True)
        except:
            pass
        ax.set_position([0.12,0.125,0.850,0.75])
        if opts['legendlabels'] != []:
            ax.legend(opts['legendlabels'])
    else:

        #plt.figure()
        #plt.clf()
        plt.plot(t, y, **props)
        plt.gcf().canvas.set_window_title(opts['title'])
        plt.ylabel(opts['ylabel'])
        plt.xlabel(opts['xlabel'])
        plt.title(opts['title'])

        if opts['legendlabels'] != []:
            plt.legend(opts['legendlabels'])
        ax = plt.gca()
        ax.set_position([0.12,0.125,0.850,0.75])
        try:
            ax.ticklabel_format(axis='y', style='sci', scilimits=(-3,3), useMathText=True)
        except:
            pass

    ax.grid()

    if len(ylabels) > 0:
        ax.set_yticks(np.unique(y))
        ax.set_yticklabels(ylabels)

    if isinstance(t[0], datetime.datetime):
        datetick('x', axes=ax)
    if isinstance(y[0], datetime.datetime):
        datetick('y', axes=ax)
    
    # See
    # https://stackoverflow.com/questions/24581194/matplotlib-text-bounding-box-dimensions
    # for determining text bounding box in figure coordinates
    if False:
        for item in ax.get_yticklabels():
            ml = 0 # max length
            for t in item.get_text().split('\n'):
                l = len(t)
                if l > ml: ml = l 
    
    # savefig.transparent=True requires the following for the saved image
    # to have a transparent background. Seems as though figure.facealpha
    # and axes.facealpha should be rc parameters, but they are not. So
    # savefig.transparent controls both transparency in saved image and
    # in GUI image.
    if opts['transparent']:
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)

    if not opts['returnimage']:
        plt.show()
        fig = plt.gcf()

    return fig
