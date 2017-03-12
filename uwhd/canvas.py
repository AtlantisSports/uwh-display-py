
class Color(object):
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b

    def as_hex(self):
        return "#%0.2x%0.2x%0.2x" % (self.r, self.g, self.b)

class Canvas(object):
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.c = [[Color()] * self.w for y in range(self.h)]

    def get(self, x, y):
        return self.c[y][x]

    def set(self, x, y, c):
        self.c[y][x] = c
