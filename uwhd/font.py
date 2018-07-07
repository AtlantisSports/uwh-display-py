import os
from .ppm import PPMImage
from random import random

class Font(object):
    def __init__(self, name, w, h):
        self.name = name
        self.map = {}
        self.remap = lambda x : x
        self.w = w
        self.h = h

    def get_character(self, c):
        return self.map[self.remap(c)]

    def insert(self, c, filename):
        with open(filename, 'r') as img:
            self.map[c] = PPMImage.load(img).as_canvas()

    def print(self, canvas, x, y, color, s, shimmer=False):
        def print_char(canvas, x, y, color, char_img):
            for yi in range(0, self.h):
              for xi in range(0, self.w):
                  ic = char_img.get(xi, yi)
                  scale = min(1, 0.5 + random()) if shimmer else 1
                  ic.r = scale * (ic.r * color.r) / 255
                  ic.g = scale * (ic.g * color.g) / 255
                  ic.b = scale * (ic.b * color.b) / 255
                  canvas.set(x + xi, y + yi, ic)
        xi = x
        for c in s:
            print_char(canvas, xi, y, color, self.get_character(c))
            xi += self.w + 1

    @staticmethod
    def get_5x7():
        f = Font("5x7", 5, 7)

        chars = {
            '(': 'fonts/5x7/ascii_LPAREN.ppm',
            ')': 'fonts/5x7/ascii_RPAREN.ppm',
            '-': 'fonts/5x7/ascii_HYPHEN.ppm',
            '.': 'fonts/5x7/ascii_DOT.ppm',
            '/': 'fonts/5x7/ascii_FSLASH.ppm',
            '0': 'fonts/5x7/ascii_0.ppm',
            '1': 'fonts/5x7/ascii_1.ppm',
            '2': 'fonts/5x7/ascii_2.ppm',
            '3': 'fonts/5x7/ascii_3.ppm',
            '4': 'fonts/5x7/ascii_4.ppm',
            '5': 'fonts/5x7/ascii_5.ppm',
            '6': 'fonts/5x7/ascii_6.ppm',
            '7': 'fonts/5x7/ascii_7.ppm',
            '8': 'fonts/5x7/ascii_8.ppm',
            '9': 'fonts/5x7/ascii_9.ppm',
            ':': 'fonts/5x7/ascii_COLON.ppm',
            '@': 'fonts/5x7/ascii_AT.ppm',
            'A': 'fonts/5x7/ascii_A.ppm',
            'B': 'fonts/5x7/ascii_B.ppm',
            'C': 'fonts/5x7/ascii_C.ppm',
            'D': 'fonts/5x7/ascii_D.ppm',
            'E': 'fonts/5x7/ascii_E.ppm',
            'F': 'fonts/5x7/ascii_F.ppm',
            'G': 'fonts/5x7/ascii_G.ppm',
            'H': 'fonts/5x7/ascii_H.ppm',
            'I': 'fonts/5x7/ascii_I.ppm',
            'J': 'fonts/5x7/ascii_J.ppm',
            'K': 'fonts/5x7/ascii_K.ppm',
            'L': 'fonts/5x7/ascii_L.ppm',
            'M': 'fonts/5x7/ascii_M.ppm',
            'N': 'fonts/5x7/ascii_N.ppm',
            'O': 'fonts/5x7/ascii_O.ppm',
            'P': 'fonts/5x7/ascii_P.ppm',
            'Q': 'fonts/5x7/ascii_Q.ppm',
            'R': 'fonts/5x7/ascii_R.ppm',
            'S': 'fonts/5x7/ascii_S.ppm',
            'T': 'fonts/5x7/ascii_T.ppm',
            'U': 'fonts/5x7/ascii_U.ppm',
            'V': 'fonts/5x7/ascii_V.ppm',
            'W': 'fonts/5x7/ascii_W.ppm',
            'X': 'fonts/5x7/ascii_X.ppm',
            'Y': 'fonts/5x7/ascii_Y.ppm',
            'Z': 'fonts/5x7/ascii_Z.ppm',
            '{': 'fonts/5x7/ascii_LCURL.ppm',
            '}': 'fonts/5x7/ascii_RCURL.ppm',
            ' ': 'fonts/5x7/ascii_SPACE.ppm',
            '\x01': 'fonts/5x7/ascii_em1.ppm',
            '\x02': 'fonts/5x7/ascii_em2.ppm',
            '\x03': 'fonts/5x7/ascii_em3.ppm',
            '\x04': 'fonts/5x7/ascii_th1.ppm',
            '\x05': 'fonts/5x7/ascii_th2.ppm'
        }

        dir_path = os.path.dirname(os.path.realpath(__file__))

        for k, v in chars.items():
            f.insert(k, os.path.join(dir_path, v))

        f.remap = lambda x : x.upper()

        return f


    @staticmethod
    def get_11x20():
        f = Font("11x20", 11, 20)

        chars = {
            '0': 'fonts/11x20/ascii_0.ppm',
            '1': 'fonts/11x20/ascii_1.ppm',
            '2': 'fonts/11x20/ascii_2.ppm',
            '3': 'fonts/11x20/ascii_3.ppm',
            '4': 'fonts/11x20/ascii_4.ppm',
            '5': 'fonts/11x20/ascii_5.ppm',
            '6': 'fonts/11x20/ascii_6.ppm',
            '7': 'fonts/11x20/ascii_7.ppm',
            '8': 'fonts/11x20/ascii_8.ppm',
            '9': 'fonts/11x20/ascii_9.ppm',
            ':': 'fonts/11x20/ascii_COLON.ppm',
            ' ': 'fonts/11x20/ascii_SPACE.ppm'
        }

        dir_path = os.path.dirname(os.path.realpath(__file__))

        for k, v in chars.items():
            f.insert(k, os.path.join(dir_path, v))

        return f

    @staticmethod
    def get_15x29():
        f = Font("15x29", 15, 29)

        chars = {
            '0': 'fonts/15x29/ascii_0.ppm',
            '1': 'fonts/15x29/ascii_1.ppm',
            '2': 'fonts/15x29/ascii_2.ppm',
            '3': 'fonts/15x29/ascii_3.ppm',
            '4': 'fonts/15x29/ascii_4.ppm',
            '5': 'fonts/15x29/ascii_5.ppm',
            '6': 'fonts/15x29/ascii_6.ppm',
            '7': 'fonts/15x29/ascii_7.ppm',
            '8': 'fonts/15x29/ascii_8.ppm',
            '9': 'fonts/15x29/ascii_9.ppm',
            ' ': 'fonts/15x29/ascii_SPACE.ppm'
        }

        dir_path = os.path.dirname(os.path.realpath(__file__))

        for k, v in chars.items():
            f.insert(k, os.path.join(dir_path, v))

        return f


