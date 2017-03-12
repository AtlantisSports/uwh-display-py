from .canvas_viewer import CanvasViewer
from .canvas import Canvas

def test__CanvasViewer():
    class CVT(CanvasViewer):
        def show(self, c):
            super(CVT, self).show(c)
            self.pixels = c.h * c.w

    t = CVT()
    c = Canvas(10, 20)
    t.show(c)
    assert t.pixels == 10 * 20

