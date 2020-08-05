from util import *
import random
import sys
import math

"""File holds all of the player objects used by the blackjack environment"""


class Dealer:
    """The Dealer object"""

    def __init__(self):
        self.hand = []

    def recieveCards(self, cards):
        for card in cards:
            self.hand.append(card)

    def getSum(self):
        cardsSum = sum(self.hand)
        for card in self.hand:
            if card == 1 and (cardsSum + 10) <= 21:
                cardsSum += 10

        return cardsSum

    def getAction(self):
        if self.getSum() < 17 or (1 in self.hand and self.getSum() == 17):  # dealer will hit on soft 17
            return Actions.HIT
        else:
            return Actions.STAND

    def newRound(self):
        self.hand = []


class Player:
    """
    The parent player class, that the player objects used in Blackjack class inherit from this class.

    This class and all sub player classes handle the high level functionality of the player.

    Each player class holds Hand objects in a list which actually play the game and handle the decisions
    of the player.

    A player starts each game playing with one hand, held in the list called hands.
    """

    def __init__(self, name="Name", type="None"):
        self.name = name
        self.type = type
        self.hands = []
        if self.type != "None":
            hand = self.chooseHandType(self.type)
        else:
            hand = Hand()
        hand.setPlayer(self)
        self.hands.append(hand)
        self.cash = 10000
        self.dealerUpCard = None
        self.bet = 2

    def getHand(self, index):
        return self.hands[index]

    def getFirstHand(self):
        return self.hands[0]

    def isLastHand(self, hand):
        return hand == self.hands[-1]

    def addHand(self):
        if self.type != "None":
            hand = self.chooseHandType(self.type)
        else:
            hand = Hand()
        hand.setPlayer(self)
        self.hands.append(hand)
        return hand

    def getBet(self):
        self.cash -= self.bet
        return self.bet

    def recieveProfit(self, profit):
        self.cash += profit

    def newRound(self):
        hand = self.hands.pop(0)
        hand.reset()
        self.hands = []
        self.hands.append(hand)
        self.dealerUpCard = None

    # Chooses which hand type the player should use
    def chooseHandType(self, type):
        if type == "Random":
            return RandomHand()
        elif type == "Optimal":
            return OptimalHand()
        elif type == "QLearning":
            return QLearningHand()
        elif type == "Basic":
            return BasicHand()

    def recieveDealerUpCard(self, card):
        self.dealerUpCard = card


class Hand:
    """
    This class handles the game play functionality on behalf
    of the player that possesses an object of this class.

    All other hand types inherit from this class.

    The Blackjack class calls methods from the hand class
    in order to get the decisions of a player during gameplay.
    """

    def __init__(self):
        self.cards = []
        self.player = None

    def setPlayer(self, player):
        self.player = player

    def recieveCards(self, cards):
        for card in cards:
            self.cards.append(card)

    def getSum(self):
        cardsSum = sum(self.cards)
        for card in self.cards:
            if card == 1 and (cardsSum + 10) <= 21:
                cardsSum += 10

        return cardsSum

    def getBet(self):
        return self.player.getBet()

    def getAction(self):
        if len(self.cards) == 2:
            if self.cards[0] == self.cards[1]:
                return Actions.SPLIT

        if self.getSum() < 17 or (
                1 in self.cards and self.getSum() == 17 and len(self.cards) == 2):  # dealer will hit on soft 17
            return Actions.HIT
        else:
            return Actions.STAND

    def recieveReward(self, reward):
        pass

    def recieveProfit(self, profit):
        self.player.recieveProfit(profit)

    def giveCardBack(self):
        return self.cards.pop(0)

    def reset(self):
        self.cards = []


