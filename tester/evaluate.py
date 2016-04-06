import platform
import time
import traceback
from itertools import permutations, combinations_with_replacement

from poker_game import PokerGame
from naive_bots import *

MAX_PLAYERS = 8
NUM_TESTS = 100

def evaluate():

    seed = 0
    results = []

    bots = [FoldBot,RandomBet,MinBet,AllIn,RandomBot]
    for num_players in range(MAX_PLAYERS):
        for combination in combinations_with_replacement(bots,num_players):
            for permutation in permutations(combination,numplayers):
                for i in range(NUM_TESTS):
                    game = PokerGame(bots=permutation, seed=seed)
                    results.append(game.run())
                    seed += 1


if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except Exception, e:
        print ""
        traceback.print_exc()
    if platform.system() == 'Windows':
        raw_input('\nPress enter to continue')
