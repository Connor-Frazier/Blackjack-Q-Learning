from blackjack import *
from player import *
import time
import optparse

"""Main project run file"""

def run(options):
    """Main run method that runs the learning and testing phases for an experiment with the command line options"""
    #Initialize the environment
    blackjack = Blackjack(100000, 250)
    # Set the options of the game based on the parameters of the script
    blackjack.winReward = float(options.winReward)
    blackjack.pushReward = float(options.pushReward)
    blackjack.loseReward = float(options.loseReward)
    blackjack.players[0].alpha = float(options.alpha)
    blackjack.players[0].discount = float(options.discount)
    blackjack.players[0].epsilon = float(options.epsilon)
    blackjack.players[0].epsilonDecreasing = bool(options.epsilonDecreasing)
    blackjack.players[0].epsilonDecreasingFactor = float(options.epsilonDecreasingFactor)
    blackjack.players[0].qLearningBetting = bool(options.qLearningBetting)
    blackjack.players[0].bet = int(options.initialBet)
    blackjack.players[1].bet = int(options.initialControlBet)
    blackjack.players[2].bet = int(options.initialControlBet)
    blackjack.players[3].bet = int(options.initialControlBet)
    blackjack.players[0].collapsedStateSpace = bool(options.collapsedStateSpace)

    # Run Learning
    blackjack.runBlackjack(Phase.LEARNING)
    results = []
    # Run testing
    for i in range(10):
        blackjack.runBlackjack(Phase.TESTING)
        # Collect the results of each test game
        for result in blackjack.gameStatCollector.finalResults:
            results.append(result)
        # time.sleep(5)

    print "\n\n\n"
    # Calculate and print the final test results for each player over the ten rounds of testing.
    for player in blackjack.players:
        profit = 0
        winPercentage = 0
        for result in results:
            if result[0] == player.name:
                profit += result[1]
                winPercentage += result[2]
        print "{0}, Average Profits: {1}, Average Win Percetage: {2}".format(player.name, profit / 10,
                                                                             winPercentage / 10)


# Read in the command line arguments
def readCommand(argv):
    parser = optparse.OptionParser(description='Run project script')
    parser.set_defaults(generateSolutions=False, edxOutput=False, muteOutput=False, printTestCase=False,
                        noGraphics=False)
    parser.add_option('--win-reward',
                      dest='winReward',
                      default=5,
                      help='win reward for the q learning agent in blackjack')
    parser.add_option('--push-reward',
                      dest='pushReward',
                      default=0,
                      help='push reward for the q learning agent in blackjack')
    parser.add_option('--lose-reward',
                      dest='loseReward',
                      default=-10,
                      help='lose reward for the q learning agent in blackjack')
    parser.add_option('--alpha',
                      dest='alpha',
                      default=0.5,
                      help='alpha for the q learning agent in blackjack')
    parser.add_option('--discount',
                      dest='discount',
                      default=0.5,
                      help='discount for the q learning agent in blackjack')
    parser.add_option('--epsilon',
                      dest='epsilon',
                      default=1,
                      help='epsilon for the q learning agent in blackjack')
    parser.add_option('--epsilonDecreasing',
                      dest='epsilonDecreasing',
                      default=False,
                      help='epsilon decreasing boolean for the q learning agent in blackjack')
    parser.add_option('--epsilonDecreasingFactor',
                      dest='epsilonDecreasingFactor',
                      default=0.1,
                      help='epsilon decreasing factor for the q learning agent in blackjack')
    parser.add_option('--qLearningBetting',
                      dest='qLearningBetting',
                      default=False,
                      help='q learning betting boolean for the q learning agent in blackjack')
    parser.add_option('--initialBet',
                      dest='initialBet',
                      default=2,
                      help='initial bet for the q learning agent in blackjack')
    parser.add_option('--initialControlPlayersBet',
                      dest='initialControlBet',
                      default=2,
                      help='initial bet for the control agents in blackjack')
    parser.add_option('--collapsedStateSpace',
                      dest='collapsedStateSpace',
                      default=False,
                      help='collapsed state space for the q learning agent in blackjack')

    (options, args) = parser.parse_args(argv)
    return options


if __name__ == '__main__':
    options = readCommand(sys.argv)
    run(options)
