import matplotlib.pyplot as plt
import autograd.numpy as np

from algo.functions import beale_function_plot
from algo.functions_const import BEALE_FUNCTION_CONST_PLOT
from matplotlib.colors import LogNorm


def plot_function():
    f = lambda x, y: (1.5 - x + x * y) ** 2 + (2.25 - x + x * y ** 2) ** 2 + (2.625 - x + x * y ** 3) ** 2

    xmin, xmax, xstep = BEALE_FUNCTION_CONST_PLOT
    ymin, ymax, ystep = BEALE_FUNCTION_CONST_PLOT

    x, y = np.meshgrid(np.arange(xmin, xmax + xstep, xstep), np.arange(ymin, ymax + ystep, ystep))
    z = f(x, y)
    ax = plt.axes(projection='3d', elev=50, azim=-50)

    ax.plot_surface(x, y, z, norm=LogNorm(), rstride=1, cstride=1,
                    edgecolor='none', alpha=.8, cmap=plt.cm.jet)

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$z$')

    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))

    plt.show()