class QLearningAgent(Player):
    """
    Q Learning agent object that inherits from the Player class.

    This class contains all of the Q Learning algorithm logic.
    """
    def __init__(self, name="Name", type="None"):
        Player.__init__(self, name, type)
        self.qValues = Counter()
        self.betQValues = Counter()
        self.epsilon = 1
        self.alpha = 0.5
        self.discount = 0.5
        self.count = 0
        self.epsilonDecreasing = False
        self.epsilonDecreasingFactor = 0.1
        self.qLearningBetting = False
        self.bettingQValues = Counter()
        self.bet = 2
        self.currentBetExperience = None
        self.collapsedStateSpace = False

    #Card playing Q-Learning methods
    def getQValue(self, state, action):
        actualState = (state[1], state[2], state[3], state[4])
        if self.collapsedStateSpace == True:
            actualState = (state[1], state[3])
        return self.qValues[actualState, action]

    def computeValueFromQValues(self, state):
        if state == "Terminal" or len(getAvailableActions(state[0])) == 0:
            return 0.0
        maxValue = -sys.maxint
        for action in getAvailableActions(state[0]):
            if self.getQValue(state, action) > maxValue:
                maxValue = self.getQValue(state, action)
        return maxValue

    def computeActionFromQValues(self, state):
        if len(getAvailableActions(state[0])) == 0:
            return None
        maxAction = getAvailableActions(state[0])[0]
        for action in getAvailableActions(state[0]):
            if self.getQValue(state, action) > self.getQValue(state, maxAction):
                maxAction = action
        return maxAction

    def getAction(self, state):
        legalActions = getAvailableActions(state[0])

        if len(legalActions) == 0:
            return None

        if flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            return self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward):
        actualState = (state[1], state[2], state[3], state[4])
        if self.collapsedStateSpace == True:
            actualState = (state[1], state[3])
        qVal = self.getQValue(state, action)
        self.qValues[actualState, action] = qVal + self.alpha * (
                    (reward + self.discount * self.computeValueFromQValues(nextState)) - qVal)

    def recieveReward(self, reward, handExperiences):
        self.count += 1
        if self.count == 10000 and self.epsilon > 0 and self.epsilonDecreasing:
            self.epsilon -= self.epsilonDecreasingFactor
            self.count = 0
        for i in range(len(handExperiences) - 1):
            if i == 0:
                self.update(handExperiences[i + 1][0], handExperiences[i + 1][1], handExperiences[i][0], reward)
            else:
                self.update(handExperiences[i + 1][0], handExperiences[i + 1][1], handExperiences[i][0], 0)

    # Betting strategy playing Q-Learning methods
    def getBetQValue(self, state, action):
        return self.betQValues[state, action]

    def computeValueFromBetQValues(self, state):
        if state == "Terminal" or len(getBetActions(self.bet)) == 0:
            return 0.0
        maxValue = -sys.maxint
        for action in getBetActions():
            if self.getBetQValue(state, action) > maxValue:
                maxValue = self.getBetQValue(state, action)
        return maxValue

    def computeActionFromBetQValues(self, state):
        if len(getBetActions(self.bet)) == 0:
            return None
        maxAction = getBetActions(self.bet)[0]
        for action in getBetActions(self.bet):
            if self.getBetQValue(state, action) > self.getBetQValue(state, maxAction):
                maxAction = action
        return maxAction

    def getBet(self):
        if not self.qLearningBetting:
            self.cash -= self.bet
            return self.bet

        legalActions = getBetActions(self.bet)

        if len(legalActions) == 0:
            bet = None

        profitState = - 1.0 * (10000 - self.cash)
        profitState = int(math.ceil(profitState / 10.0)) * 10
        if flipCoin(self.epsilon):
            bet = random.choice(legalActions)
        else:
            bet = self.computeActionFromBetQValues(profitState)

        # Update the player's bet based the betting action choice
        if bet == BettingActions.DOUBLEBET:
            self.bet *= 2
        elif bet == BettingActions.BETLESS:
            self.bet -= 15
        elif bet == BettingActions.BETMORE:
            self.bet += 15
        elif bet == BettingActions.MAXBET:
            self.bet = 1000
        else:
            self.bet = 15

        self.currentBetExperience = (profitState, bet)
        self.cash -= self.bet
        return self.bet

    def updateBetQValues(self, state, action, nextState, reward):
        qVal = self.getBetQValue(state, action)
        self.qValues[state, action] = qVal + self.alpha * (
                    (reward + self.discount * self.computeValueFromBetQValues(nextState)) - qVal)

    def recieveProfit(self, profit):
        if self.qLearningBetting:
            if profit == self.bet:
                self.updateBetQValues(self.currentBetExperience[0], self.currentBetExperience[1], "Terminal", 0)
            elif profit == 0:
                self.updateBetQValues(self.currentBetExperience[0], self.currentBetExperience[1], "Terminal", -self.bet)
            else:
                self.updateBetQValues(self.currentBetExperience[0], self.currentBetExperience[1], "Terminal", profit)
        self.cash += profit


class QLearningHand(Hand):
    """
    The Hand subclass used by the Q Learning player class.

    Overrides necessary methods of the hand to use the Q-Learning player's methods.
    """
    def __init__(self):
        Hand.__init__(self)
        self.experiences = []

    def getAction(self):
        ace = False
        if (1 in self.cards):
            ace = True
        split = False
        if Actions.SPLIT in getAvailableActions(self.cards):
            split = True
        state = (self.cards, self.getSum(), ace, self.player.dealerUpCard, split)
        action = self.player.getAction(state)
        self.experiences.insert(0, (state, action))
        return action

    def recieveReward(self, reward):
        var = ("Terminal", Actions.NONE)
        self.experiences.insert(0, var)
        self.player.recieveReward(reward, self.experiences)

    def reset(self):
        Hand.reset(self)
        self.experiences = []


