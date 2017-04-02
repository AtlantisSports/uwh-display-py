from .font import Font
from .canvas import Color, Canvas

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

def test__print():
    f = Font.get_5x7()
    c = Canvas(12, 7)
    f.print(c, 0, 0, Color(255, 255, 255), "ab")
    a = f.get_character('a')
    b = f.get_character('b')
    for yi in range(0, 7):
        for xi in range(0, 5):
            assert c.get(xi, yi) == a.get(xi, yi)
            assert c.get(xi + 6, yi) == b.get(xi, yi)
