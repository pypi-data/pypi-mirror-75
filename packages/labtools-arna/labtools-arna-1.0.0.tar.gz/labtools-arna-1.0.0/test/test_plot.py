
from LabTools.utils.uncertainties import *
from LabTools.plot import *

## Generic stuff for simulate a fit
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

fitted = ucurve_fit(model, X, Y)




def test_residual_plot():
    # Generic
    residual_plot(umodel, fitted, X, Y, use_ux = False)
    
    #PDF
    residual_plot(umodel, fitted, X, Y,
                  use_ux = False, figfile = 'test.tmp.pdf',
                  title = '\\LaTeX')
    #TKZ: actually it does not work :( 
    try:
        residual_plot(umodel, fitted, X, Y, use_ux = False, figfile = 'test.tmp.tex')
    except NotImplementedError:
        pass
        
def test_errorbars_plot():
    errorbars_plot(X,Y, xlogscale = True, ylogscale = True, figfile = 'errorbarstest.tmp.pdf')
