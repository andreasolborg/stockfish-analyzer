from PGNGame import *
from PGNMove import *
from PGNPly import * 
import re

class PGNDatabase:
    '''
    Encapsultaes all games TODO, skriv bedre
    '''
    
    def __init__(self):  
        pass

    
  
        
    def parse(self,path):
        file = open(path, 'r')
        pgn_data = file.read()
        
        games = list(filter(lambda x: len(x) > 0, pgn_data.split('\n\n[')))
        
        for i, game in enumerate(games, start=1):
            print(i)
            
            g = list(filter(lambda x: len(x) > 0, game.split('\n\n')))
            
            meta_data = g[0]
            moves = g[1]
            
            
            moves = moves.replace('\n', '')
            
            moves = re.sub(r'\d+\.\.\.|\d+\.', '', moves)
            moves = re.sub(r'(\)|\(|\$\d+)', r' \1 ', moves) 
            
            test = list(filter(lambda x: x, re.split(r'({[\w\W]*?})|\s', moves)))[:-1]
            
 
            for e in test:
                print(e)
              
            #print(moves)
  
            print(test)
            
            

def main():
    
    pgn = PGNDatabase()
    pgn.parse("./sample.pgn")
 
main()


    