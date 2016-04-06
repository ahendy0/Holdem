import platform
import time
import traceback
from itertools import permutations, combinations_with_replacement
from random import shuffle
from math import factorial

from poker_game import PokerGame
from naive_bots import *
from bots import RFT, RaiseTwentyBot

MAX_PLAYERS = 4
NUM_SHUFFLES = 2
NUM_TESTS = 10

def evaluate():

    seed = 0
    results = []
    bot_under_test = RFT
    bots = [FoldBot,RandomBet,MinBet,AllIn,RandomBot,RaiseTwentyBot]
    bots += [bot_under_test]

    for num_players in range(1,MAX_PLAYERS-1):
        for combination in combinations_with_replacement(bots,num_players):
            test_group = list(combination) + [bot_under_test]
            for i in range(NUM_SHUFFLES):
                shuffle(test_group)
                for i in range(NUM_TESTS):
                    game = PokerGame(bots=test_group, seed=seed)
                    results.append(game.run())
                    seed += 1
    return results




def main():
    results = evaluate()



if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except Exception, e:
        print ""
        traceback.print_exc()
    if platform.system() == 'Windows':
        raw_input('\nPress enter to continue')
