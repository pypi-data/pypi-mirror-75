
#  LabTools - plot.py
#  Copyright 2019 Luca Arnaboldi

from .utils import unpack_unarray
import matplotlib.pyplot as plot
import numpy
from uncertainties import unumpy

from functools import wraps

##  Costant
DEFAULT_PLOT_DIMENSION = [10., 7.5]
DEFAULT_ERRORBAR_STYLE = {
    'linestyle' : '',
    'c' : 'k',
    'capsize' : 0,
    'elinewidth' : 0.7,
}
DEFAULT_PLOT_STYLE = {
    'c' : 'b',
    'lw' : .3,
}
DEFAULT_NORM_RES_STYLE = {
    'marker' : '.',
    'c' : 'b',
    'markersize' : 3.,
    'linestyle' : '',
}

DEFAULT_OUTLIERS_STYLE = {
    'linestyle' : '',
    'c' : 'red',
    'capsize' : 0,
    'elinewidth' : 0.7,
}

DEFAULT_OUTLIERS_RES_STYLE = {
    'marker': 'x',
    'linestyle' : '',
    'c' : 'red',
    'markersize' : 3.,
}

DEFAULT_SECOND_PLOT_STYLE = {
    'c' : 'g',
    'lw' : .3,
}

def rcConfig(
    usetex = True,
    latex_adds = True,
    fontsize = 12,
    ):
    """
    This defines the rcConfig for my plots.
    Thanks to: Niccolò Porciani
    """
    # Set the usage of LaTeX in labels and titles. It needs a LaTeX compiler
    # installed on the PC.
    plot.rcParams['text.usetex'] = usetex
    # LaTeX things needed:
    #   - siunitx
    #   - amsmath
    if latex_adds:
        plot.rcParams['text.latex.preamble'] = [
            r'''
            \usepackage{amsmath}
            \usepackage{siunitx}
            '''
        ]
    plot.rcParams['font.family'] = 'serif'
    plot.rcParams['font.serif'] = 'Computer Modern'
    plot.rcParams['font.size'] = fontsize

def xlimit(x, ux, logscale):
    if logscale:
        d_interval = (numpy.log10(max(x)) - numpy.log10(min(x))) * 0.01
        return (
            numpy.power(10., numpy.log10(min(x)) - d_interval),
            numpy.power(10., numpy.log10(max(x)) + d_interval)
        )
    else:
        d_interval = (max(x) - min(x)) * 0.01
        return (
            min(x) - max(ux) - d_interval,
            max(x) + max(ux) + d_interval
        )


def savepdf(fig, figfile):
    if figfile is not None:
        if figfile.endswith('tex'):
            raise NotImplementedError('tikzplotlib does not suppurt subplots.')
            """
            save_tikz(
                figure = fig,
                figurewidth = '\\linewidth',
                filepath = figfile,
                textsize = fontsize,
            )
            """
        else:
            fig.savefig(figfile, format = 'pdf', bbox_inches = 'tight')

def multi_plot(
    data,
    xlabel = "",
    ylabel = "",
    title = None,
    fontsize = 12,
    xlogscale = False,
    ylogscale = False,
    figfile = None,
    ):
    """
    Plot many set of points
    """
    # Load Configuration
    rcConfig(fontsize = fontsize)

    fig = plot.figure()
    fig.set_size_inches(*DEFAULT_PLOT_DIMENSION)
    main = plot.subplot2grid((12,9), (0,0), colspan = 9, rowspan = 12, fig = fig)

    for point_set in data:
        main.plot(point_set[0], point_set[1])

    main.minorticks_on()

    if xlogscale:
        main.set_xscale('log')

    if ylogscale:
        main.set_yscale('log')

    main.set_xlabel(xlabel)
    main.set_ylabel(ylabel)

    if title is not None:
        main.set_title(title)

    ## Salva immagine
    savepdf(fig, figfile)


def errorbars_plot(
    X,
    Y,
    xlabel = "",
    ylabel = "",
    title = None,
    fontsize = 12,
    xlogscale = False,
    ylogscale = False,
    figfile = None,
    ):
    """
    Plot points with errorbars
    """
    # Load Configuration
    rcConfig(fontsize = fontsize)

    x, ux = unpack_unarray(X)
    y, uy = unpack_unarray(Y)

    fig = plot.figure()
    fig.set_size_inches(*DEFAULT_PLOT_DIMENSION)
    main = plot.subplot2grid((12,9), (0,0), colspan = 9, rowspan = 12, fig = fig)

    main.set_xlim(xlimit(x, ux, xlogscale))

    main.minorticks_on()
    main.errorbar( x, y, xerr = ux, yerr = uy, **DEFAULT_ERRORBAR_STYLE)

    if xlogscale:
        main.set_xscale('log')

    if ylogscale:
        main.set_yscale('log')

    main.set_xlabel(xlabel)
    main.set_ylabel(ylabel)

    if title is not None:
        main.set_title(title)

    ## Salva immagine
    savepdf(fig, figfile)



