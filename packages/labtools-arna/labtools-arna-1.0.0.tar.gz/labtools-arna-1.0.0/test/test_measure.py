
from LabTools.measure import *
import numpy as np


def test_instrument():
    i = Instrument('test/inputs/instrument1.yaml')
    assert(str(i.measure('tipo1', 15.)) == '15+/-10')
    assert(str(i.measure('tipo1', 74.6)) == '75+/-12')
    assert(str(i.measure('tipo1', 0.34)) == '0.34+/-0.05')
    
    assert(str(i.measure('tipo2', 1.876)) == '1.876+/-0.031')
    assert(str(i.measure('tipo2', 1.876, 5.000)) == '1.876+/-0.021')
    
    # Tipo che non esiste
    try:
        i.measure('tipononesiste', 0.)
    except KeyError:
        pass
        
    # Provo a passare un value che non è un float
    try:
        i.measure('tipo1', 'uno')
    except ValueError:
        pass
        
    # Fuori il fondoscala più grande
    try:
        i.measure('tipo1', 5000.)
    except ValueError:
        pass
        
    # Fondoscala che non esiste
    try:
        i.measure('tipo1', 5., fond = 50.)
    except ValueError:
        pass
        
def test_tester():
    t = Tester('test/inputs/multimetro_digitale.yaml')
    v = np.array([2.87, 89.7])
    t.voltage(v)
    
def test_oscilloscope():
    o = Oscilloscope('test/inputs/oscilloscopio.yaml')
    
    v = np.array([2.87, 89.7e-2])
    o.voltage(v)
    
    t = np.array([1.6e-6, 12.e-3])
    o.time(t)
    o.frequency(1./t)
    
    
