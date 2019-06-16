from .font import Font
from .canvas import Canvas, Color
from uwh.gamemanager import PoolLayout, TimeoutState, GameState, TeamColor

import math

BLUE = Color( 64, 128, 255)
WHITE = Color(255, 255, 255)
GREEN  = Color(  0, 255,   0)
ORANGE = Color(255, 128,   0)
RED    = Color( 96,   0,   0)
YELLOW = Color(255, 255,   0)
GRAY = Color(128, 128, 128)

class GameDisplay2(object):
    def __init__(self):
        self.canvas = Canvas(64 * 4, 64)
        self.font_xs = Font.get_5x7()
        self.font_s = Font.get_10x14()
        self.font_m = Font.get_11x20()
        self.font_l = Font.get_15x29()
        self.font_xl = Font.get_22x40()
        self.font_xxl = Font.get_30x58()

        self.score_str = None
        self.time_str = None

    def left_score(self, mgr):
        if mgr.layout() == PoolLayout.white_on_right:
            return mgr.blackScore()
        else:
            return mgr.whiteScore()

    def left_color(self, mgr):
        if mgr.layout() == PoolLayout.white_on_right:
            return BLUE
        else:
            return WHITE

    def right_score(self, mgr):
        if mgr.layout() == PoolLayout.white_on_right:
            return mgr.whiteScore()
        else:
            return mgr.blackScore()

    def right_color(self, mgr):
        if mgr.layout() == PoolLayout.white_on_right:
            return WHITE
        else:
            return BLUE

    def left_team(self, mgr):
        if mgr.layout() == PoolLayout.white_on_right:
            return TeamColor.black
        else:
            return TeamColor.white

    def right_team(self, mgr):
        if mgr.layout() == PoolLayout.white_on_right:
            return TeamColor.white
        else:
            return TeamColor.black

    def render_score(self, mgr):
        lscore = self.left_score(mgr)
        lpenalties = mgr.penalties(self.left_team(mgr))
        if len(lpenalties):
            loffs = 8 if 10 <= lscore else 20
            self.font_xl.print(self.canvas,    2 + loffs, 3, self.left_color(mgr),
                               "%d" % (lscore,))

            lpenalties = lpenalties[:3]
            count = len(lpenalties)
            for i, penalty in enumerate(lpenalties):
                offset = int((count - i) * 64 / (count + 1))
                self.render_penalty(penalty, offset, 51)
        else:
            loffs = 0 if 10 <= lscore else 16
            self.font_xxl.print(self.canvas,   2 + loffs, 3, self.left_color(mgr),
                                "%d" % (lscore,))

        rscore = self.right_score(mgr)
        rpenalties = mgr.penalties(self.right_team(mgr))
        if len(rpenalties):
            roffs = 8 if 10 <= rscore else 20
            self.font_xl.print(self.canvas,  194 + roffs, 3, self.right_color(mgr),
                               "%d" % (rscore,))

            rpenalties = rpenalties[:3]
            count = len(rpenalties)
            for i, penalty in enumerate(rpenalties):
                offset = int((count - i) * 64 / (count + 1))
                self.render_penalty(penalty, 192 + offset, 51)
        else:
            roffs = 0 if 10 <= rscore else 16
            self.font_xxl.print(self.canvas, 194 + roffs, 3, self.right_color(mgr),
                                "%d" % (rscore,))

    def render_penalty(self, p, x, y):
        if p.dismissed():
            thick = 3
            size = 7
            for yo in range(-size, size):
                for xo in range(-size, size):
                    if abs(xo + yo) < thick or abs(yo - xo) < thick:
                        self.canvas.set(x + xo, y + yo + 4, RED)
        else:
            width = {
                60: 1,
                180: 3,
                300: 8
            }[p.duration()]
            self.draw_pie(x, y + 3, 8, 0.75, RED, width)

        color = WHITE if p.team() == TeamColor.white else BLUE
        cap = str(p.player())
        self.font_xs.print(self.canvas, x - 5 + 3 * (2 - len(cap)), y, color, cap, alpha=True)

    def render(self, mgr):
        self.render_score(mgr)

        game_clock = mgr.gameClockAtPause()
        timeout_clock = mgr.gameClock()

        period_color, period_text = {
            GameState.first_half:       (GREEN,  "FIRST\nHALF"),
            GameState.second_half:      (GREEN,  "SECOND\nHALF"),
            GameState.half_time:        (ORANGE, "HALF\nTIME"),
            GameState.pre_game:         (YELLOW, "NEXT\nGAME"),
            GameState.game_over:        (YELLOW, "NEXT\nGAME"),
            GameState.pre_ot:           (ORANGE, "PRE\nOVTM"),
            GameState.ot_first:         (GREEN,  "FIRST\nOVTM"),
            GameState.ot_half:          (GREEN,  "OVTM\nHALF"),
            GameState.ot_second:        (GREEN,  "2ND\nOVTM"),
            GameState.pre_sudden_death: (ORANGE, "PRE SDN\nDEATH"),
            GameState.sudden_death:     (GREEN,  "SUDN\nDEATH"),
        }[mgr.gameState()]

        if (mgr.timeoutState() == TimeoutState.penalty_shot or
            mgr.timeoutState() == TimeoutState.ref or
            mgr.timeoutState() == TimeoutState.white or
            mgr.timeoutState() == TimeoutState.black):

            state_color, state_text = {
                TimeoutState.ref:           (YELLOW, "REF\nT/O"),
                TimeoutState.penalty_shot:  (RED,    "PNLTY\nSHOT"),
                TimeoutState.white:         (WHITE,  "WHITE\nT/O"),
                TimeoutState.black:         (BLUE,   "BLACK\nT/O"),
                TimeoutState.none:          (None, None)
            }[mgr.timeoutState()]

            if mgr.gameState() == GameState.game_over:
                game_clock += 3 * 60

            if period_color == GREEN:
                period_color = YELLOW

            self.font_s.print(self.canvas,  65, 1, state_color, state_text)
            self.font_s.print(self.canvas,  65, 64 - 30, period_color, period_text)

            self.font_l.print(self.canvas,  93 + 32, 1, state_color,
                              "{:>2}".format(timeout_clock // 60))

            self.font_l.print(self.canvas, 128 + 32, 1, state_color,
                              "{:0>2}".format(timeout_clock % 60))

            self.draw_colon(125 + 32,  8 + 5, state_color)
            self.draw_colon(125 + 32, 20 + 5, state_color)

            # Game Clock
            self.font_l.print(self.canvas,  93 + 32, 28 + 5, period_color,
                              "{:>2}".format(game_clock // 60))

            self.font_l.print(self.canvas, 128 + 32, 28 + 5, period_color,
                              "{:0>2}".format(game_clock % 60))

            self.draw_colon(125 + 32, 36 + 5, period_color)
            self.draw_colon(125 + 32, 48 + 5, period_color)
        else:
            self.font_s.print(self.canvas, 65 + 1, 1, period_color,
                              period_text.replace('\n', ' '))

            # Game Clock
            self.font_xl.print(self.canvas,  128 - 22 - 22 - 4, 20, period_color,
                               "{:>2}".format(game_clock // 60))

            self.font_xl.print(self.canvas, 128 + 4, 20, period_color,
                               "{:0>2}".format(game_clock % 60))

            self.draw_colon(127, 36, period_color)
            self.draw_colon(127, 48, period_color)


    def draw_colon(self, x, y, c):
        self.canvas.set(x,   y,   c)
        self.canvas.set(x,   y+1, c)
        self.canvas.set(x+1, y,   c)
        self.canvas.set(x+1, y+1, c)

    def draw_skinnycolon(self, x, y, c):
        self.canvas.set(x,   y, c)
        self.canvas.set(x+1, y, c)

    def draw_pie(self, x, y, r, p, c, rad):
        def inarc(xo, yo, p):
            return math.atan2(xo, yo) + math.pi <= 2 * math.pi * p

        def incirc(xo, yo, r):
            return xo * xo + yo * yo <= r * r

        for yo in range(-r, r, 1):
            for xo in range(-r, r, 1):
                if (incirc(xo, yo, r) and (not incirc(xo, yo, r - rad)) and inarc(xo, yo, p)):
                    self.canvas.set(x + xo, y + yo, c)
