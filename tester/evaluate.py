import platform
import time
import traceback

from poker_game import PokerGame
from naive_bots import *

def main():

    seed = None

    bots = [FoldBot,RandomBet,MinBet,AllIn,RandomBot]
    game = PokerGame(bots=bots, seed=seed)
    start_time = time.time()
    outcome = game.run()
    end_time = time.time()
    print "Result:", outcome
    print "Time elapsed: %0.2f seconds" % (end_time - start_time)

if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except Exception, e:
        print ""
        traceback.print_exc()
    if platform.system() == 'Windows':
        raw_input('\nPress enter to continue')
