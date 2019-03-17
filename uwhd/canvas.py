
class Color(object):
    def __init__(self, r=0, g=0, b=0):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b

    def as_hex(self):
        return "#%0.2x%0.2x%0.2x" % (self.r, self.g, self.b)

    def copy(self):
        # FIXME: is there a pythonic way of doing this?
        return Color(self.r, self.g, self.b)

class Canvas(object):
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.c = [[Color()] * self.w for y in range(self.h)]

    def get(self, x, y):
        return self.c[y][x].copy()

    def set(self, x, y, c):
        if x < self.w and y < self.h:
            self.c[y][x] = c

    def clear(self):
        for i in range(self.w):
            for j in range(self.h):
                self.c[j][i] = Color()
