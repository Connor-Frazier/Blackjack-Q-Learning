from util import *
import csv

class GameStatCollector:
    """
    This class is used by the Blackjack class in order to store and calculate statistics of the game
    over the course of gameplay.
    """

    def __init__(self, players, phase = Phase.NONE):
        self.roundCount = 0
        self.currentPhase = phase
        self.learningRecords = []
        self.testingRecords = []
        self.players = players
        self.learningRecordsBatch = []
        self.learningEpisodeBlocks = []
        self.finalResults = None

    #Recieve and store the outcome of one game for a player
    def recievePlayerResult(self, player, profit, outcome, reward):
        record = EpisodeResult(player, profit, outcome, reward)
        if self.currentPhase == Phase.NONE:
            pass    
        elif self.currentPhase == Phase.LEARNING:
            self.learningRecords.append(record)
            self.learningRecordsBatch.append(record)
            if self.roundCount > 0 and self.roundCount % 1000 == 0 and player == self.players[-1]:
                self.printOneThousandTrainingEpisodes()
                self.learningRecordsBatch = []
        elif self.currentPhase == Phase.TESTING:
            self.testingRecords.append(record)
            self.printTestingRecord(record)


    def newRound(self):
        self.roundCount += 1

    #Used in learning phase to print out the results of 1000 games
    def printOneThousandTrainingEpisodes(self):
        learningEpisodeBlockData = []
        for player in self.players:
            index = 0
            profit = 0
            wins = 0
            push = 0
            loss = 0
            rewards = 0
            handsCount = 0
            for i in range(len(self.learningRecordsBatch)):
                if self.learningRecordsBatch[index].player == player:
                    handsCount += 1
                    profit += self.learningRecordsBatch[index].profit
                    if self.learningRecordsBatch[index].outcome == "WIN":
                        wins += 1
                    elif self.learningRecordsBatch[index].outcome == "PUSH":
                        push += 1
                    else:
                        loss += 1
                    rewards += self.learningRecordsBatch[index].reward
                index += 1
            if handsCount == 0:
                handsCount = 1
            learningEpisodeBlockData.append((1.0 * rewards)/(1.0 * handsCount))
            print "Player: {0}, Wins: {1}, Pushes: {2}, Losses: {3}, hands played(over 1000 rounds): {4}, Win Percentage: {5}, Average Rewards: {6}"\
                .format(player.name, wins, push, loss, handsCount, (1.0 * wins)/(1.0 * handsCount), (1.0 * rewards)/(1.0 * handsCount))
        self.learningEpisodeBlocks.append(learningEpisodeBlockData)
        print "\n"

    #Prints the result of a game for a player during testing
    def printTestingRecord(self, record):
        print "Player: {0}, Hand: {1}, Profit: {2}, Outcome: {3}".format(record.player.name, self.roundCount, record.profit, record.outcome)

    #Prints final testing round results
    def printFinalTestResults(self):
        results = []
        print "Final Test Result:"
        for player in self.players:
            index = 0
            profit = 0 # not being used at the moment
            wins = 0
            push = 0
            loss = 0
            gamesPlayed = self.roundCount
            rewards = 0
            for i in range(len(self.testingRecords)):
                if self.testingRecords[index].player == player:
                    profit += self.testingRecords[index].profit
                    if self.testingRecords[index].outcome == "WIN":
                        wins += 1
                    elif self.testingRecords[index].outcome == "PUSH":
                        push += 1
                    else:
                        loss += 1
                    rewards += self.testingRecords[index].reward
                index += 1
            results.append((player.name, profit, (1.0 * wins)/(1.0 * gamesPlayed)))
            print "Player: {0}, profits: {1}, win percentage: {2}".format(player.name, profit, (1.0 * wins)/(1.0 * gamesPlayed))
        self.finalResults = results
        self.downloadFiles()

    #Writes necessary data to a csv file for analysis
    def downloadFiles(self):
        with open('blackjack-learning.csv', mode='w') as learning_file:
            csv_writer = csv.writer(learning_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            csv_writer.writerow(['Q Learning', 'Optimal', 'Basic', 'Random'])
            for block in self.learningEpisodeBlocks:
                csv_writer.writerow(block)


#Data object for internal storage
class EpisodeResult:

    def __init__(self, player, profit, outcome, reward):
        self.player = player
        self.profit = profit
        self.outcome = outcome
        self.episodeCount = 1
        self.reward = reward


    def printRecord(self):
        print "record output"


#Data object for internal storage
class LearningEpisodeBlock:

    def __init__(self, player, wins, push, loss, gamesPlayed, winPercentage, aveRewards):
        self.player = player
        self.wins = wins
        self.push = push
        self.loss = loss,
        self.gamesPlayed = gamesPlayed
        self.winPercentage = winPercentage
        self.aveRewards = aveRewards

