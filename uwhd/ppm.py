from .canvas import Canvas, Color

class PPMException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


def remove_comments(s):
    (data, cchar, comment) = s.partition('#')
    return data.rstrip(" \n\t")


class PPMImage(object):
    def __init__(self, w, h, data):
        self.w = w
        self.h = h
        self.data = data

    @staticmethod
    def load(infile):
        magic = ""
        while magic == "":
            line = infile.readline()
            magic = remove_comments(line)
        if (magic != "P3"):
            raise PPMException("Not a valid P3 PPM file")

        line = infile.readline()
        (w, space, h) = remove_comments(line).partition(" ")
        w, h = int(w), int(h)

        if w <= 0 or h <= 0:
            raise PPMException("Invalid dimensions: %d x %d" % (w, h))

        line = infile.readline()
        max_val = int(remove_comments(line))
        if (max_val != 255):
            raise PPMException("Max val must be 255")

        color_data = []
        for line in infile:
            line = remove_comments(line)
            color_data += [x for x in line.split(' ') if x != ' ' and x != '']

        color_data = [int(x) for x in color_data]

        if len(color_data) != w * h * 3:
            raise PPMException("Dimensions don't match color data %d != %d * %d * 3" % (len(color_data), w, h))

        return PPMImage(w, h, color_data)

    def fill_canvas(self, canvas):
        assert self.w == canvas.w
        assert self.h == canvas.h
        for y in range(self.h):
            for x in range(self.w):
                index = y * self.w * 3 + x * 3
                canvas.set(x, y, Color(self.data[index],
                                       self.data[index+1],
                                       self.data[index+2]))

    def as_canvas(self):
        canvas = Canvas(self.w, self.h)
        self.fill_canvas(canvas)
        return canvas
