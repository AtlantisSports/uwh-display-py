from .font import Font
from .canvas import Color

def test__get_5x7():
    f = Font.get_5x7()
    assert f.get_character('c') is f.get_character('C')
    assert f.get_character('0').get(0,0).as_hex() == Color(0,0,0).as_hex()

def test__get_11x20():
    f = Font.get_11x20()
    assert f.get_character('0').get(0,0).as_hex() == Color(0,0,0).as_hex()

def test__get_15x29():
    f = Font.get_15x29()
    assert f.get_character('0').get(0,0).as_hex() == Color(0,0,0).as_hex()

