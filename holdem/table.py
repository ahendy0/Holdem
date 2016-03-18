from holdem.diler import Diler
from holdem.player import CLIPlayer
from holdem.player import PlayerAtTable
from holdem.different import Deck

class Table(object):
    """
    Implementation of table abstraction.
    """
    def __init__(self, name, sbl, bbl, sits_count, min_buyin):
        # sbl = small blind
        # bb; = big blind
        # sit_count = max number of seats
        # min_buyin is smallest amount person can come in with
        self.deck = Deck()
        self.diler = Diler(self.deck)
        self.sbl = sbl
        self.bbl = bbl
        self.min_buyin = min_buyin
        self.but_pos = 1
        self.table_history = []
        self.sits = range(1, sits_count + 1)
        self.players = []
        self.msg_separator = '--------------'

    def add_player(self, player, bot):
        """Registers player for current table"""
        # if player doesnt have enough money, dont add them
        if player.cash_amount < self.min_buyin:
            #### print"player %d is out of chips" % player.plid
            return

        if bot:
            tplayer = PlayerAtTable(player)
        else:
            tplayer = CLIPlayer(player)

        tplayer.take_sit(self.__available_sits__())
        tplayer.make_buyin(self.min_buyin)
        self.players.append(tplayer)
        tplayer.become_active()
        
    def remove_player(self, player):
        """Removes player from current table"""

        self.players.remove(player)
        

    def __available_sits__(self):
        """Returns list of sits numbers that are avaialble for players"""
        return list(set(self.sits) - set(self.__occupied_sits__()))

    def __occupied_sits__(self):
        """Returns list of sits numbers that are occupied by players"""
        return [player.sit for player in self.players]


    def display_cards(self, game_info):
        pass
        #### printself.msg_separator
        #### print"Diler hands out next card(s): %s" % game_info['cards'][-1]

    def display_move(self, move):
        pass
        # print self.msg_separator
        #### print'\tPlayer with id %r decided to %r with %r' \
                # % (move['plid'],
                #    move['decision'].dec_type,
                #    move['decision'].value)

    def display_move_start(self):
        pass
        #### printself.msg_separator

    def on_game_started(self):
        pass
        #### printself.msg_separator
        #### print'--- So, let the game begin! ---'

    def announce_win(self, plid, comb, amount):
        pass
        #### printself.msg_separator
        #### print'Player %r wins %r with %r: %r' \
                # % (plid,
                #    amount,
                #    comb[0],
                #    comb[1])
