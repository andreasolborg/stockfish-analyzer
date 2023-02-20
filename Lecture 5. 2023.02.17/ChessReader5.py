# 1. Imported Modules
# -------------------

import sys
import re

# 2. Main
# -------

def ImportChessDataBase(filePath):
    inputFile = open(filePath, "r")
    count = ReadChessDataBase(inputFile)
    inputFile.close()

def ReadLine(inputFile):
    line = inputFile.readline()
    if line=="":
        return None
    return line.rstrip()
    
def ReadChessDataBase(inputFile):
    step = 1
    line = ReadLine(inputFile)
    while True:
        if step==1: # Read a game
            if line==None:
                break
            else:
                step = 2
        elif step==2: # Read meta-data
            if re.match("\[", line):
                match = re.search("\[([a-zA-Z]+)", line)
                if match:
                    key = match.group(1)
                match = re.search(r'"([^"]+)"', line)
                if match:
                    value = match.group(1)
                print(key + " " + value)
                line = ReadLine(inputFile)
                if line==None:
                    break
            else:
                step = 3
        elif step==3: # read moves
            line = ReadLine(inputFile)
            if line==None:
                break
            elif re.match("\[", line):
                step = 2

      

ImportChessDataBase("DataBases/Stockfish_15_64-bit.commented.[2600].pgn")
