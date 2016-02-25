from enum import Enum

class Table:
    hands = []
    def __init__(self, name, type, bb, ante):
        self.name = name
        self.type = type
        self.bb = bb
        self.ante = ante
     
class Hand:
    board = None
    players = [] #dealer is always first player in list
    actions = []
    winners = None
    showdown = False #does this hand go to showdown
    def __init__(self, id):
        self.id = id

class Board:
    def __init__(self, cards):
        self.cards = cards
        
class PlayerinHand:
    def __init__(self, stack, pos)
        self.sstack = stack #original stack size used to calc the net in the hand
        self.stack = stack #will be modified by bets call raise
        self.pos = pos #pos from dealer where dealer is pos 0 maybe change this based on who folds?
        
class Action:
    #Type will be Ante, Post?, Bet, Call, Fold, Raise, timeout
    #info is the amount of info available to player: Predeal, Preflop, Flop, Turn, River
    def __init__(self, type, info, amount, player):
        self.type = type
        self.info = info
        self.amount = amount
        self.player = player


class ActionType(Enum):
    ANTE = 0
    POST = 1
    BET = 2
    CALL = 3
    FOLD = 4
    RAISE = 5
    TIMEOUT = 6
    
    
class ActionInfo(Enum)
    PREDEAL = 0
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4 
    

    
    


    