from enum import Enum
import re
import copy
import numpy as np
import matplotlib.pyplot as plt

class Table:
    def __init__(self, name, type, bb, ante):
        self.name = name
        self.type = type
        self.bb = bb
        self.ante = ante
        self.hands = []
        
    def __eq__(self, other):
        return self.name == other.name and self.type == other.type and self.bb == other.bb and self.ante == other.ante
    
    def __str__(self):
        return self.name + " " + self.type
     
class Hand:
    def __init__(self, id):
        self.id = id
        self.board = None
        self.players = [] #dealer is always first player in list
        self.actions = []
        self.winners = None
        self.showdown = False #does this hand go to showdown
        self.totalpot = 0
        
        
    def find_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

class Board:
    def __init__(self, cards):
        self.cards = cards
        
class PlayerinHand:
    def __init__(self, name, stack, seat):
        self.name = name
        self.origstack = stack #original stack size used to calc the net in the hand
        self.stack = stack #will be modified by bets call raise
        self.seat = seat
           
    def __str__(self):
        return self.name
        
class Action:
    #Type will be Ante, Post?, Bet, Call, Fold, Raise, timeout
    #info is the amount of info available to player: Predeal, Preflop, Flop, Turn, River
    def __init__(self, type, info, amount, player):
        self.type = type
        self.info = info
        self.amount = amount
        self.player = player
        
        #TODO IMPLEMENT
        self.called = 0
        self.tocall = 0
        self.inhand = 0
        self.cashinpot = 0
        self.amounttocall = 0
        
        
    def __str__(self):
        return self.info.name + " " + str(self.player) + " " + self.type.name + " " + str(self.amount)


class ActionType(Enum):
    ANTE = 0
    POST = 1
    BET = 2
    CALL = 3
    FOLD = 4
    RAISE = 5
    CHECK = 6
    ALLIN = 7
    TIMEOUT = 8
    
    
class ActionInfo(Enum):
    PREDEAL = 0
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4 
    
    
class ParseState(Enum):
    PSTAGE = 0
    PTABLE = 1
    PPLAYER = 2
    PPREDEAL = 3
    PPREFLOP = 4
    PFLOP = 5
    PTURN = 6
    PRIVER = 7
    PSHOWDOWN = 8
    PSUMMARY = 9
    

def findindex(list , obj):
    index = 0
    for i in list:
        if obj == i:
            return index
        index += 1
        
    return -1
    
def parse_stage(line):
  #parse stage
    handid = int(re.search('#(\d+):', line).group(1))
    
    #parse table info
    curbb = float(re.search(' \$([\. \d]+)(,| -)', line).group(1))
    curtype = re.search(': ([^\$]*) \$', line).group(1)
    
    curante = float(0)
    if "ante" in line: #sometimes no ante 
        curante = float(re.search(' \$([\. \d]+)ante', line).group(1))
    
    #print line
    #print curbb, curante, curtype
    
    return handid, curtype, curbb, curante
    
    
def parse_table(line ,type, bb, ante):
    name = re.search('Table: (.*) Seat', line).group(1)
    table = Table(name, type, bb, ante)
    return table

def parse_player(line):
    name = re.search('- (.*) \(', line).group(1)
    stackstr = re.search('\$([\d,.]*)', line).group(1)
    stack = float(stackstr.replace(',', ''))
    seat = int(re.search('Seat (\d) -', line).group(1))
    return PlayerinHand(name, stack, seat)
    
    
def get_acttype_from_str(str):
    if 'Ante' in str:
        return ActionType.ANTE
    if 'Posts' in str:
        return ActionType.POST
    if 'Bets' in str:
        return ActionType.BET
    if 'Calls' in  str:
        return ActionType.CALL
    if 'Folds' in str:
        return ActionType.FOLD
    if 'Raises' in str:
        return ActionType.RAISE
    if 'Checks' in str:
        return ActionType.CHECK
    if 'All-In' in str:
        return ActionType.ALLIN
    if 'Timeout' in str:
        return ActionType.TIMEOUT

    
def parse_action(line, player, info):
    type = get_acttype_from_str(line)
    amount = 0
    if type != ActionType.FOLD and type != ActionType.CHECK:
        amount = float(re.search('\$([\d,.]*)', line).group(1).replace(',',''))
    #print player, info , type.name, amount
    return Action(type, info, amount, player)
    
def parse_board(str):
    boardstr = re.search('(\[.*\])', line).group(1)
    boardstr = boardstr.replace('[', '').replace(']', '')
    return boardstr
    