def residual_plot(
    f,
    param,
    X,
    Y,
    use_ux = True,
    df = None,
    xlabel = "",
    normres = True,
    fontsize = 12,
    ylabel = "",
    title = None,
    rylabel = None,
    xlogscale = False,
    ylogscale = False,
    outliers = None,
    figfile = None,
    second_f = None,
    #second_df = None,
    second_param = None,
    ):
    """
    It takes X and Y as unumpy.uarray and makes a plot with the residual graph.
    """

    # Load Configuration
    rcConfig(fontsize = fontsize)

    # Redefine f  and df for curvefit
    @wraps(f) # need for pass the number of parametres. Without, curve_fit fails
    def uf(x, *pars):
        # if you give to nominal_values a standard  numpy.array it returns it
        return unumpy.nominal_values(f(x, *pars))
    # df is analogous
    if df is not None:
        @wraps(df)
        def udf(x, *pars):
            return unumpy.nominal_values(df(x, *pars))

    # Processing the second function
    if second_f is not None:
        @wraps(second_f)
        def suf(x, *pars):
            return unumpy.nominal_values(second_f(x, *pars))
    """
    if second_df is not None:
        @wraps(second_df)
        def sudf(x, *pars):
            return unumpy.nominal_values(second_f(x, *second_pars))
    """



    x, ux = unpack_unarray(X)
    y, uy = unpack_unarray(Y)
    pars, upars = unpack_unarray(param)

    fig = plot.figure()
    fig.set_size_inches(*DEFAULT_PLOT_DIMENSION)
    main = plot.subplot2grid((12,9), (0,0), colspan = 9, rowspan = 6, fig = fig)
    res = plot.subplot2grid((12,9), (6,0), colspan = 9, rowspan = 3, fig = fig)

    fig.subplots_adjust(hspace=0) # Non lascia spazio tra i grafici

    ## Calcola residui
    #Propago errori su y da x
    if use_ux:
        if df is None:
            raise TypeError('Errors on x were given but no derivative of f')
        else:
            errore = numpy.sqrt( uy**2 + (udf(x, *pars) * ux)**2 )
    else:
        errore = uy
    residui = y - uf(x, *pars)
    if normres:
        residui = residui / errore

    # Adding the outliers if not present
    if outliers is None:
        outliers = [False] * len(X)


    ## Setto i limiti sulle x
    xlim = xlimit(x, ux, xlogscale)
    main.set_xlim(xlim)
    res.set_xlim(xlim)

    ##Crea la grid appropriata e setta i limiti
    if xlogscale:
        d_interval = (numpy.log10(max(x)) - numpy.log10(min(x))) * 0.01
        grid = numpy.logspace(
            numpy.log10(min(x)) - d_interval,
            numpy.log10(max(x)) + d_interval,
            1000
        )
    else:
        d_interval = (max(x) - min(x)) * 0.01
        grid = numpy.linspace(
            min(x) - max(ux) - d_interval,
            max(x) + max(ux) + d_interval
        )

    # Plot dei punti
    for i in range(0, len(X)):
        err_bar_style = DEFAULT_ERRORBAR_STYLE
        norm_res_style = DEFAULT_NORM_RES_STYLE
        if outliers[i]:
            err_bar_style = DEFAULT_OUTLIERS_STYLE
            norm_res_style = DEFAULT_OUTLIERS_RES_STYLE

        main.errorbar(x[i], y[i], xerr = ux[i], yerr = uy[i], **err_bar_style)
        if normres:
            res.plot(x[i], residui[i], **norm_res_style)
        else:
            res.errorbar(x[i], residui[i], xerr = 0., yerr = uy[i], **err_bar_style)

    # Grafico curva
    #main.grid()
    main.minorticks_on()
    main.plot(grid, uf(grid, *pars), **DEFAULT_PLOT_STYLE)
    if second_f is not None:
        main.plot(grid, suf(grid, *second_param), **DEFAULT_SECOND_PLOT_STYLE)

    if xlogscale:
        main.set_xscale('log')

    if ylogscale:
        main.set_yscale('log')
    main.set_xticklabels([]) #Leva i numeri sotto il primo grafico

    main.set_ylabel(ylabel)
    if title is not None:
        main.set_title(title)

    ## Grafico residui (solo impostazioni, i punti li ho già messi sopra)
    #res.grid()
    res.minorticks_on()
    res.plot(grid, grid * 0., **DEFAULT_PLOT_STYLE)


    if xlogscale:
        res.set_xscale('log')

    res.set_xlabel(xlabel)

    if rylabel is None:
        if normres:
            res.set_ylabel('Res. Norm')
    else:
        res.set_ylabel(rylabel)



    ## Salva immagine
    savepdf(fig, figfile)
