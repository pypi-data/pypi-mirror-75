
#  LabTools - significant_digit
#  Copyright 2019 Luca Arnaboldi

import math


def significant_digits(x, p, compact = False):
    """
    Code heavily ispired from https://github.com/randlet/to-precision
    
    Convert x in a string written with p significant digit and the  exponent of the 
    exponential notation.
    If compact is True it retuens only a string. Example:
    0.00345, 2, False --> ("3.4", -3)
    0.00345, 2, True  --> "3.4e-3"
    """
    x = float(x)

    if x == 0.:
        ans = "0." + "0"*(p-1)
        if not compact:
            return ans, 0
        else:
            return ans

    out = []

    if x < 0:
        out.append("-")
        x = -x

    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x/tens)

    if n < math.pow(10, p - 1):
        e = e - 1
        tens = math.pow(10, e - p+1)
        n = math.floor(x / tens)

    if abs((n + 1.) * tens - x) <= abs(n * tens -x):
        n = n + 1

    if n >= math.pow(10,p):
        n = n / 10.
        e = e + 1

    m = "%.*g" % (p, n)
    
    exp_notation = False

    if e < -2 or e >= p:
        out.append(m[0])
        if p > 1:
            out.append(".")
            out.extend(m[1:p])

        if compact:
            out.append('e')
            if e > 0:
                out.append("+")
            out.append(str(e))
        else:
            exp_notation = True
    elif e == (p - 1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e+1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e+1:])
    else:
        out.append("0.")
        out.extend(["0"]*-(e+1))
        out.append(m)
        
    if exp_notation:
        exponent = e
    else:
        exponent = 0

    if compact:
        return "".join(out)
    else:
        return "".join(out), exponent



def most_significant_digit(x):
    """
    Return the exponent of themost significant digit of a number x
    """
    if x == 0.:
        return 0
    return int(math.floor(math.log10(abs(x))))


def move_decimal(number, delta):
    """
    Move the decimal separator of delta digits.
    """
    float(number) # Check that number is representing a float
    
    if delta == 0:
        return number
        
    p = number.find('.')
    
    if p == -1:
        number += '.' # This will not affect the orginal argument
        p = len(number) - 1
    
    if delta > 0:
        ans = number[:p]
        if p + 1 + delta < len(number):
            ans += number[p + 1:p + 1 + delta]
            ans += "."
            ans += number[p + 1 + delta:len(number)]
        else:
            ans += number[p + 1:len(number)]
            ans += "0" * (p + 1 + delta - len(number))
        return ans
    else:
        if p + delta <= 0:
            ans = "0."
            ans += "0" * (-(p + delta))
            ans += number[:p] + number[p + 1:len(number)]
        else:
            ans = number[:p + delta]
            ans += "."
            ans += number[p + delta : p]
            ans += number[p + 1 : len(number)]
        return ans 

def pair_decimal_with_uncertainty(value, unc, digits):
    """
    Given a two float value, unc, a number and its uncertanty, and digits the number
    of significant difits of the uncertanty, it returns a tuple containg (a, b, e),
    where:
    - a: is a string for value;
    - b: is a string for unc;
    - e: the common exponent.
    - warn: it is if the number of digits of the uncertainty is increased
    Strings are formatted in a way that (a +- b) 10^e is the correct representation
    of the numbers.
    """
    # Calculate the position of most significant digit of value and unc
    unc_digit = most_significant_digit(unc)
    value_digit = most_significant_digit(value)

    # Get the value and unc with the appropiate number of significant digits
    to_print_unc, unc_digit_rep = significant_digits(unc, digits)
    to_print_value, value_digit_rep = significant_digits(
        value,
        max(value_digit - unc_digit + digits, 0)
    )
    
    # return a warning if adding digits to uncertanty
    if len(str(unc)) < len(to_print_unc):
        warn = True
    else:
        warn = False

    # Move the unc value until it has the same exponent of the value
    to_print_unc = move_decimal(
        to_print_unc,
        unc_digit_rep - value_digit_rep
    )
    
        
    return to_print_value, to_print_unc, value_digit_rep, warn
    
    
def percentual_error_digit(value, percentage):
    """
    Given value and a percentage return the number of significant digits of value
    needed for specify the value up to percentage%.
    """
    
    d = 1
    approx = float(significant_digits(value, d, True))
    while abs(value - approx)/min(approx, value) > float(percentage)/100.:
        d += 1
        approx = float(significant_digits(value, d, True))
        
    return d
        
