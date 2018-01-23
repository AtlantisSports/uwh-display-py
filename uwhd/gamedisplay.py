from .font import Font
from .canvas import Canvas, Color

black_color = Color(  0,   0, 255)
white_color = Color(255, 255, 255)
time_color  = Color(255, 255,   0)

class GameDisplay(object):
    def __init__(self):
        self.canvas = Canvas(32 * 3, 32)
        self.font_s = Font.get_5x7()
        self.font_m = Font.get_11x20()
        self.font_l = Font.get_15x29()

    def render(self, mgr):
        self.render_base(mgr)

    def render_base(self, mgr):
        self.font_l.print(self.canvas,  1, 1, black_color,
                          "%02d" % (mgr.blackScore(),))
        self.font_l.print(self.canvas, 64, 1, white_color,
                          "%02d" % (mgr.whiteScore(),))

        game_clock = mgr.gameClock()
        self.font_m.print(self.canvas, 38, 2, time_color,
                          "%2d" % (game_clock // 60,))

        self.font_s.print(self.canvas, 38, 23, time_color,
                          ":%02d" % (game_clock % 60,))
