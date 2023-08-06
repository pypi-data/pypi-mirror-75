
from LabTools.utils.uncertainties import *

from uncertainties import ufloat, correlated_values



def test_unarray_unpackuarray():
    a = numpy.array([ufloat(2, 3), ufloat(4, 5), ufloat(6., 7.)])
    b = numpy.array([2, 4, 6.])
    c = numpy.array([3, 5, 7.])
    d = numpy.array([3., 2.])

    b_, c_ = unpack_unarray(a)
    assert(b.all() == b_.all())
    assert(c.all() == c_.all())

    a_ = unarray(b, c)
    # We need str beacuse uncertainties behavior with comparsion
    assert(str(a_.all()) == str(a.all()))

    assert(str(a.all()) == str(unarray(*unpack_unarray(a)).all()))
    b__, c__ = unpack_unarray(unarray(b, c))
    assert(b__.all() == b.all())
    assert(c__.all() == c.all())
    try:
        unarray(a, d)
    except IndexError:
        pass

def test_de2unc():
    # Test Lab3
    assert(str(de2unc(1.673, 0.001, 0.5)) == '1.673+/-0.008')
    assert(str(de2unc(1.673, 0.001, 0.5, False)) == '1.673+/-0.009')

    assert(str(de2unc(0.167, 0.001, 0.5)) == '0.1670+/-0.0013')
    assert(str(de2unc(0.167, 0.001, 0.5, False)) == '0.1670+/-0.0018')

    # Misura negativa
    assert(str(de2unc(-1.673, 0.001, 0.5)) == '-1.673+/-0.008')
    assert(str(de2unc(-1.673, 0.001, 0.5, False)) == '-1.673+/-0.009')

    a = numpy.array([1.0, 2.0])
    b = numpy.array([0.1, 0.2])
    c = numpy.array([1, 1])
    res = numpy.array([ufloat(1.0, 0.100498), ufloat(2.00, 0.2009)])

    assert(str(de2unc(a, b, c).all()) == str(res.all()))

def test_ucurve_fit():
    """
    This is not testing the correcteness of the fit or the error propagation of
    uncertainties. It is only checking if it works in every case I need.
    """
    def model(x, a, b):
        return numpy.sqrt(a * x + b)

    def umodel(x, a, b):
        return unumpy.sqrt(a * x + b)


    x = numpy.array([3., 41., 100.])
    y = numpy.array([5., 15., 25.])
    ux = x / 100.
    uy = y / 100.

    X = unarray(x, ux)
    Y = unarray(y, uy)


    fitted1 = ucurve_fit(model, X, Y)
    fitted2 = ucurve_fit(umodel, X, Y)

    assert(str(fitted1[0]) == str(fitted2[0]))
    assert(str(fitted1[1]) == str(fitted2[1]))

def test_ucurve_fit_correlation():
    def model(x, a, b):
        return numpy.sqrt(a * x + b)
    def umodel(x, a, b):
        return unumpy.sqrt(a * x + b)

    x = numpy.array([3., 41., 100.])
    ux = x / 100.

    y = numpy.array([5., 15., 25.])
    uy = numpy.array([[0.01, 0.001,  0.01],
                      [0.001,  0.01, 0.02],
                      [0.01, 0.02, 0.05]])

    p, cov = curve_fit(model, x, y, sigma=uy)
    fitted1 = correlated_values(p, cov)
    X = unarray(x, ux)
    Y = correlated_values(y, uy)
    fitted2 = ucurve_fit(umodel, X, Y)

    assert(str(fitted1[0]) == str(fitted2[0]))
    assert(str(fitted1[1]) == str(fitted2[1]))
