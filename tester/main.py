import platform
import time
import traceback

from poker_game import PokerGame
from naive_bots import *

def main():
   from bots import FoldBot, RaiseTwentyBot, RFT

   ##bots = [ExampleBot, FoldBotCpp]
   seed = 999
   if len(sys.argv) > 1:
       seed = int(sys.argv[1])
   bots = [FoldBot, RaiseTwentyBot, RFT]
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
