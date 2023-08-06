
#  LabTools - uncertainties.py
#  Copyright 2019 Luca Arnaboldi

import numpy
import math
import uncertainties as unc
from uncertainties import unumpy
from scipy.optimize import curve_fit

from functools import wraps

def unarray(data, u_data):
    """
    Crea a numpy.array of ufloat given two arrays of float.

    This function is now deprecated since it's already implemented in unumpy.
    This is now only a redirect to unumpy mantained for retrocompability.
    """

    if len(data) != len(u_data):
        raise IndexError('Two arrays have different leght: {0} and {1}'.format(
        len(data),
        len(u_data),
    ))

    # Old Version
    # return numpy.array([unc.ufloat(data[i], u_data[i]) for i in range(0, len(data))])

    return unumpy.uarray(data, u_data)


def unpack_unarray(u_array):
    """
    Divide an array of ufloats in two numpy.array of floats.
    It works also for unumpy.uarray and tuple.
    """
    data = numpy.zeros(len(u_array), dtype = 'float64')
    u_data = numpy.zeros(len(u_array), dtype = 'float64')

    for i in range(0, len(u_array)):
        data[i] = u_array[i].n
        u_data[i] = u_array[i].s

    return data, u_data


def de2unc(value, dig, percent = 0., quad = True):
    # Double Error to uncertainties
    """
    Given a value with its digit error and percentage error return the uncertaties
    element.
    If quad is true the error are summated in quadrature.
    """
    err_perc = abs(value * percent / 100)
    if quad:
        error = numpy.sqrt(dig**2 + err_perc**2)
    else:
        error = abs(dig) + err_perc

    # Try with floats
    try:
        return unc.ufloat(value, error)
    # Use arrays
    except AttributeError:
        return unarray(value, error)

def ucurve_fit(f, xdata, ydata, **kwargs):
    """
    Wrapper for curve_fit that allows use of uncertainties both in model and data.
    It returns a tuple o ufloat for parametres, correlated.
    """

    x, ux = unpack_unarray(xdata)
    y, uy = unpack_unarray(ydata)

    uy = unc.covariance_matrix(ydata) # I use the covariance matrix as sigma, to fit correlated values

    @wraps(f) # need for pass the number of parametres. Without curve_fit fails
    def model(x, *pars):
        # if you give to nominal_values a standard  numpy.array it returns it
        return unumpy.nominal_values(f(x, *pars))

    p, cov = curve_fit(
        f = model,
        xdata = x,
        ydata = y,
        sigma = uy,
        **kwargs
    )

    return unc.correlated_values(p, cov)