if __name__ == "__main__":
    tablelist = []
    file = open('datatest.txt', 'r')
    
    parserstate = ParseState.PSTAGE
    curhand = None
    curtable = None
    
    #for table
    curbb = 0
    curante = 0
    curtype = ""
    

    
    
    #state machine parser
    for line in file:
        if parserstate == ParseState.PSTAGE:
           if "Stage" in line:
                hid, curtype, curbb, curante = parse_stage(line)
                curhand = Hand(hid)
                parserstate = ParseState.PTABLE
                
        elif parserstate == ParseState.PTABLE:
            if "Table:" in line:
                table = parse_table(line, curtype, curbb, curante)
                index = findindex(tablelist, table)
                if index == -1: #not in tablelist
                    tablelist.append(table)
                    index = len(tablelist) - 1
                curtable = tablelist[index]
                parserstate = ParseState.PPLAYER
            else: 
                parserstate = ParseState.PSTAGE

        elif parserstate == ParseState.PPLAYER:
            if "Seat " in line:
                player = parse_player(line)
                curhand.players.append(player)
            else:
                parserstate = ParseState.PPREDEAL
            
        if parserstate == ParseState.PPREDEAL: #IF NOT ELIF
            if "POCKET" in line:
                parserstate = ParseState.PPREFLOP
            elif "due to player sit out" in line: 
                pass #ignore
            else:
                playername = re.search('(.*) -', line).group(1)
                player = curhand.find_player_by_name(playername)
                if "sitout" in line: #handle sitout by deleting player from hand not player action
                    curhand.players.remove(player)
                    for action in curhand.actions:#removed actions by that player
                        if action.player.name == player.name: 
                            curhand.actions.remove(action)
                            #print "removed" + " " + str(action)
                elif "returned" not in line: #ignore returned as player is deleted
                    action = parse_action(line, player, ActionInfo.PREDEAL)
                    player.stack -= action.amount
                    curhand.actions.append(action)
            
             
        elif parserstate == ParseState.PPREFLOP:
            if "FLOP" in line:
                board = parse_board(line)
                curhand.board = board
                parserstate = ParseState.PFLOP
            elif "SHOW DOWN" in line:
                parserstate = ParseState.PSHOWDOWN
            else:
                playername = re.search('(.*) -', line).group(1)
                player = curhand.find_player_by_name(playername)
                if "returned" in line: #ignore returned as it is not player action
                    amount = float(re.search('\$([\d,.]*)', line).group(1).replace(',',''))
                    player.stack += amount
                else:
                    action = parse_action(line, player, ActionInfo.PREFLOP)
                    player.stack -= action.amount
                    curhand.actions.append(action)
                
        elif parserstate == ParseState.PFLOP:
            if "TURN" in line:
                board = parse_board(line)
                curhand.board = board
                parserstate = ParseState.PTURN
            elif "SHOW DOWN" in line:
                parserstate = ParseState.PSHOWDOWN
            else:
                playername = re.search('(.*) -', line).group(1)
                player = curhand.find_player_by_name(playername)
                if "returned" in line: #ignore returned as it is not player action
                    amount = float(re.search('\$([\d,.]*)', line).group(1).replace(',',''))
                    player.stack += amount
                else:
                    action = parse_action(line, player, ActionInfo.FLOP)
                    player.stack -= action.amount
                    curhand.actions.append(action)
        elif parserstate == ParseState.PTURN:
            if "RIVER" in line:
                board = parse_board(line)
                curhand.board = board
                parserstate = ParseState.PRIVER
            elif "SHOW DOWN" in line:
                parserstate = ParseState.PSHOWDOWN
            else:
                playername = re.search('(.*) -', line).group(1)
                player = curhand.find_player_by_name(playername)
                if "returned" not in line: #ignore returned as it is not player action
                    action = parse_action(line, player, ActionInfo.TURN)
                    player.stack -= action.amount
                    curhand.actions.append(action)
        elif parserstate == ParseState.PRIVER:
            if "SHOW DOWN" in line:
                parserstate = ParseState.PSHOWDOWN
            else:
                playername = re.search('(.*) -', line).group(1)
                player = curhand.find_player_by_name(playername)
                if "returned" in line: #ignore returned as it is not player action
                    amount = float(re.search('\$([\d,.]*)', line).group(1).replace(',',''))
                    player.stack += amount
                else:
                    action = parse_action(line, player, ActionInfo.RIVER)
                    player.stack += action.amount
                    curhand.actions.append(action)
        elif parserstate == ParseState.PSHOWDOWN:
            if "SUMMARY" in line:
                parserstate = ParseState.PSUMMARY
            elif "Collects" in line: 
                playername = re.search('(.*) Col', line).group(1)
                player = curhand.find_player_by_name(playername)
                amount = float(re.search('\$([\d,.]*)', line).group(1).replace(',',''))
                player.stack += amount
        elif parserstate == ParseState.PSUMMARY:
            curhand.showdown = True
            #TODO PARSE PLAYER HANDS
            if "Pot" in line:
                curhand.totalpot =  float(re.search('\$([\d,.]*)', line).group(1).replace(',',''))
            else:
                curtable.hands.append(curhand)
                curhand = None
                parserstate = ParseState.PSTAGE
            
    #Try to find which players played the most hands and plot their winnings           
    playerlist = []
    playerwinnings = []
    
    def findplayerindex(playerlist, playername):
        index = -1
        for p in playerlist:
            index += 1
            if p == playername:
                return index 
        return -1
    
    for table in tablelist:
        for hand in table.hands:
            for player in hand.players:
                index = findplayerindex(playerlist, player.name)
                if index == -1:
                    playerlist.append(player.name)
                    index = len(playerlist) - 1
                    playerwinnings.append([])
                playerwinnings[index].append(player.stack - player.origstack)
                
    max = 0
    maxi = 0
    for i in xrange(len(playerwinnings)):
        sum = np.sum(playerwinnings[i])
        if  sum > max:
            max = sum
            maxi = i
    print max
    print playerlist[maxi]
        
    plt.plot(np.cumsum(playerwinnings[maxi]))

      
    plt.ylabel('Stack size')
    plt.xlabel('hands')
    plt.show()               

                
                
                