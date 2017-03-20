from .ppm import PPMImage, PPMException, remove_comments
from .canvas import Color
import io

def test__remove_comments():
    assert remove_comments("1234") == "1234"
    assert remove_comments("5678\t \t# comment") == "5678"

def test__load():
    infile = io.StringIO("""
P3
3 2
255
 1  2  3   4  5  6   7  8  9
10 11 12  13 14 15  16 17 18
""")
    img = PPMImage.load(infile)

    assert img.w == 3
    assert img.h == 2
    assert img.data[0] == 1
    assert img.data[1] == 2
    for i in range(0, 18):
        assert img.data[i] == i + 1
    canvas = img.as_canvas()
    for y in range(0, 1):
        for x in range (0, 2):
            idx = y * 3 * 3 + x * 3
            assert canvas.get(x, y).as_hex() == Color(idx + 1, idx + 2, idx + 3).as_hex()

    infile = io.StringIO("P6")
    try:
        img = PPMImage.load(infile)
    except PPMException as ex:
        assert str(ex) == "'Not a valid P3 PPM file'"

    infile = io.StringIO("""
P3
0 0""")
    try:
        img = PPMImage.load(infile)
    except PPMException as ex:
        assert str(ex) == "'Invalid dimensions: 0 x 0'"

    infile = io.StringIO("""
P3
1 1
254""")
    try:
        img = PPMImage.load(infile)
    except PPMException as ex:
        assert str(ex) == "'Max val must be 255'"

    infile = io.StringIO("""
P3
1 1
255
0 0 0 0""")
    try:
        img = PPMImage.load(infile)
    except PPMException as ex:
        assert str(ex) == '"Dimensions don\'t match color data"'
