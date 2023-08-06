
#  LabTools - latex.py
#  Copyright 2019 Luca Arnaboldi


from .utils import significant_digits, move_decimal, most_significant_digit
from .utils import pair_decimal_with_uncertainty, unpack_unarray
from .utils import percentual_error_digit
import numpy

DEFAULT_SIGNIFICANT_DIGITS = 4
DEFAULT_UNC_DIGITS = 2
DEFAULT_UNC_PERCENT_ACCURACY = 25
FILE_HEADER = '''
% File generated with LabTools.latex
% Copyright (c) Luca Arnaboldi 2019

'''


################################################################################
# Tables

class TabularColumn():
    
    def __init__(
        self,
        array,
        show_unc=None,
        siunitx_num=None,
        global_unc=None,
        unc_digits=None,
        value_digits=None,
        unc_perc_accuracy=None
    ):
        try:
            self.array, self.unc = unpack_unarray(array)
        except AttributeError:
            self.array = array
            self.unc = numpy.array([None] * len(array))
        self.show_unc = show_unc
        self.siunitx_num = siunitx_num
        self.global_unc = global_unc
        self.unc_digits = unc_digits
        self.value_digits = value_digits
        self.unc_perc_accuracy = unc_perc_accuracy
    

class TabularContent():
    
    def __init__(
        self,
        hlines=False, 
        show_unc=True,
        siunitx_num=True,
        unc_digits=None,
        value_digits=DEFAULT_SIGNIFICANT_DIGITS,
        unc_perc_accuracy = DEFAULT_UNC_PERCENT_ACCURACY,
    ):
        self.hlines = hlines
        self.show_unc = show_unc
        self.siunitx_num = siunitx_num
        self.unc_digits = unc_digits
        self.value_digits = value_digits
        self.unc_perc_accuracy = unc_perc_accuracy
        self.columns = []
        
    def add_column(self, *args, **kwargs):
        if args[0].__class__.__name__ == 'ndarray':
            self.columns.append(TabularColumn(args[0], **kwargs))
        elif args[0].__class__.__name__ == 'TabularColumn':
            self.columns.append(args[0])
        else:
            raise(TypeError('TabularContent.add_column() does not support this arguments.'))
        
        
    def save(self, filename):
        tex = FILE_HEADER
        tex += '% Include this code in tabular enviroment to display this content\n'
        
        # Get the number of rows
        content_lines = []
        number_of_rows = 0
        for c in self.columns:
            number_of_rows = max(number_of_rows, len(c.array))
        
        # build the content lines
        content_lines = [""] * number_of_rows
        
        # Insert elements
        for i in range(0, len(self.columns)):
            c = self.columns[i]
            cnt = 0 # Count how many row in this column
            
            ## Setting up column
            # show_unc
            show_unc = self.columns[i].show_unc
            if show_unc == None:
                show_unc = self.show_unc
            # siunitx_num
            siunitx_num = self.columns[i].siunitx_num
            if siunitx_num == None:
                siunitx_num = self.siunitx_num
            # unc_digits
            unc_digits = self.columns[i].unc_digits
            if unc_digits == None:
                unc_digits = self.unc_digits
            # value_digits
            value_digits = self.columns[i].value_digits
            if value_digits == None:
                value_digits = self.value_digits
            # unc_perc_accuracy
            unc_perc_accuracy = self.columns[i].unc_perc_accuracy
            if unc_perc_accuracy == None:
                unc_perc_accuracy = self.unc_perc_accuracy
            
            
            for j in range(0, len(c.array)):
                cnt += 1 # Add 1 to the row counter
                
                # There's no unc for this column (neither gloabal or local)
                if c.global_unc == None and c.unc.all() == None:
                    if siunitx_num == False:
                        raise(NotImplementedError('siunitx_num = False'))
                    else:
                        content_lines[j] += '\\num{{{0}}}'.format(
                            significant_digits(c.array[j], value_digits, True)
                        )
                # There's unc
                else:
                    if siunitx_num == False:
                        raise(NotImplementedError('siunitx_num = False'))
                    else:
                        # If there's global_unc
                        if c.unc.all() == None:
                            act_unc = c.global_unc
                        else:
                            act_unc = c.unc[j]
                            
                        # Compute the number of digit of the uncertainty of this
                        # element.
                        if unc_digits == None:
                            unc_digits = percentual_error_digit(
                                act_unc,
                                unc_perc_accuracy,
                            )
                        assert(not unc_digits == None)
                        value_s, unc_s, e, warn = pair_decimal_with_uncertainty(
                            c.array[j],
                            act_unc,
                            unc_digits,
                        )
                        content_lines[j] += '\\num{{{0}'.format(value_s)
                        if show_unc:
                            content_lines[j] += ' \\pm {0}'.format(unc_s)
                        content_lines[j] += ' e{0}}}'.format(e)
                        
                # Next element. Last column & is removed next
                content_lines[j] += ' &'

            # Fill the empty lines of the table
            while cnt < number_of_rows:
                content_lines[cnt] += ' &'
                cnt += 1
                    
                    
                

        # End lines and attach to the tex
        for l in content_lines:
            l = l[:-1] # Remove & char at the end of the line
            l += ' \\\\'
            if self.hlines:
                l += ' \\hline'
            tex += l + '\n'
        
        # Write file
        with open(filename, 'w') as tfile:
            tfile.write(tex)



