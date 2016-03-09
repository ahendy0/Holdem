from enum import Enum
import re
import copy
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datastruct import *
import os
import sys
import traceback
    
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
    #print name, stack
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
        player.stack -= amount
    #print player, info.name , type.name, amount, player.stack
    return Action(type, info, amount, player)
    
def parse_action_line(line, curhand, info):
    playername = re.search('(.*) -', line).group(1)
    player = curhand.find_player_by_name(playername)
    if "returned" in line: #ignore returned as it is not player action
        amount = float(re.search('\$([\d,.]*)', line).group(1).replace(',',''))
        player.stack += amount
    else:
        action = parse_action(line, player, info)
        curhand.actions.append(action)
    
def parse_board(line, hand):
    boardstr = re.search('(\[.*\])', line).group(1)
    boardstr = boardstr.replace('[', '').replace(']', '')
    hand.board = Board(boardstr)
    
def parse_collect(line, curhand):
    playername = re.search('(.*) Col', line).group(1)
    player = curhand.find_player_by_name(playername)
    amount = float(re.search('\$([\d,.]*)', line).group(1).replace(',',''))
    player.stack += amount
    curhand.winners.append(player)
    #print playername, "collects", amount
    
def parse_cards(line, curhand):
    name = re.search('(.*) - Shows', line).group(1)
    player = curhand.find_player_by_name(name)
    handstr = re.search('(\[.*\])', line).group(1)
    handstr = handstr.replace('[', '').replace(']', '')
    player.hand = handstr
   
def hands_in_list(tablelist):
    numhands = 0
    for table in tablelist:
        numhands += table.numhands()
    return numhands

def parse_file(file):
    tablelist = []
    counter = 0
    
    parserstate = ParseState.PSTAGE
    curhand = None
    curtable = None
    
    #for table
    curbb = 0
    curante = 0
    curtype = ""
    
   
    #state machine parser
    for line in file:
        try:#capturing an error will skip the hand
            if parserstate == ParseState.PSTAGE:
               if "Stage" in line:
                    counter += 1
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
                elif "due to player sit out" or "due to player leave" in line: 
                    pass #ignore these lines
                else:
                    playername = re.search('(.*) -', line).group(1)
                    player = curhand.find_player_by_name(playername)
                    if "sitout" in line: #handle sitout/leave by deleting player from hand not player action
                        curhand.players.remove(player)
                        for action in curhand.actions:#removed actions by that player
                            if action.player.name == player.name: 
                                curhand.actions.remove(action)
                
                    elif "returned" not in line: #ignore returned as player is deleted
                        action = parse_action(line, player, ActionInfo.PREDEAL)
                        curhand.actions.append(action)
                                #print "removed" + " " + str(action)
                 
            elif parserstate == ParseState.PPREFLOP:
                if "FLOP" in line:
                    parse_board(line, curhand)
                    parserstate = ParseState.PFLOP
                elif "SHOW DOWN" in line:
                    parserstate = ParseState.PSHOWDOWN
                else:
                    parse_action_line(line, curhand, ActionInfo.PREFLOP)
            elif parserstate == ParseState.PFLOP:
                if "TURN" in line:
                    parse_board(line, curhand)
                    parserstate = ParseState.PTURN
                elif "SHOW DOWN" in line:
                    parserstate = ParseState.PSHOWDOWN
                else:
                    parse_action_line(line, curhand, ActionInfo.FLOP)
            elif parserstate == ParseState.PTURN:
                if "RIVER" in line:
                    parse_board(line, curhand)
                    parserstate = ParseState.PRIVER
                elif "SHOW DOWN" in line:
                    parserstate = ParseState.PSHOWDOWN
                else:
                    parse_action_line(line, curhand, ActionInfo.TURN)
            elif parserstate == ParseState.PRIVER:
                if "SHOW DOWN" in line:
                    parserstate = ParseState.PSHOWDOWN
                else:
                    parse_action_line(line, curhand, ActionInfo.RIVER)
                    
            elif parserstate == ParseState.PSHOWDOWN:
                if "SUMMARY" in line:
                    parserstate = ParseState.PSUMMARY
                elif "Shows" in line:
                    parse_cards(line, curhand)
                elif "Collects" in line:
                    parse_collect(line, curhand)
                    
            elif parserstate == ParseState.PSUMMARY:
                curhand.showdown = True
                if "Pot" in line:
                    curhand.totalpot =  float(re.search('\$([\d,.]*)', line).group(1).replace(',',''))
                else:
                    curtable.hands.append(curhand)
                    curhand = None
                    parserstate = ParseState.PSTAGE
                          
        except Exception as e:
            parserstate = ParseState.PSTAGE
            traceback.print_exc()
            print line 
            print "Skipping hand"
                
    print "Parsed", counter, "hands"           
    return tablelist
                
    def tester(tablelist):
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
        print playerwinnings[maxi]
          
        plt.ylabel('Stack size')
        plt.xlabel('hands')
        plt.show()               


if __name__ == "__main__":

    #if you want to try parsing the data, create a folder called Holdem/data. unzip all the files from http://web.archive.org/web/20110205042259/http://www.outflopped.com/questions/286/obfuscated-datamined-hand-histories into that folder and run.
    #currently this version only works on ABS logs.
    tablelist = []
    for folder in os.listdir('./data/'):
        for logfile in  os.listdir('./data/' + folder):
            print "Parsing file:" + './data/' + folder + '/' + logfile
            start_time = datetime.datetime.now()
            file = open('./data/' + folder + '/' + logfile, 'r')
            list = parse_file(file)
            tablelist.extend(list)
            end_time = datetime.datetime.now()
            print "time taken: ", end_time - start_time            
    print "Parsed" , hands_in_list(tablelist), "total hands"
                
            
 
                
                
                