#from PNGGame import *
#from PNGMove import *
import re

class PGNDatabase:
    '''
    Encapsultaes all games TODO, skriv bedre
    '''
    
    def __init__(self):  
        pass

    
    def parse2(self,path):
        file = open(path, 'r')
        pgn_data = file.read()

        games = list(filter(lambda x: len(x) > 0, pgn_data.split('\n\n[')))
        
        for i, game in enumerate(games, start=1):
            print(i)
            
            g = list(filter(lambda x: len(x) > 0, game.split('\n\n')))
            
            meta_data = g[0]
            moves = g[1].replace('\n', ' ')
            
            pattern = r'\d+\.\s[\S\s]+?(?=\d+\.\s|\Z)' # Matches all moves
            matches = re.findall(pattern, moves)
            for match in matches:
                pattern = re.compile(r"(\w+|\{[\w\s\+\-\.\/\(\)]+\})")
                result = pattern.findall(match)
                number = result[0]
                white_move = result[1]
                white_move_comment = result[2]
                black_move = result[3]
                black_move_comment = result[4]
                print(number, white_move, white_move_comment, black_move, black_move_comment)     

    
    def parse(self,path):
        file = open(path, 'r')
        pgn_data = file.read()

        games = list(filter(lambda x: len(x) > 0, pgn_data.split('\n\n[')))
        
        for i, game in enumerate(games, start=1):
            g = list(filter(lambda x: len(x) > 0, game.split('\n\n')))
            
            meta_data = g[0]
            moves = g[1].replace('\n', ' ')
            
            
            moves = moves.replace('\n', '')
            
            moves = re.sub(r'\d+\.\.\.|\d+\.', '', moves)
            moves = re.sub(r'(\)|\(|\$\d+)', r' \1 ', moves) 
            
            test = list(filter(lambda x: x, re.split(r'({[\w\W]*?})|\s', moves)))[:-1]
            
            moves = []
            
            for i in range(0, len(test), 4)
                white_move = PNGPly()
                black_move = PNGPly()
                
                move = PNGMove((i+1)/4, white_move, black_move)
                moves.append(move)
            
                
            #print(moves)
  
            print(test)
            
            

def main():
    
    pgn = PGNDatabase()
    pgn.parse("./prototype/sample.pgn")
 
main()


    