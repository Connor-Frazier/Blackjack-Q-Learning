# Blackjack-Q-Learning


### Overview
The goal of this project was to create a reinforcement learning agent that could learn how to play blackjack effecitively where performance was measured in terms of number of hands won and profit/loss of the agent. The secondary goal was to analyze its performance in more detail in terms of the decisions it learned to make compared to other common strategies used in blackjack. For a very detailed


### The simulator
This project was completely original. The blackjack game simulator was built from scratch to allow for more design flexibility, this included created the dealer, the basic player, hand(s) for the player, the cards, the card dealing system, the results decision, and a custom stats collector. The most interesting part about this blackjack simulator is that it includes the option for the player to split their hand when allowed. This feature was a large part of the reason for creating an original simulator as it was difficult to find an open source simulator that included split hands. Lastly unit tests were written for a majority of project to ensure that the simulator, the players and their interactions worked as intended.


### The Q-learning agent

