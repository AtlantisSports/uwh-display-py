from .font import Font
from .canvas import Canvas, Color

black_color = Color(  0,   0, 255)
white_color = Color(255, 255, 255)
GREEN  = Color(  0, 255,   0)
ORANGE = Color(255, 128,   0)
RED    = Color(255,   0,   0)

class GameDisplay(object):
    def __init__(self):
        self.canvas = Canvas(32 * 3, 32)
        self.font_s = Font.get_5x7()
        self.font_m = Font.get_11x20()
        self.font_l = Font.get_15x29()

    def render(self, mgr):
        self.render_base(mgr)

    def render_base(self, mgr):
        if mgr.whiteScore() < 10 and mgr.blackScore() < 10:
            self.render_wide(mgr)
        elif mgr.whiteScore() < 10 or mgr.blackScore() < 10:
            self.render_medium(mgr)
        else:
            self.render_narrow(mgr)

    def render_narrow(self, mgr):
        self.font_l.print(self.canvas,  0, 1, black_color,
                          "%2d" % (mgr.blackScore(),))
        self.font_l.print(self.canvas, 65, 1, white_color,
                          "%2d" % (mgr.whiteScore(),))

        if mgr.gameStateFirstHalf():
            time_color = GREEN
            show_time = True
        elif mgr.gameStateSecondHalf():
            time_color = GREEN
            show_time = True
        elif mgr.gameStateHalfTime():
            time_color = ORANGE
            show_time = True
        elif mgr.gameStateGameOver():
            time_color = RED
            show_time = False
            self.font_s.print(self.canvas, 38, 6, time_color,
                              "game")

            self.font_s.print(self.canvas, 38, 20, time_color,
                              "over")

        if show_time:
            self.font_m.print(self.canvas, 38, 2, time_color,
                              "%d" % (mgr.gameClock() // 60,))

            self.font_s.print(self.canvas, 38, 23, time_color,
                              ":%d" % (mgr.gameClock() % 60,))

    def render_medium(self, mgr):
        self.font_l.print(self.canvas, 65, 1, white_color,
                          "%2d" % (mgr.whiteScore(),))
        offset = 0 if mgr.blackScore() < 10 else 16
        if mgr.gameStateFirstHalf():
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "1st half")
        elif mgr.gameStateSecondHalf():
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "2nd half")
        elif mgr.gameStateHalfTime():
            time_color = ORANGE
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "1/2 time")
        elif mgr.gameStateGameOver():
            time_color = RED
            show_time = False
            self.font_s.print(self.canvas, offset + 28, 6, time_color,
                              "game")

            self.font_s.print(self.canvas, offset + 28, 20, time_color,
                              "over")

        if show_time:
            self.font_m.print(self.canvas, offset + 14, 10, time_color,
                              "%d" % (mgr.gameClock() // 60))

            self.font_m.print(self.canvas, offset + 41, 10, time_color,
                              "%02d" % (mgr.gameClock() % 60))
            self.draw_colon(offset + 38, 16, time_color)
            self.draw_colon(offset + 38, 24, time_color)

        self.font_l.print(self.canvas,  0, 1, black_color,
                          "%d" % (mgr.blackScore(),))


    def render_wide(self, mgr):
        self.font_l.print(self.canvas,  1, 1, black_color,
                          "%1d" % (mgr.blackScore(),))
        self.font_l.print(self.canvas, 81, 1, white_color,
                          "%1d" % (mgr.whiteScore(),))

        if mgr.gameStateFirstHalf():
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "1st  half")
        elif mgr.gameStateSecondHalf():
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "2nd  half")
        elif mgr.gameStateHalfTime():
            time_color = ORANGE
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "half time")
        elif mgr.gameStateGameOver():
            time_color = RED
            show_time = False
            self.font_s.print(self.canvas, 38, 6, time_color,
                              "game")

            self.font_s.print(self.canvas, 38, 20, time_color,
                              "over")

        if show_time:
            self.font_m.print(self.canvas, 22, 10, time_color,
                              "%d" % (mgr.gameClock() // 60))

            self.font_m.print(self.canvas, 53, 10, time_color,
                              "%02d" % (mgr.gameClock() % 60))

            self.draw_colon(48, 16, time_color)
            self.draw_colon(48, 24, time_color)


    def draw_colon(self, x, y, c):
        self.canvas.set(x,   y,   c)
        self.canvas.set(x,   y+1, c)
        self.canvas.set(x+1, y,   c)
        self.canvas.set(x+1, y+1, c)

    def draw_skinnycolon(self, x, y, c):
        self.canvas.set(x,   y, c)
        self.canvas.set(x+1, y, c)
