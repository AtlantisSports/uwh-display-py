
class Color(object):
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b

class Canvas(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.c = [[Color()] * width for y in range(height)]

    def get(self, x, y):
        return self.c[y][x]

    def set(self, x, y, c):
        self.c[y][x] = c
