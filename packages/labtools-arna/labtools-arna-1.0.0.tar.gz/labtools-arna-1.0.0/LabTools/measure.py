
#  LabTools - measure.py
#  Copyright 2019 Luca Arnaboldi

from .utils import de2unc

import numpy
from operator import attrgetter
import yaml

class Instrument():
    """
    This class handle a generic misuration instrument.
    The configuration must be given in a configuration file in YAML format.
    """
    
    def __init__(self, config):
        with open(config) as conf:
            self.measure_types = yaml.full_load(conf)
        
        # Sort all the measure types by ascending order of scale
        for measure_type, scale in self.measure_types.items():
            scale.sort(key = lambda scale: scale['full-scale'])
            
    def measure_single(self, measure_type, value, fond = None):
        """
        Take a value measured with this instrument and it returns an uncertainty
        item. The error is calculated with the specification for this instrument
        given in the configuration.
        If fond is None the best full-scale one is choosed.
        """

        ref = float(value)
        
        for item in self.measure_types[measure_type]:
            if (fond is None and value < item['full-scale']) or (fond is not None and float(fond) == float(item['full-scale'])):
                return de2unc(
                    value,
                    item['resolution'] * item['digit_error'],
                    item['percentage_error'],
                )
        # Right full-scale not found        
        raise ValueError('Unable to compute this measure: {0}, {1}, {2}'.format(
            measure_type,
            value,
            fond
        ))
        
    def measure_array(self, measure_type, data, fond = None):
        
        if fond is not None:
            if len(data) != len(fond):
                raise IndexError('Two arrays have different leght: {0} and {1}'.format(
                len(data),
                len(fond),
            ))
        else:
            fond = [None] * len(data)
            
        return numpy.array(
            [self.measure_single(measure_type, data[i], fond[i]) for i in range(0, len(data))]
        )
        
    def measure(self, measure_type, value, fond = None):
        try:
            return self.measure_single(measure_type, value, fond)
        except TypeError:
            return self.measure_array(measure_type, value, fond)
            
        

class Tester(Instrument):
    """
    Class specialized for the multimeter.
    Voltage are in V.
    Currents are in mA.
    Capacitance are in nF.
    Resistance are in Ohm.
    """
    
    def voltage(self, value, fond = None, AC = False): 
        if AC:
            measure_type = 'ACtension'
        else:
            measure_type = 'DCtension'
        return self.measure(measure_type, value, fond)
    
    def current(self, value, fond = None, AC = False):
        if AC:
            measure_type = 'ACcurrent'
        else:
            measure_type = 'DCcurrent'
        return self.measure(measure_type, value, fond)
         
    def resistance(self, value, fond = None):
        return self.measure('resistance', value, fond)
        
    def capacitance(self, value, fond = None):
        return self.measure('capacitance', value, fond)
        
    def frequency(self, value, fond = None):
        return self.measure('frequency', value, fond)
        
    def temperature(self, value, fond = None):
        return self.measure('temperature', value, fond)


class Oscilloscope(Instrument):
    
    def voltage(self, value, fond = None):
        return self.measure('voltage', value, fond)
    
    def time(self, value, fond = None):
        return self.measure('time', value, fond)
    
    def trigger_frequency(self, value):
        return self.measure('trigger_frequency', value)
        
    def time_frequency(self, value, fond = None):
        return self.measure('frequency', value, fond)
    
    def frequency(self, value, fond = None):
        # The frequency measure is given by the time
        return 1./ self.time_frequency(1./value, fond)
        
    

