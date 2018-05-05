from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from .canvas_viewer import CanvasViewer

class MatrixCanvasViewer(CanvasViewer):
    def __init__(self):
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

    def show(self, c):
        for y in range(c.h):
            for x in range(c.w):
                color = c.get(x, y)
                self._offscreen.SetPixel(x, y, color.r, color.g, color.b)

        self._offscreen = self._matrix.SwapOnVSync(self._offscreen)
