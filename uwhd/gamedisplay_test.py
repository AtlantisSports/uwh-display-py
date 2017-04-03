from .gamemanager import GameManager
from .gamedisplay import GameDisplay

def test__GameDisplay():
    mgr = GameManager()
    mgr.setBlackScore(13)
    mgr.setWhiteScore(10)
    mgr.setGameClock(11 * 60 + 42)

    gd = GameDisplay()
    gd.render(mgr)
    # Don't bother checking yet
