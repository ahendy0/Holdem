from holdem.diler import Diler
from holdem.player import CLIPlayer
from holdem.different import Deck

class Table(object):
    """
    Implementation of table abstraction.
    """
    def __init__(self, name, sbl, bbl, sits_count, min_buyin):
        self.deck = Deck()
        self.diler = Diler(self.deck)
        self.sbl = sbl
        self.bbl = bbl
        self.min_buyin = min_buyin
        self.but_pos = 1
        self.table_history = []
        self.sits = range(1, sits_count + 1)
        self.players = []

    def add_player(self, player):
        """Registers player for current table"""
        tplayer = CLIPlayer(player)
        tplayer.take_sit(self.__available_sits__())
        tplayer.make_buyin(self.min_buyin)
        self.players.append(tplayer)
        tplayer.become_active()
        
    def remove_player(self, player):
        """Removes player from current table"""
        pass
        

    def __available_sits__(self):
        """Returns list of sits numbers that are avaialble for players"""
        return list(set(self.sits) - set(self.__occupied_sits__()))

    def __occupied_sits__(self):
        """Returns list of sits numbers that are occupied by players"""
        return [player.sit for player in self.players]

