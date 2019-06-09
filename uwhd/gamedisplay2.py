from .font import Font
from .canvas import Canvas, Color
from uwh.gamemanager import PoolLayout, TimeoutState, GameState

black_color = Color( 64, 128, 255)
white_color = Color(255, 255, 255)
GREEN  = Color(  0, 255,   0)
ORANGE = Color(255, 128,   0)
RED    = Color(255,   0,   0)
YELLOW = Color(255, 255,   0)

class GameDisplay2(object):
    def __init__(self):
        self.canvas = Canvas(64 * 4, 64)
        self.font_s = Font.get_5x7()
        self.font_m = Font.get_11x20()
        self.font_l = Font.get_15x29()
        self.font_xl = Font.get_30x58()

        self.score_str = None
        self.time_str = None

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

    def render(self, mgr):
        lscore = self.left_score(mgr)
        loffs = 0 if 10 <= lscore else 16
        self.font_xl.print(self.canvas,   2 + loffs, 3, self.left_color(mgr),
                           "%d" % (lscore,))
        rscore = self.right_score(mgr)
        roffs = 0 if 10 <= rscore else 16
        self.font_xl.print(self.canvas, 194 + roffs, 3, self.right_color(mgr),
                           "%d" % (rscore,))

        game_clock = mgr.gameClockAtPause()

        if mgr.timeoutState() == TimeoutState.ref:
            state_color = YELLOW
            state_text = " REF T/O "
        elif mgr.timeoutState() == TimeoutState.penalty_shot:
            state_color = RED
            state_text = "PNLTY SHT"
        elif mgr.timeoutState() == TimeoutState.white:
            state_color = YELLOW
            state_text = "WHITE T/O"
        elif mgr.timeoutState() == TimeoutState.black:
            state_color = YELLOW
            state_text = "BLACK T/O"
        elif mgr.gameState() == GameState.first_half:
            state_color = GREEN
            state_text = "1st  half"
        elif mgr.gameState() == GameState.second_half:
            state_color = GREEN
            state_text = "2nd  half"
        elif mgr.gameState() == GameState.half_time:
            state_color = ORANGE
            state_text = "1/2  time"
        elif mgr.gameState() == GameState.pre_game:
            state_color = YELLOW
            state_text = "next game"
        elif mgr.gameState() == GameState.game_over:
            state_color = YELLOW
            state_text = "next game"
            game_clock += 3 * 60
        elif mgr.gameState() == GameState.pre_ot:
            state_color = ORANGE
            state_text = "PRE - O/T"
        elif mgr.gameState() == GameState.ot_first:
            state_color = GREEN
            state_text = "1st OVRTM"
        elif mgr.gameState() == GameState.ot_half:
            state_color = ORANGE
            state_text = "1/2 - O/T"
        elif mgr.gameState() == GameState.ot_second:
            state_color = GREEN
            state_text = "2nd OVRTM"
        elif mgr.gameState() == GameState.pre_sudden_death:
            state_color = ORANGE
            state_text = "PRE - S/D"
        elif mgr.gameState() == GameState.sudden_death:
            state_color = GREEN
            state_text = "sdn death"

        self.font_s.print(self.canvas, 100, 12, state_color,
                          state_text)

        # Game Clock
        self.font_l.print(self.canvas,  93, 28, YELLOW,
                          "{:>2}".format(game_clock // 60))

        self.font_l.print(self.canvas, 128, 28, YELLOW,
                          "{:0>2}".format(game_clock % 60))

        self.draw_colon(125, 36, state_color)
        self.draw_colon(125, 48, state_color)


    def draw_colon(self, x, y, c):
        self.canvas.set(x,   y,   c)
        self.canvas.set(x,   y+1, c)
        self.canvas.set(x+1, y,   c)
        self.canvas.set(x+1, y+1, c)

    def draw_skinnycolon(self, x, y, c):
        self.canvas.set(x,   y, c)
        self.canvas.set(x+1, y, c)
