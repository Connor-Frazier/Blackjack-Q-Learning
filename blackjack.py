# Connor Frazier
# Final Project
# Blackjack Q learning agent

from random import shuffle

from util import *
from player import *
from statcollecter import *


class Blackjack():
    """Main environemt class that contains all of the logic for running the game of blackjack."""
    def __init__(self, learningIterations=1, testingIterations=1):

        self.learningIterations = learningIterations
        self.testingIterations = testingIterations
        self.iterations = 1
        self.deck = self.createDeck()
        self.dealer = Dealer()
        self.players = []
        self.players.append(QLearningAgent("Q Learning", "QLearning"))
        self.players.append(Player("Optimal", "Optimal"))
        self.players.append(Player("Basic", "Basic"))
        self.players.append(Player("Random", "Random"))
        self.winReward = 5
        self.pushReward = 0
        self.loseReward = -10
        self.gameOver = False
        self.playerHands = {}
        #Creates the stat collecter object that will hold all stats collected throughout gameplay
        self.gameStatCollector = GameStatCollector(self.players)

    # Main method to run the blackjack game
    def runBlackjack(self, phase=Phase.NONE):
        self.gameOver = False
        print "Running Blackjack"
        #Decides which phase to run based of the argument
        self.gameStatCollector.currentPhase = phase
        if phase == Phase.LEARNING:
            self.gameStatCollector.roundCount = 0
            self.iterations = self.learningIterations
        elif phase == Phase.TESTING:
            self.gameStatCollector.roundCount = 0
            self.gameStatCollector.testingRecords = []
            self.iterations = self.testingIterations
        count = 0
        print self.gameStatCollector.currentPhase
        #Main game loop
        while not self.gameOver:
            self.gameStatCollector.newRound()

            #Ask the players for their bets
            self.getBets()

            #Deal the player hands
            self.dealHands()

            #Have each player take their turns
            self.handlePlayerMoves()

            #Run the dealer's turn
            self.handleDealerMoves()

            #Handle the game results and the payouts
            self.handlePlayerPayouts()

            #Clear the game state for the next game
            self.clearHands()

            #Decide when to suffle
            if len(self.deck) <= 138:
                self.shuffleCards()
            count += 1

            #Set variables to end the main game loop and tell the stat collector to print the final results
            if count == self.iterations:
                self.gameOver = True
                if phase == Phase.TESTING:
                    self.gameStatCollector.printFinalTestResults()
                    # count = 0
                    # for key,value in self.players[0].qValues.items():
                    #     count += 1
                    # print count
                    #     print key
                    #     print value
                    # print self.players[0].qValuesCounts[key]

    # Create the deck of cards
    def createDeck(self):
        deck = []
        for x in range(8):
            for i in range(4):
                for j in range(10):
                    deck.append(j + 1)
                    if j + 1 == 10:
                        for k in range(3):
                            deck.append(10)
        shuffle(deck)
        return deck

    def shuffleCards(self):
        self.deck = self.createDeck()

    def dealHand(self):
        return [self.pickCard(), self.pickCard()]

    def dealCard(self):
        return [self.pickCard()]

    def pickCard(self):
        return self.deck.pop(0)

    #Handle the action choice of the player
    def handleAction(self, player, hand, handCount, action):
        if action == Actions.HIT:
            hand.recieveCards(self.dealCard())
        elif action == Actions.STAND:
            pass
        elif action == Actions.DOUBLE:
            self.playerHands[player][handCount][1] *= 2
            hand.recieveCards(self.dealCard())
        elif action == Actions.SPLIT:
            card = hand.giveCardBack()
            bet = hand.getBet()
            secondHand = player.addHand()
            secondHand.recieveCards([card])
            self.playerHands[player].append([secondHand, bet])

    #Handle the action of the dealer
    def handleDealerAction(self, action):
        if action == Actions.HIT:
            self.dealer.recieveCards(self.dealCard())
        else:
            pass

    def isHandBust(self, hand):
        return hand.getSum() > 21

    def clearHands(self):
        self.playerHands = {}
        for player in self.players:
            player.newRound()
        self.dealer.newRound()

    def getBets(self):
        for player in self.players:
            self.playerHands[player] = []
            hand = player.getFirstHand()
            bet = hand.getBet()
            self.playerHands[player].append([hand, bet])

    def dealHands(self):
        for player in self.players:
            self.playerHands[player][0][0].recieveCards(self.dealHand())
        self.dealer.recieveCards(self.dealHand())
        dealerCards = self.dealer.hand[:]
        for player in self.players:
            player.recieveDealerUpCard(dealerCards[0])

    #Handle each player's turn
    def handlePlayerMoves(self):
        for player in self.players:
            lastHandCheck = False
            handCount = 0
            while not lastHandCheck:
                hand = self.playerHands[player][handCount][0]
                action = Actions.NONE
                while action != Actions.STAND and not self.isHandBust(hand) and action != Actions.DOUBLE:
                    action = hand.getAction()
                    self.handleAction(player, hand, handCount, action)
                if player.isLastHand(hand):
                    lastHandCheck = True
                else:
                    handCount = handCount + 1

    #Handle the dealer's turn
    def handleDealerMoves(self):
        action = Actions.HIT
        while action == Actions.HIT:
            action = self.dealer.getAction()
            self.handleDealerAction(action)

    #Decide each player's game result over all of their hands and then the payouts
    def handlePlayerPayouts(self):
        for player in self.players:
            for hand in self.playerHands[player]:
                if len(hand[0].cards) == 2 and hand[0].getSum() == 21 and hand[0].getSum() > self.dealer.getSum():
                    hand[0].recieveReward(self.winReward)
                    hand[0].recieveProfit(hand[1] + 1.5 * hand[1])
                    self.gameStatCollector.recievePlayerResult(player, 1.5 * hand[1], Result.WIN, 1)
                elif not self.isHandBust(hand[0]) and (
                        hand[0].getSum() > self.dealer.getSum() or self.dealer.getSum() > 21):
                    hand[0].recieveReward(self.winReward)
                    hand[0].recieveProfit(2 * hand[1])
                    self.gameStatCollector.recievePlayerResult(player, hand[1], Result.WIN, 1)
                elif hand[0].getSum() == self.dealer.getSum():
                    hand[0].recieveReward(self.pushReward)
                    hand[0].recieveProfit(hand[1])
                    self.gameStatCollector.recievePlayerResult(player, 0, Result.PUSH, 0)
                else:
                    hand[0].recieveReward(self.loseReward)
                    hand[0].recieveProfit(0)
                    self.gameStatCollector.recievePlayerResult(player, - 2, Result.LOSS, -1)

