import unittest
from blackjack import *
from player import *


class TestBlackJack(unittest.TestCase):
    """Test File used to test the correctness of the blackjack environment.
        Run using the command python blackjack-tests.py
        """
    blackjack = Blackjack()

    def test_createPlayer(self):
        player = Player()
        self.assertEqual(len(player.hands), 1, "Hands count should be 1")

    def test_playerCount(self):
        self.assertEqual(len(self.blackjack.players), 4, "Should be 4")

    def test_getPlayerBets(self):
        self.blackjack = Blackjack()
        self.blackjack.getBets()
        for player in self.blackjack.players:
            self.assertEqual(self.blackjack.playerHands[player][0][1], 2, "{} Should be 2".format(self.blackjack.playerHands[player][0][1]))

    def test_dealCards(self):
        self.blackjack = Blackjack()
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.assertEqual(len(self.blackjack.dealer.hand), 2, "Should be 2")
        for player in self.blackjack.players:
            self.assertEqual((len(self.blackjack.playerHands[player][0][0].cards)), 2, "Should be 2")
            print player.dealerUpCard
            self.assertEqual(player.dealerUpCard, self.blackjack.dealer.hand[0], "The dealer has {0} but the player has {1}".format(self.blackjack.dealer.hand[0], player.dealerUpCard))

    def test_Hit(self):
        testPlayer = TestPlayer("HIT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 4, 8, 7, 6, 1, 4]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(self.blackjack.playerHands[testPlayer][0][0].cards, [10,4, 6, 1],
                         "{} Should be [10, 4]".format(self.blackjack.playerHands[testPlayer][0][0].cards))
        self.assertEqual(testPlayer.hands[0].cards, [10, 4, 6, 1],
                         "{} Should be [10, 4, 6, 1]".format(testPlayer.hands[0].cards))
        self.assertEqual(self.blackjack.dealer.hand, [8, 7, 4],
                         "{} Should be [8, 7, 4]".format(self.blackjack.dealer.hand))

    def test_Stand(self):
        testPlayer = TestPlayer("STAND")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 9, 8, 9, 6, 2]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(self.blackjack.playerHands[testPlayer][0][0].cards, [10, 9],
                         "{} Should be [10, 9]".format(self.blackjack.playerHands[testPlayer][0][0].cards))
        self.assertEqual(testPlayer.hands[0].cards, [10, 9],
                         "{} Should be [10, 9]".format(testPlayer.hands[0].cards))
        self.assertEqual(self.blackjack.dealer.hand, [8, 9],
                         "{} Should be [8, 9]".format(self.blackjack.dealer.hand))

    def test_Double(self):
        testPlayer = TestPlayer("DOUBLE")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 4, 8, 9, 6, 2, 4, 4]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.assertEqual(self.blackjack.playerHands[testPlayer][0][1], testPlayer.hands[0].getBet() * 2,
                         "Bet was {}, should be 4".format(self.blackjack.playerHands[testPlayer][0][1]))
        self.assertEqual(testPlayer.cash, 9996, "Should be 9996 but was {}".format(testPlayer.cash))
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(self.blackjack.playerHands[testPlayer][0][0].cards, [10, 4, 6],
                         "{} Should be [10, 4, 6]".format(self.blackjack.playerHands[testPlayer][0][0].cards))
        self.assertEqual(testPlayer.hands[0].cards, [10, 4, 6],
                         "{} Should be [10, 4, 6]".format(testPlayer.hands[0].cards))
        self.assertEqual(self.blackjack.dealer.hand, [8, 9],
                         "{} Should be [8, 9]".format(self.blackjack.dealer.hand))


    def test_Split(self):
        testPlayer = TestPlayer("SPLIT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 10, 9, 8, 4, 6, 10, 5, 2, 8]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.assertEqual(len(self.blackjack.playerHands[testPlayer]), 3, "Should have three hands")
        for i in range(3):
            self.assertEqual(self.blackjack.playerHands[testPlayer][i][1], 2, "Bet should be 2")
        self.assertEqual(testPlayer.cash, 9994)

        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()

        self.assertEqual(self.blackjack.dealer.hand, [9, 8],
                         "{} Should be [9, 8]".format(self.blackjack.dealer.hand))

        self.assertEqual(self.blackjack.playerHands[testPlayer][0][0].cards, [10, 4, 6],
                         "{} should be [10, 4, 6]".format(self.blackjack.playerHands[testPlayer][0][0].cards))
        self.assertEqual(testPlayer.hands[0].cards, [10, 4, 6], "{} should be [10, 4, 6]".format(testPlayer.hands[0].cards))

        self.assertEqual(self.blackjack.playerHands[testPlayer][1][0].cards, [10, 5, 2],
                         "{} should be [10, 5, 2]".format(self.blackjack.playerHands[testPlayer][1][0].cards))
        self.assertEqual(testPlayer.hands[1].cards, [10, 5, 2], "{} should be [10, 5, 2]".format(testPlayer.hands[1].cards))

        self.assertEqual(self.blackjack.playerHands[testPlayer][2][0].cards, [10, 8],
                         "{} should be [10, 8]".format(self.blackjack.playerHands[testPlayer][2][0].cards))
        self.assertEqual(testPlayer.hands[2].cards, [10, 8], "{} should be [10, 8]".format(testPlayer.hands[2].cards))


    def test_payoutsOverMultipleRounds(self):
        testPlayer = TestPlayer("HIT")
        self.blackjack = Blackjack()
        self.blackjack.iterations = 5
        self.blackjack.players = [testPlayer]
        testDeck = [10, 1, 10, 10, 10, 1, 10, 10, 10, 1, 10, 10, 10, 10, 10, 10, 10, 8, 10, 10]
        for i in range(200):
            testDeck.append(1)
        self.blackjack.deck = testDeck
        self.blackjack.runBlackjack()
        self.assertEqual(testPlayer.cash, 10007, "{} should be 10009".format(testPlayer.cash))
        self.assertEqual(len(testPlayer.hands), 1, "Should have one hand")
        self.assertEqual(len(testPlayer.hands[0].cards), 0, "The hand should have no cards")
        self.assertEqual(len(self.blackjack.dealer.hand), 0, "The dealer should have no cards")


    #Both players bust, player loses
    def test_bothPlayerAndDealerBustPlayerLoses(self):
        testPlayer = TestPlayer("PAYOUT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 8, 8, 7, 8, 10]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(testPlayer.cash, 9998, "Player should lose the bet")

    #Dealer has 20, player busts and loses
    def test_playerBustsPlayerLoses(self):
        testPlayer = TestPlayer("PAYOUT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 8, 10, 10, 4]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(testPlayer.cash, 9998, "Player should lose the bet")


    #Dealer has 20, player has 19 and loses
    def test_playerSumLessThanDealerSumPlayerLoses(self):
        testPlayer = TestPlayer("PAYOUT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 9, 10, 10, 2, 10]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(testPlayer.cash, 9998, "Player should lose the bet")

    #Dealer busts, player has 20 and wins
    def test_dealerBustsPlayerWins(self):
        testPlayer = TestPlayer("PAYOUT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 9, 10, 6, 2, 8]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(testPlayer.cash, 10002, "Player should win the bet")

    #Dealer has 19, player has 20 and wins
    def test_playerSumGreaterThanDealerSumPlayerWins(self):
        testPlayer = TestPlayer("PAYOUT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 9, 10, 8, 2, 10]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(testPlayer.cash, 10002, "Player should win the bet")

    #Dealer has 20, player has 20, push
    def test_playerSumEqualDealerSumPush(self):
        testPlayer = TestPlayer("PAYOUT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 9, 10, 9, 2, 10]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(testPlayer.cash, 10000, "Player should keep the bet")

    #Delaer has 20, player has 21 naturally and wins 3:2
    def test_playerNaturalBlackjackPayout(self):
        testPlayer = TestPlayer("PAYOUT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 1, 10, 10, 2, 10]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(testPlayer.cash, 10003, "Player should win the bet 3:2")

    #Player has 21 unnaturally, dealer has 20 and player gets 1:1
    def test_playerWinsWithBlackjackPayout(self):
        testPlayer = TestPlayer("PAYOUT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 7, 10, 10, 4, 10]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(testPlayer.cash, 10002, "Player should win the bet 1:1")

    #Player wins payout
    def test_playerWinsPayout(self):
        testPlayer = TestPlayer("PAYOUT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 9, 10, 8, 2, 10]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(testPlayer.cash, 10002, "Player should win the bet 1:1")

    #Player loses, lost money
    def test_playerLosesPayout(self):
        testPlayer = TestPlayer("PAYOUT")
        self.blackjack = Blackjack()
        self.blackjack.players = [testPlayer]
        self.blackjack.deck = [10, 9, 10, 10, 2, 10]
        self.blackjack.getBets()
        self.blackjack.dealHands()
        self.blackjack.handlePlayerMoves()
        self.blackjack.handleDealerMoves()
        self.blackjack.handlePlayerPayouts()
        self.assertEqual(testPlayer.cash, 9998, "Player should lose the bet")


    #Test if initial player hand has no dealer face upcard
    def test_playerHandHasNoFaceCardInBeginningOfRound(self):
        pass
    #test if the initial player hand recieves the dealer face up card
    def test_playerHasDealerFaceUpCard(self):
        pass
    #test if the player splits and both hands have the dealer face up card
    def test_playerSplitsThenBothHandsHaveFaceUpCard(self):
        pass

    def test_handDealerFaceUpCardCleared(self):
        pass

    # A visual test as well, should see ten 1oo game learning phase print outs
    def test_learningPhase(self):
        testPlayer = TestPlayer("HIT")
        self.blackjack = Blackjack(1000, 1)
        self.blackjack.players = [testPlayer]
        self.blackjack.gameStatCollector.players = [testPlayer]
        self.blackjack.runBlackjack(Phase.LEARNING)
        self.assertEqual(len(self.blackjack.gameStatCollector.learningRecords), 1000, "Should be 1000 records")

    # A visual test as well, should see 200 single game testing rescors printed
    def test_testPhase(self):
        testPlayer = TestPlayer("HIT")
        self.blackjack = Blackjack(1, 200)
        self.blackjack.players = [testPlayer]
        self.blackjack.gameStatCollector.players = [testPlayer]
        self.blackjack.runBlackjack(Phase.TESTING)
        self.assertEqual(len(self.blackjack.gameStatCollector.testingRecords), 200, "Should be 200 records")

    def test_usageGuideTest(self):
        # Sample on how to use, can use this in test suite script
        self.blackjack = Blackjack(100000, 250)
        self.blackjack.runBlackjack(Phase.LEARNING)
        self.blackjack.runBlackjack(Phase.TESTING)


"""Special Test Players and Hands"""
class TestPlayer(Player):
    def __init__(self, handType, name="Test"):
        self.name = name
        self.type = "None"
        self.hands = []
        hand = self.createhandBasedOnHandType(handType)
        # hand = Hand()
        hand.setPlayer(self)
        self.hands.append(hand)
        self.cash = 10000
        self.bet = 2

    def createhandBasedOnHandType(self, handType):
        if handType == "HIT":
            return TestHitHand()
        elif handType == "STAND":
            return TestStandHand()
        elif handType == "DOUBLE":
            return TestDoubleHand()
        elif handType == "SPLIT":
            return TestSplitHand()
        else:
            return TestPayoutHand()



class TestHitHand(Hand):
    def getAction(self):
        if self.getSum() < 21:
            return Actions.HIT
        else:
            return Actions.STAND

class TestStandHand(Hand):
    def getAction(self):
        return Actions.STAND

class TestDoubleHand(Hand):
    def getAction(self):
        return Actions.DOUBLE

class TestSplitHand(Hand):
    def getAction(self):
        if len(self.cards) == 2:
            if self.cards[0] == self.cards[1]:
                return Actions.SPLIT
                # print "THIS PLAYER SPLIT"

        if self.getSum() < 17 or (
                1 in self.cards and self.getSum() == 17 and len(self.cards) == 2):  # dealer will hit on soft 17
            return Actions.HIT
        else:
            return Actions.STAND


class TestPayoutHand(Hand):
    def getAction(self):
        if self.getSum() <= 18:
            return Actions.HIT
        else:
            return Actions.STAND

if __name__ == '__main__':
    unittest.main()