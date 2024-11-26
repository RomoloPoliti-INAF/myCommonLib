import re
from MyCommonLib.version import __version__, Vers

def test_version_format():
    assert re.match(r"(\d+)\.(\d+)(?:\.(\d+))?(?:-(\w+)(?:\.(\d+))?)?", __version__)

def test_version_full():

    a=Vers('1.2.3-f.1')
    assert a.full() == '1.2.3'

def test_version_devel_dash():
    b=Vers('1.2.3-d.1')
    assert b.full() == '1.2.3-devel.1'

def test_version_devel_dot():
    c=Vers( '1.2.3.devel.1')
    assert c.full() == "1.2.3-devel.1"

def test_version_tuple():
    a = Vers((1, 2, 3, "d", 1))
    assert a.full() == "1.2.3-devel.1"

def test_comparison_eq():
    a=Vers((1,2,3,'d',1))
    b=Vers('1.2.3-d.1')
    assert a==b

def test_comparison_ne():
    a=Vers((1,2,3,'d',1))
    b=Vers('1.2.3-d.2')
    assert a!=b
    
def test_comparison_gt():
    a=Vers((1,2,3,'d',1))
    b=Vers('1.2.3-d.0')
    assert a>b

def test_comparison_gt_type():
    a = Vers((1, 2, 3, 'a', 1))
    b = Vers('1.2.3-d.7')
    assert a > b

def test_comparison_ge():
    a = Vers((1, 2, 3, 'd', 1))
    b = Vers('1.2.3-d.1')
    assert a >= b
    
def test_comparison_lt():
    a = Vers((1, 2, 3, 'd', 1))
    b = Vers('1.2.3-d.2')
    assert a < b
    
def test_comparison_le():
    a = Vers((1, 2, 3, 'd', 1))
    b = Vers('1.2.3-d.1')
    assert a <= b
