
class Table:
    hands = []
    def __init__(self, name, bb, ante):
        self.name = name
        self.bb = bb
        self.ante = ante
     
class Hand:
    board = None
    players = []
    actions = []
    winners = None
    showdown = False #does this hand go to showdown
    def __init__(self, id):
        self.id = id

class Board:
    def __init__(self, cards):
        self.cards = cards
        
class PlayerinHand:
    def __init__(self, stacksize, pos, 
    

class Action:
    #Type will be Ante, Post?, Bet, Call, Fold, Raise
    #info is the amount of info available to player: Predeal, Preflop, Flop, Turn, River
    def __init__(self, type, info, amount, player):
        self.type = type
        self.info = info
        self.amount = amount
        self.player = player