class RandomHand(Hand):
    """
    The Hand subclass used by the Random Player.
    """
    def getAction(self):
        return random.choice(getAvailableActions(self.cards))


class BasicHand(Hand):
    """
    The Hand subclass used by the Basic Player.
    """
    def getAction(self):
        if len(self.cards) == 2:
            if self.cards[0] == self.cards[1] and self.cards[0] == 8:
                return Actions.SPLIT
                # print "THIS PLAYER SPLIT"
        if self.getSum() > 14 or self.getSum() < 17:
            return Actions.DOUBLE

        if self.getSum() < 19:
            return Actions.HIT
        else:
            return Actions.STAND


class OptimalHand(Hand):
    """
    The Hand subclass used by Optimal Player
    """
    def getAction(self):
        if self.getSum() == 8 and 1 not in self.cards:
            return Actions.HIT
        elif self.getSum() == 9 and 1 not in self.cards:
            if self.player.dealerUpCard > 2 and self.player.dealerUpCard < 7:
                return Actions.DOUBLE
            else:
                return Actions.HIT
        elif self.getSum() == 10 and 1 not in self.cards:
            if self.player.dealerUpCard < 10 and self.player.dealerUpCard > 1:
                return Actions.DOUBLE
            else:
                return Actions.HIT
        elif self.getSum() == 11 and 1 not in self.cards:
            if self.player.dealerUpCard > 1:
                return Actions.DOUBLE
            else:
                return Actions.HIT
        elif self.getSum() == 12 and 1 not in self.cards:
            if self.player.dealerUpCard > 3 and self.player.dealerUpCard < 7:
                return Actions.STAND
            else:
                return Actions.HIT
        elif self.getSum() > 12 and self.getSum() < 17 and 1 not in self.cards:
            if self.player.dealerUpCard > 1 and self.player.dealerUpCard < 7:
                return Actions.STAND
            else:
                return Actions.HIT
        elif self.getSum() == 17 and 1 not in self.cards:
            return Actions.STAND
        elif self.getSum() == 13:
            if self.player.dealerUpCard > 4 and self.player.dealerUpCard < 7:
                return Actions.DOUBLE
            else:
                return Actions.HIT
        elif self.getSum() == 14:
            if self.player.dealerUpCard > 4 and self.player.dealerUpCard < 7:
                return Actions.DOUBLE
            else:
                return Actions.HIT
        elif self.getSum() == 15:
            if self.player.dealerUpCard > 3 and self.player.dealerUpCard < 7:
                return Actions.DOUBLE
            else:
                return Actions.HIT
        elif self.getSum() == 16:
            if self.player.dealerUpCard > 3 and self.player.dealerUpCard < 7:
                return Actions.DOUBLE
            else:
                return Actions.HIT
        elif self.getSum() == 17:
            if self.player.dealerUpCard > 2 and self.player.dealerUpCard < 7:
                return Actions.DOUBLE
            else:
                return Actions.HIT
        elif self.getSum() == 18:
            if self.player.dealerUpCard < 2 or self.player.dealerUpCard > 8:
                return Actions.HIT
            elif self.player.dealerUpCard > 2 and self.player.dealerUpCard < 7:
                return Actions.DOUBLE
            else:
                return Actions.STAND
        elif self.getSum() == 19:
            return Actions.STAND
        elif len(self.cards) == 2 and self.cards[0] == self.cards[1]:
            if self.getSum() == 4 or self.getSum() == 6:
                if self.player.dealerUpCard < 8 and self.player.dealerUpCard > 1:
                    return Actions.SPLIT
                else:
                    return Actions.HIT
            elif self.getSum() == 8:
                if self.player.dealerUpCard > 4 and self.player.dealerUpCard < 7:
                    return Actions.HIT
                else:
                    return Actions.SPLIT
            elif self.getSum() == 10:
                if self.player.dealerUpCard < 10 and self.player.dealerUpCard > 1:
                    return Actions.DOUBLE
                else:
                    return Actions.HIT
            elif self.getSum() == 12:
                if self.player.dealerUpCard > 1 and self.player.dealerUpCard < 7:
                    return Actions.SPLIT
                else:
                    return Actions.HIT
            elif self.getSum() == 14:
                if self.player.dealerUpCard > 1 and self.player.dealerUpCard < 8:
                    return Actions.SPLIT
                else:
                    return Actions.HIT
            elif self.getSum() == 16 or self.getSum() == 2 or self.getSum() == 12:
                return Actions.SPLIT
            elif self.getSum() == 18:
                if self.player.dealerUpCard == 7 or self.player.dealerUpCard == 10 or self.player.dealerUpCard == 1:
                    return Actions.STAND
                else:
                    return Actions.SPLIT
            elif self.getSum() == 20:
                return Actions.STAND
        else:
            return Actions.STAND
