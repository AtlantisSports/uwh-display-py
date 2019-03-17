from .font import Font
from .canvas import Canvas, Color
from uwh.gamemanager import PoolLayout, TimeoutState, GameState

from Adafruit_LED_Backpack import SevenSegment, AlphaNum4

black_color = Color( 64, 128, 255)
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

        self.score_str = None
        self.time_str = None

        try:
            self.score_backpack = AlphaNum4.AlphaNum4(address=0x70)
            self.score_backpack.begin()

            self.time_backpack = SevenSegment.SevenSegment(address=0x71)
            self.time_backpack.begin()
        except FileNotFoundError:
            self.score_backpack = None
            self.time_backpack = None

    def render(self, mgr):
        self.render_base(mgr)
        self.render_backpack(mgr)

    def render_backpack(self, mgr):
        if self.time_backpack is None:
            return

        time_str = "%2d%02d" % (
                   mgr.gameClockAtPause() // 60,
                   mgr.gameClockAtPause() % 60)

        if time_str != self.time_str:
            self.time_str = time_str
            self.time_backpack.print_number_str(self.time_str)
            self.time_backpack.set_colon(True)
            self.time_backpack.write_display()

        if self.score_backpack is None:
            return

        score_str = "%2d%2d" % (mgr.whiteScore(), mgr.blackScore())

        if score_str != self.score_str:
            self.score_str = score_str
            self.score_backpack.print_str(self.score_str)
            self.score_backpack.write_display()

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

        game_clock = mgr.gameClock()

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
            show_time = True
        elif mgr.gameState() == GameState.pre_game:
            time_color = YELLOW
            show_time = True
        elif mgr.gameState() == GameState.game_over:
            time_color = RED
            show_time = True
            game_clock += 3 * 60
        elif mgr.gameState() == GameState.pre_ot:
            time_color = ORANGE
            show_time = True
        elif mgr.gameState() == GameState.ot_first:
            time_color = GREEN
            show_time = True
        elif mgr.gameState() == GameState.ot_half:
            time_color = ORANGE
            show_time = True
        elif mgr.gameState() == GameState.ot_second:
            time_color = GREEN
            show_time = True
        elif mgr.gameState() == GameState.pre_sudden_death:
            time_color = ORANGE
            show_time = True
        elif mgr.gameState() == GameState.sudden_death:
            time_color = GREEN
            show_time = True

        if show_time:
            self.font_m.print(self.canvas, 38, 2, time_color,
                              "%d" % (game_clock // 60,))

            self.font_s.print(self.canvas, 38, 23, time_color,
                              ":%02d" % (game_clock % 60,))

    def render_medium(self, mgr):
        self.font_l.print(self.canvas, 65, 1, self.right_color(mgr),
                          "%2d" % (self.right_score(mgr),))

        game_clock = mgr.gameClock()

        offset = 0 if self.left_score(mgr) < 10 else 16
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
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "1/2 time")
        elif mgr.gameState() == GameState.pre_game:
            time_color = YELLOW
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "nxt game")
        elif mgr.gameState() == GameState.game_over:
            time_color = YELLOW
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "nxt game")
            game_clock += 3 * 60
        elif mgr.gameState() == GameState.pre_ot:
            time_color = ORANGE
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "PRE O/T")
        elif mgr.gameState() == GameState.ot_first:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, ORANGE,
                              "1st OVTM")
        elif mgr.gameState() == GameState.ot_half:
            time_color = ORANGE
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "H/T O/T")
        elif mgr.gameState() == GameState.ot_second:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, ORANGE,
                              "2nd OVTM")
        elif mgr.gameState() == GameState.pre_sudden_death:
            time_color = ORANGE
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "PRE S/D")
        elif mgr.gameState() == GameState.sudden_death:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, offset + 16, 2, time_color,
                              "SDN DTH")

        if show_time:
            self.font_m.print(self.canvas, offset + 15, 10, time_color,
                              "{:>2}".format(game_clock // 60))

            self.font_m.print(self.canvas, offset + 42, 10, time_color,
                              "{:0>2}".format(game_clock % 60))
            self.draw_colon(offset + 39, 16, time_color)
            self.draw_colon(offset + 39, 24, time_color)

        self.font_l.print(self.canvas,  0, 1, self.left_color(mgr),
                          "%d" % (self.left_score(mgr),))


    def render_wide(self, mgr):
        self.font_l.print(self.canvas,  1, 1, self.left_color(mgr),
                          "%1d" % (self.left_score(mgr),))
        self.font_l.print(self.canvas, 81, 1, self.right_color(mgr),
                          "%1d" % (self.right_score(mgr),))

        game_clock = mgr.gameClock()

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
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "1/2  time")
        elif mgr.gameState() == GameState.pre_game:
            time_color = YELLOW
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "next game")
        elif mgr.gameState() == GameState.game_over:
            time_color = YELLOW
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "next game")
            game_clock += 3 * 60
        elif mgr.gameState() == GameState.pre_ot:
            time_color = ORANGE
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "PRE - O/T")
        elif mgr.gameState() == GameState.ot_first:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, 22, 2, ORANGE,
                              "1st OVRTM")
        elif mgr.gameState() == GameState.ot_half:
            time_color = ORANGE
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "1/2 - O/T")
        elif mgr.gameState() == GameState.ot_second:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, 22, 2, ORANGE,
                              "2nd OVRTM")
        elif mgr.gameState() == GameState.pre_sudden_death:
            time_color = ORANGE
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "PRE - S/D")
        elif mgr.gameState() == GameState.sudden_death:
            time_color = GREEN
            show_time = True
            self.font_s.print(self.canvas, 22, 2, time_color,
                              "sdn death")

        if show_time:
            self.font_m.print(self.canvas, 22, 10, time_color,
                              "{:>2}".format(game_clock // 60))

            self.font_m.print(self.canvas, 53, 10, time_color,
                              "{:0>2}".format(game_clock % 60))

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
