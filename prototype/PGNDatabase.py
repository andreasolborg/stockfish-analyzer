from PGNGame import *
from PGNMove import *
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

        game_list = []
        
        for i, game in enumerate(games, start=1):
            chessgame = PGNGame()            
            g = list(filter(lambda x: len(x) > 0, game.split('\n\n')))
            
            meta_data = g[0]
            print(meta_data)

            
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
                # print(number, white_move, white_move_comment, black_move, black_move_comment)
                chessgame.add_move(PGNMove(number, white_move, white_move_comment, black_move, black_move_comment))

            game_list.append(chessgame)

        return game_list
            
    
    def parse(self,path):
        file = open(path, 'r')
        pgn_data = file.read()

        games = list(filter(lambda x: len(x) > 0, pgn_data.split('\n\n[')))
        
        for i, game in enumerate(games, start=1):
            print(i)
            
            g = list(filter(lambda x: len(x) > 0, game.split('\n\n')))
            
            meta_data = g[0]
            moves = g[1].replace('\n', ' ')
            
            
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
    game_list = pgn.parse2("./prototype/sample.pgn")
    for game in game_list:
        print(game.get_last_move())

 
main()


    