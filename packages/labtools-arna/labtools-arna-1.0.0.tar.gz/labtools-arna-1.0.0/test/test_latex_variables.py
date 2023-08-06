
from LabTools.latex import Variable, Decimal, UDecimal, Document

from uncertainties import ufloat

def test_variable():
    # Basic methods testing
    v = Variable("name", "value")
    assert(v.latexcode() == "\\newcommand{\\name}{value}")
    v.setname("n4m3")
    assert(v.latexcode() == "\\newcommand{\\n4m3}{value}")
    v.setvalue("v4lu3")
    assert(v.latexcode() == "\\newcommand{\\n4m3}{v4lu3}")
    
def test_decimal():
    d = Decimal('test', 45)
    assert(d.latexcode() == "\\newcommand{\\test}{45.00}")
    d.setdigits(7)
    assert(d.latexcode() == "\\newcommand{\\test}{45.00000}")
    d.setvalue(450000100)
    assert(d.latexcode() == "\\newcommand{\\test}{4.500001e+8}")

def test_udecimal_starndard():
    ud = UDecimal("R", 3423.34768, unc = 8.2385, unc_digit = 2)
    assert(ud.latexcode() == "\\newcommand{\\R}{3423.3 \\pm 8.2 e0}")
    ud.setuncdigit(3)
    assert(ud.latexcode() == "\\newcommand{\\R}{3423.35 \\pm 8.24 e0}")
    ud.setvalue(8.436)
    ud.setuncdigit(2)
    ud.setunc(0.056)
    assert(ud.latexcode() == "\\newcommand{\\R}{8.436 \\pm 0.056 e0}")

    ud1 = UDecimal("test", 87, unc = 7, unc_digit = 2)
    try:
        assert(ud1.latexcode() == "\\newcommand{\\test}{87.0 \\pm 7.0 e0}")
    except Warning:
        pass
    ud1.setuncdigit(1)
    assert(ud1.latexcode() == "\\newcommand{\\test}{87 \\pm 7 e0}")
    ud1.setunc(7.0)
    assert(ud1.latexcode() == "\\newcommand{\\test}{87 \\pm 7 e0}")
    ud1.setuncdigit(4)
    try:
        assert(ud1.latexcode() == "\\newcommand{\\test}{87.000 \\pm 7.000 e0}")
    except Warning:
        pass
        
def test_udecimal_uncertainties():
    ud = UDecimal("test", ufloat(3423.34768, 8.2385))
    assert(ud.latexcode() == "\\newcommand{\\test}{3423 \\pm 8 e0}")
    
    a = ufloat(3.456, 0.056)
    b = ufloat(4.98, 0.000003)

    ud.setvalue(a + b)
    assert(ud.latexcode() == "\\newcommand{\\test}{8.44 \\pm 0.06 e0}")
    ud.setvalue(a*b)
    assert(ud.latexcode() == "\\newcommand{\\test}{17.2 \\pm 0.3 e0}")
    
    c = ufloat(0.0e-3, 1.3e-3)
    ud.setvalue(c)
    ud.setuncdigit(2)
    assert(ud.latexcode() == "\\newcommand{\\test}{0.0000 \\pm 0.0013 e0}")
    
    
    

def check_file_with_document(d, filename):
    with open(filename) as f:
        cnt = 0
        for l in f:
            if l.startswith('%') or l.startswith('\n'):
                continue
            assert(d.variables[cnt].latexcode() + '\n' == l)
            cnt = cnt + 1

def test_document():
    # Basic method
    d = Document()
    d.setvariable(Variable('name1', 'value1'))
    assert(d.variables[0].name == 'name1' and d.variables[0].value == 'value1')
    d.setvariable(Variable('name2', 'value2'))
    d.setvariable(Variable('name2', 'value3'))
    assert(d.variables[1].name == 'name2' and d.variables[1].value == 'value3')
    
    # Fail inserting not Variable
    try:
        d.setvariable("string")
    except TypeError:
        pass
        
    # Saving
    d.save('test.tmp')
    check_file_with_document(d, 'test.tmp')
    
    d.clearvariables()
    assert(len(d.variables) == 0)
    d.setvariable(Decimal("R", 3423.34768, 6))
    d.save('test.tmp')
    check_file_with_document(d, 'test.tmp')
    
    
    d.setvariable(UDecimal("R", ufloat(4.57,0.3)))
    d.setvariable(UDecimal("a", ufloat(4.54,0.32), unc_digit = 2))
    d.setvariable(UDecimal("b", ufloat(4.55,0.31), unc_digit = 2))
    d.setvariable(UDecimal("S", ufloat(4.56,0.30)))
    
    # Deleting
    d.removevariable("R")
    assert(len(d.variables) == 3)
    try:
        d.removevariable("R")
    except Warning:
        pass
    d.removevariable("S")
    assert(len(d.variables) == 2)
    assert(d.variables[0].latexcode() == "\\newcommand{\\a}{4.54 \\pm 0.32 e0}")
    assert(d.variables[1].latexcode() == "\\newcommand{\\b}{4.55 \\pm 0.31 e0}")
