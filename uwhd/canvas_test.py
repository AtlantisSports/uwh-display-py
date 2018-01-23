from .canvas import Color, Canvas

def test__Color():
    col = Color()
    assert col.r == 0
    assert col.g == 0
    assert col.b == 0

    col = Color(1, 2, 3)
    assert col.r == 1
    assert col.g == 2
    assert col.b == 3

    col = Color(1.1, 2.1, 3.1)
    assert col.r == 1
    assert col.g == 2
    assert col.b == 3


def test__Canvas_as_hex():
    col = Color(1, 2, 3)
    assert "#010203" == col.as_hex()

def test__Canvas():
    canv = Canvas(2, 3)
    assert canv.w == 2
    assert canv.h == 3

    px = canv.get(0, 0)
    assert px.r == 0
    assert px.g == 0
    assert px.b == 0

    px = canv.get(1, 2)
    assert px.r == 0
    assert px.g == 0
    assert px.b == 0

    canv.set(0, 0, Color(253, 254, 255))
    assert canv.get(0,0).r == 253
    assert canv.get(0,0).g == 254
    assert canv.get(0,0).b == 255
