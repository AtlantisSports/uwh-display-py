from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from .canvas_viewer import CanvasViewer

class MatrixCanvasViewer(CanvasViewer):
    def __init__(self, window=None):
        options = RGBMatrixOptions()
        options.rows = 32
        options.chain_length = 3
        options.parallel = 1
        options.hardware_mapping = 'regular'

        self._matrix = RGBMatrix(options=options)

        self._image = Image.new("RGB", (self._matrix.width,
                                        self._matrix.height),
                                "white")

        self._offscreen = self._matrix.CreateFrameCanvas()

        if window is None:
            window = { 'w': c.w, 'h': c.h, 'x': 0, 'y': 0, 'invert': False }

        self.window = window
        self.invert = window['invert']

        self.cw = window['w']
        self.ch = window['h']

    def show(self, c):
        for y in range(self.ch):
            for x in range(self.cw):
                xo = self.cw - x if self.invert else x
                yo = self.ch - y if self.invert else y

                color = c.get(self.window['x'] + xo, self.window['y'] + yo)
                self._offscreen.SetPixel(x, y, color.r, color.g, color.b)

        self._offscreen = self._matrix.SwapOnVSync(self._offscreen)