################################################################################
# Variables

class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def setvalue(self, value):
        self.value = value

    def setname(self, name):
        self.name = name

    def latexcode(self):
        return '\\newcommand{{\\{0}}}{{{1}}}'.format(
            self.name,
            str(self.value),
        )


class Decimal(Variable):
    """
        It needs Latex Package siunitx to work properly.
    """
    def __init__(self, name, value, digits=DEFAULT_SIGNIFICANT_DIGITS):
        super().__init__(name, float(value))
        self.digits = digits

    def setdigits(self, digits):
        self.digits = digits

    def latexcode(self, ):
        return '\\newcommand{{\\{0}}}{{{1}}}'.format(
            self.name,
            significant_digits(self.value, self.digits, True),
        )


class UDecimal(Variable):
    """
    It needs Latex Package siunitx to work properly.
    """

    def __init__(self, name, value, unc_digit=None, unc_perc_accuracy = DEFAULT_UNC_PERCENT_ACCURACY, unc = None):
        # uncertainties.ufloat passed
        if unc is None:
            value_ = value.nominal_value
            unc_ = value.std_dev
        # other case
        else:
            value_ = value
            unc_ = unc
            
        super().__init__(name, value_)
        self.unc = float(unc_)
        if unc_digit is None:
            self.unc_digit = percentual_error_digit(
                self.unc,
                unc_perc_accuracy,
            )
        else:
         self.unc_digit = int(unc_digit)

    def setunc(self, unc):
        self.unc = float(unc)

    def setuncdigit(self, unc_digit):
        self.unc_digit = int(unc_digit)
        
    def setvalue(self, value):
        try:
            self.value = value.nominal_value
            self.unc = value.std_dev
        except AttributeError:
            self.value = float(value)

    def latexcode(self):
        to_print_value, to_print_unc, unc_digit_rep, warn = pair_decimal_with_uncertainty(
            self.value,
            self.unc,
            self.unc_digit,
        )
        
        # Raise a warning if adding digits to uncertanty
        if warn:
            raise Warning("""uncertanty of Udecimal '{0}' has more digit than
                             orginal value: {1} -- {2}""".format(self.name,
                                                                 self.unc,
                                                                 to_print_unc))

        return '\\newcommand{{\\{0}}}{{{1} \\pm {2} e{3}}}'.format(
            self.name,
            to_print_value,
            to_print_unc,
            unc_digit_rep,
        )


class Document:
    def __init__(self):
        self.variables = []

    def setvariable(self, variable):
        # Check correct type
        if issubclass(variable.__class__, Variable):
            # Try to replace an existence one
            for i in range(0, len(self.variables)):
                if self.variables[i].name == variable.name:
                    self.variables[i] = variable
                    return
            # Adding if not present
            self.variables.append(variable)
        else:
            raise TypeError('object {0} ({1}) is not a valid variable.'.format(
                variable,
                type(variable),
            ))

    def removevariable(self, name):
        for i in range(0, len(self.variables)):
            if self.variables[i].name == name:
                del self.variables[i]
                return
        raise Warning('failed removing {0}. Variable {0} not in Document'.format(
            name,
        ))

    def clearvariables(self):
        self.variables.clear()

    def save(self, filename):
        # Header message
        tex = FILE_HEADER
        tex += '% Include this file in your LaTex project to use these definitions\n\n'

        # Variables 
        tex += '% Variables\n'
        for v in self.variables:
            tex += v.latexcode() + '\n'
        
        with open(filename, 'w') as tfile:
            tfile.write(tex)
