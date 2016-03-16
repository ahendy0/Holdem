from holdem.game import *
from holdem.table import *
from holdem.diler import *
from holdem.player import *
from holdem.different import *
from holdem.naive_bots import naive_min
from copy import deepcopy
from random import choice,seed

from holdem.table import Table


SEED = 1

DEFAULT_MAX_TABLE_SIZE = 8

BIG_BLIND = 10
SMALL_BLIND = 20
MIN_BUYIN = 100
STARTING_CASH = 300

seed(SEED)

test_no = 1

for numplayers in range(DEFAULT_MAX_TABLE_SIZE):

    for testplaypos in range(numplayers):
        test_player_positions = range(numplayers)
        test_bot_pos = testplaypos
        test_player_positions.remove(test_bot_pos)
        bot_under_test = Player(name="bot_under_test",cash_amount=STARTING_CASH,plid=test_bot_pos)
        all_bots = [bot_under_test]
        for rempos in test_player_positions:
            dumb_bot = Player('p' + str(rempos), cash_amount=STARTING_CASH, plid=rempos)
            all_bots.append(dumb_bot)
        all_bots = sorted(all_bots, key= lambda x: x.plid)
        test_table = Table(name="test" + str(test_no),bbl=BIG_BLIND,sbl=SMALL_BLIND,sits_count=numplayers,min_buyin=MIN_BUYIN)
        for bot in all_bots:
            test_table.add_player(bot,True)

        game = Game(test_table)
        game.play_hand()
        test_no += 1