from rgbmatrix import RGBMatrix, RGBMatrixOptions
from .canvas_viewer import CanvasViewer

class MatrixCanvasViewer(CanvasViewer):
    def __init__(self, window=None):
        if window is None:
            window = { 'w': 32 * 3, 'h': 32, 'x': 0, 'y': 0, 'invert': False }

        self.window = window
        self.invert = window['invert']

        self.cw = window['w']
        self.ch = window['h']

        options = RGBMatrixOptions()
        options.rows = self.ch # awkward because we don't know what size panels
        options.chain_length = self.cw / self.ch
        options.parallel = 1
        options.hardware_mapping = 'regular'

        self._matrix = RGBMatrix(options=options)
        self._offscreen = self._matrix.CreateFrameCanvas()


    def show(self, c):
        for y in range(self.ch):
            for x in range(self.cw):
                xo = self.cw - x if self.invert else x
                yo = self.ch - y if self.invert else y

                color = c.get(self.window['x'] + xo, self.window['y'] + yo)
                self._offscreen.SetPixel(x, y, color.r, color.g, color.b)

        self._offscreen = self._matrix.SwapOnVSync(self._offscreen)

