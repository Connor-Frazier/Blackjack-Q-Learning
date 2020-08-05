
import random
from enum import Enum
"""Utility file containing classes and methods used by both the environment and the players"""

class Actions(Enum):
    HIT = 1
    STAND = 2
    DOUBLE = 3
    SPLIT = 4
    NONE = 5

class Result(Enum):
    WIN = "WIN"
    PUSH = "PUSH"
    LOSS = "LOSS"

class Phase(Enum):
    NONE = 0
    LEARNING = 1
    TESTING = 2

class BettingActions(Enum):
    DOUBLEBET = 0
    MINBET = 1
    MAXBET = 2
    BETMORE = 3
    BETLESS = 4


def getAvailableActions(cards):
    if cards == None:
        return []
    actions = [Actions.HIT, Actions.STAND, Actions.DOUBLE]
    if len(cards) == 2 and cards[0] == cards[1]:
        actions.append(Actions.SPLIT)
    return actions

def getBetActions(currentBet):
    actions = [BettingActions.MINBET, BettingActions.MAXBET]
    if currentBet * 2 <= 1000:
        actions.append(BettingActions.DOUBLEBET)
    elif currentBet + 15 <= 1000:
        actions.append(BettingActions.BETMORE)
    elif currentBet - 15 >= 15:
        actions.append(BettingActions.BETLESS)
    return actions

#taken from pacman reinforcement programming assignment util file
def flipCoin(p):
    r = random.random()
    return r < p

#taken from pacman reinforcement programming assignment util file
class Counter(dict):
    """
    A counter keeps track of counts for a set of keys.

    The counter class is an extension of the standard python
    dictionary type.  It is specialized to have number values
    (integers or floats), and includes a handful of additional
    functions to ease the task of counting data.  In particular,
    all keys are defaulted to have value 0.
    """
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

