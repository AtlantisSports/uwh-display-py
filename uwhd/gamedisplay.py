from .font import Font
from .canvas import Canvas, Color
from .cmas import cmas
from uwh.gamemanager import PoolLayout, TimeoutState, GameState

black_color = Color(  0,   0, 255)
white_color = Color(255, 255, 255)
GREEN  = Color(  0, 255,   0)
ORANGE = Color(255, 128,   0)
RED    = Color(255,   0,   0)
YELLOW = Color(255, 255,   0)

class GameDisplay(object):
    def __init__(self):
        self.canvas = Canvas(32 * 3, 32)
        self.font_s = Font.get_5x7()
        self.font_m = Font.get_11x20()
        self.font_l = Font.get_15x29()

    def render(self, mgr):
        self.render_base(mgr)

    def render_base(self, mgr):
        self.canvas.clear()
        if mgr.whiteScore() < 10 and mgr.blackScore() < 10:
            self.render_wide(mgr)
        elif mgr.whiteScore() < 10 or mgr.blackScore() < 10:
            self.render_medium(mgr)
        else:
            self.render_narrow(mgr)

    def left_score(self, mgr):
        if mgr.layout() == PoolLayout.white_on_right:
            return mgr.blackScore()
        else:
            return mgr.whiteScore()

    def left_color(self, mgr):
        if mgr.layout() == PoolLayout.white_on_right:
            return black_color
        else:
            return white_color

    def right_score(self, mgr):
        if mgr.layout() == PoolLayout.white_on_right:
            return mgr.whiteScore()
        else:
            return mgr.blackScore()

    def right_color(self, mgr):
        if mgr.layout() == PoolLayout.white_on_right:
            return white_color
        else:
            return black_color

    def render_narrow(self, mgr):
        self.font_l.print(self.canvas,  0, 1, self.left_color(mgr),
                          "%2d" % (self.left_score(mgr),))
        self.font_l.print(self.canvas, 65, 1, self.right_color(mgr),
                          "%2d" % (self.right_score(mgr),))

        if mgr.timeoutState() == TimeoutState.ref:
            time_color = YELLOW
            show_time = True
        elif mgr.timeoutState() == TimeoutState.penalty_shot:
            time_color = RED
            show_time = True
        elif mgr.timeoutState() == TimeoutState.white:
            time_color = white_color
            show_time = True
        elif mgr.timeoutState() == TimeoutState.black:
            time_color = black_color
            show_time = True
        elif mgr.gameState() == GameState.first_half:
            time_color = GREEN
            show_time = True
        elif mgr.gameState() == GameState.second_half:
            time_color = GREEN
            show_time = True
        elif mgr.gameState() == GameState.half_time:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, 38, 6, time_color,
                              "half")
            self.font_s.print(self.canvas, 38, 20, time_color,
                              "time")
        elif mgr.gameState() == GameState.pre_game:
            self.render_cmas()
            show_time = False
        elif mgr.gameState() == GameState.game_over:
            time_color = RED
            show_time = False
            self.font_s.print(self.canvas, 38, 6, time_color,
                              "game")
            self.font_s.print(self.canvas, 38, 20, time_color,
                              "over")
        elif mgr.gameState() == GameState.pre_ot:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, 38, 6, time_color,
                              "over")
            self.font_s.print(self.canvas, 38, 20, time_color,
                              "time")
        elif mgr.gameState() == GameState.ot_first:
            time_color = GREEN
            show_time = True
        elif mgr.gameState() == GameState.ot_half:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, 38, 0, time_color,
                              "OVER")
            self.font_s.print(self.canvas, 38, 8, time_color,
                              "TIME")
            self.font_s.print(self.canvas, 38, 17, time_color,
                              "HALF")
            self.font_s.print(self.canvas, 38, 25, time_color,
                              "TIME")
        elif mgr.gameState() == GameState.ot_second:
            time_color = GREEN
            show_time = True
        elif mgr.gameState() == GameState.pre_sudden_death:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, 34, 6, time_color,
                              "suddn")
            self.font_s.print(self.canvas, 34, 20, time_color,
                              "death")
        elif mgr.gameState() == GameState.sudden_death:
            time_color = GREEN
            show_time = False
            self.font_s.print(self.canvas, 34, 6, time_color,
                              "suddn")
            self.font_s.print(self.canvas, 34, 20, time_color,
                              "death")

        if show_time:
            self.font_m.print(self.canvas, 38, 2, time_color,
                              "%d" % (mgr.gameClock() // 60,))

            self.font_s.print(self.canvas, 38, 23, time_color,
                              ":%02d" % (mgr.gameClock() % 60,))

    def render_medium(self, mgr):
        self.font_l.print(self.canvas, 65, 1, self.right_color(mgr),
                          "%2d" % (self.right_score(mgr),))
        offset = 0 if mgr.blackScore() < 10 else 16
        if mgr.timeoutState() == TimeoutState.ref:
            time_color = YELLOW
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "REF  T/O")
        elif mgr.timeoutState() == TimeoutState.penalty_shot:
            time_color = RED
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "PNLT SHT")
        elif mgr.timeoutState() == TimeoutState.white:
            time_color = YELLOW
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, white_color,
                              "WHT  T/O")
        elif mgr.timeoutState() == TimeoutState.black:
            time_color = YELLOW
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, black_color,
                              "BLK  T/O")
        elif mgr.gameState() == GameState.first_half:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "1st half")
        elif mgr.gameState() == GameState.second_half:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "2nd half")
        elif mgr.gameState() == GameState.half_time:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, offset + 28, 6, time_color,
                              "half")
            self.font_s.print(self.canvas, offset + 28, 20, time_color,
                              "time")
        elif mgr.gameState() == GameState.pre_game:
            self.render_cmas()
            show_time = False
        elif mgr.gameState() == GameState.game_over:
            time_color = RED
            show_time = False
            self.font_s.print(self.canvas, offset + 28, 6, time_color,
                              "game")
            self.font_s.print(self.canvas, offset + 28, 20, time_color,
                              "over")
        elif mgr.gameState() == GameState.pre_ot:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, offset + 28, 6, time_color,
                              "OVER")
            self.font_s.print(self.canvas, offset + 28, 20, time_color,
                              "TIME")
        elif mgr.gameState() == GameState.ot_first:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, ORANGE,
                              "1st OVTM")
        elif mgr.gameState() == GameState.ot_half:
            time_color = ORANGE
            show_time = False

            self.font_s.print(self.canvas, offset + 18, 6, time_color,
                              "OVERTIME")
            self.font_s.print(self.canvas, offset + 18, 17, time_color,
                              "HALFTIME")
        elif mgr.gameState() == GameState.ot_second:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, ORANGE,
                              "2nd OVTM")
        elif mgr.gameState() == GameState.pre_sudden_death:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, offset + 28, 6, time_color,
                              "SUDDEN")
            self.font_s.print(self.canvas, offset + 28, 20, time_color,
                              "DEATH")
        elif mgr.gameState() == GameState.sudden_death:
            time_color = GREEN
            show_time = False
            self.font_s.print(self.canvas, offset + 28, 6, time_color,
                              "SUDDEN")
            self.font_s.print(self.canvas, offset + 28, 20, time_color,
                              "DEATH")

        if show_time:
            self.font_m.print(self.canvas, offset + 15, 10, time_color,
                              "{:>2}".format(mgr.gameClock() // 60))

            self.font_m.print(self.canvas, offset + 42, 10, time_color,
                              "{:0>2}".format(mgr.gameClock() % 60))
            self.draw_colon(offset + 39, 16, time_color)
            self.draw_colon(offset + 39, 24, time_color)

        self.font_l.print(self.canvas,  0, 1, self.left_color(mgr),
                          "%d" % (self.left_score(mgr),))


    def render_wide(self, mgr):
        self.font_l.print(self.canvas,  1, 1, self.left_color(mgr),
                          "%1d" % (self.left_score(mgr),))
        self.font_l.print(self.canvas, 81, 1, self.right_color(mgr),
                          "%1d" % (self.right_score(mgr),))

        if mgr.timeoutState() == TimeoutState.ref:
            time_color = YELLOW
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              " REF T/O ")
        elif mgr.timeoutState() == TimeoutState.penalty_shot:
            time_color = RED
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "PNLTY SHT")
        elif mgr.timeoutState() == TimeoutState.white:
            time_color = YELLOW
            show_time = True
            self.font_s.print(self.canvas, 22, 2, white_color,
                              "WHITE T/O")
        elif mgr.timeoutState() == TimeoutState.black:
            time_color = YELLOW
            show_time = True
            self.font_s.print(self.canvas, 22, 2, black_color,
                              "BLACK T/O")
        elif mgr.gameState() == GameState.first_half:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "1st  half")
        elif mgr.gameState() == GameState.second_half:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "2nd  half")
        elif mgr.gameState() == GameState.half_time:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, 38, 6, time_color,
                              "half")
            self.font_s.print(self.canvas, 38, 20, time_color,
                              "time")
        elif mgr.gameState() == GameState.pre_game:
            self.render_cmas()
            show_time = False
        elif mgr.gameState() == GameState.game_over:
            time_color = RED
            show_time = False
            self.font_s.print(self.canvas, 38, 6, time_color,
                              "game")
            self.font_s.print(self.canvas, 38, 20, time_color,
                              "over")
        elif mgr.gameState() == GameState.pre_ot:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, 38, 6, time_color,
                              "OVER")
            self.font_s.print(self.canvas, 38, 20, time_color,
                              "TIME")
        elif mgr.gameState() == GameState.ot_first:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, 22, 2, ORANGE,
                              "1st OVRTM")
        elif mgr.gameState() == GameState.ot_half:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, 26, 6, time_color,
                              "OVERTIME")
            self.font_s.print(self.canvas, 26, 17, time_color,
                              "HALFTIME")
        elif mgr.gameState() == GameState.ot_second:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, 22, 2, ORANGE,
                              "2nd OVRTM")
        elif mgr.gameState() == GameState.pre_sudden_death:
            time_color = ORANGE
            show_time = False
            self.font_s.print(self.canvas, 32, 6, time_color,
                              "SUDDEN")
            self.font_s.print(self.canvas, 32, 20, time_color,
                              "DEATH")
        elif mgr.gameState() == GameState.sudden_death:
            time_color = GREEN
            show_time = False
            self.font_s.print(self.canvas, 32, 6, time_color,
                              "SUDDEN")
            self.font_s.print(self.canvas, 32, 20, time_color,
                              "DEATH")

        if show_time:
            self.font_m.print(self.canvas, 22, 10, time_color,
                              "{:>2}".format(mgr.gameClock() // 60))

            self.font_m.print(self.canvas, 53, 10, time_color,
                              "{:0>2}".format(mgr.gameClock() % 60))

            self.draw_colon(48, 16, time_color)
            self.draw_colon(48, 24, time_color)

    def render_cmas(self):
        import random, time
        for y in range(0, 32):
            for x in range(0, 32):
                c = cmas(x, y) * min(1, 0.5 + random.random())
                self.canvas.set(x + 16, y, Color(c, c, c/2))

        c = 255 * 0.75
        suffix = "\x01\x02\x03" if int(time.time()) % 4 >= 2 else "\x04\x05"
        self.font_s.print(self.canvas, 50, 8, Color(c, c, c/2),
                          "20" + suffix)

        self.font_s.print(self.canvas, 50, 18, Color(c, c, c/2),
                          "CMAS")

    def draw_colon(self, x, y, c):
        self.canvas.set(x,   y,   c)
        self.canvas.set(x,   y+1, c)
        self.canvas.set(x+1, y,   c)
        self.canvas.set(x+1, y+1, c)

    def draw_skinnycolon(self, x, y, c):
        self.canvas.set(x,   y, c)
        self.canvas.set(x+1, y, c)
