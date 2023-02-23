from PGNGame import *
from PGNMove import *
from PGNPly import *
import re
import time

import matplotlib.pyplot as plt

class PGNDatabase:
    '''
    Encapsultaes all games TODO, skriv bedre
    '''
    
    def __init__(self, path):
        self.games = self.parse(path)  
        self.white_wins = self.get_white_wins()
        self.black_wins = self.get_black_wins()
        self.draws = self.get_draws()

    def get_games(self):
        return self.games
    
    def get_white_wins(self):
        white_wins = []
        for game in self.games:
            if game.lookup_meta_data('Result') == '1-0':
                white_wins.append(game)
        return white_wins
    
    def get_black_wins(self):
        black_wins = []
        for game in self.games:
            if game.lookup_meta_data('Result') == '0-1':
                black_wins.append(game)
        return black_wins
    
    def get_draws(self):
        draws = []
        for game in self.games:
            if game.lookup_meta_data('Result') == '1/2-1/2':
                draws.append(game)
        return draws

    def get_plycount_distribution(self):
        plycount_distribution = {}
        for game in self.games:
            plycount = int(game.lookup_meta_data('PlyCount'))
            if plycount in plycount_distribution:
                plycount_distribution[plycount] += 1
            else:
                plycount_distribution[plycount] = 1
        return plycount_distribution

    def sort_plycount_distribution_by_key(self, plycount_distribution):
        return sorted(plycount_distribution.items(), key=lambda x: int(x[0]))

    def plot_plycount_distribution(self, plycount_distribution):
        x = []
        y = []
        for key, value in plycount_distribution:
            x.append(key)
            y.append(value)
        plt.bar(x, y)
        plt.show()

    def scatter_plot_plycount_distribution(self, plycount_distribution):
        x = []
        y = []
        for key, value in plycount_distribution:
            x.append(key)
            y.append(value)
        plt.scatter(x, y)
        plt.show()


        
            
    def parse(self,path):
        file = open(path, 'r')
        pgn_data = file.read()
        games = list(filter(lambda x: len(x) > 0, pgn_data.split('\n\n[')))

        game_list = []
        
        for game in games:
            chessgame = PGNGame()            
            g = list(filter(lambda x: len(x) > 0, game.split('\n\n'))) # Split on empty lines
            meta_data = g[0]
            meta_data = meta_data.split('\n')
            meta_data = list(filter(lambda x: len(x) > 0, meta_data))                       # Remove empty strings
            # Remove quatation marks
            meta_data = list(map(lambda x: x.replace('[', '').replace(']', ''), meta_data)) # Remove brackets
            meta_data = list(map(lambda x: x.split(' ', 1), meta_data))                     # Split on first space
            meta_data = list(map(lambda x: (x[0], x[1].replace('"', '')), meta_data))       # Remove quotes
            meta_data = dict(meta_data)
            for key, value in meta_data.items():
                chessgame.add_meta_data(key, value)
            
            moves = g[1].replace('\n', ' ')
            pattern = r'\d+\.\s[\S\s]+?(?=\d+\.\s|\Z)' # Matches all moves
            # Define a regular expression to match the input string
            matches = re.findall(pattern, moves)
            for match in matches:
                pattern = r'(\d+)\.?\s*(\S+)\s*({.*?})?\s*(\S+)?\s*({.*?})?'
                result = re.match(pattern, match)
                if result:
                    number = result.group(1)
                    white_move = result.group(2)
                    white_move_comment = result.group(3)
                    black_move = result.group(4)
                    black_move_comment = result.group(5)
                    chessgame.add_move(PGNMove(number, white_move, white_move_comment, black_move, black_move_comment))
                else:
                    print("No match---------------------")
            game_list.append(chessgame)

        return game_list
            
    
    def parse2(self,path):
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
            
            for i in range(0, len(test), 4):
                white_move = PNGPly()
                black_move = PNGPly()
                
                move = PNGMove((i+1)/4, white_move, black_move)
                moves.append(move)
            
                
            #print(moves)
  
            print(test)
            
            

def main():
    # pgn = PGNDatabase("./prototype/sample.pgn")
    pgn = PGNDatabase("./prototype/test.pgn")
    # pgn = PGNDatabase("./prototype/bigger_sample.pgn")


    # pgn = PGNDatabase("./Stockfish_15_64-bit.commented.[2600].pgn")
    # game_list = pgn.parse2("./Stockfish_15_64-bit.commented.[2600].pgn")
    
    # print(f"White wins: {len(pgn.white_wins)}")
    # print(f"Black wins: {len(pgn.black_wins)}")
    # print(f"Draws: {len(pgn.draws)}")

    print("Getting plycount distribution")
    plycount_distribution = pgn.get_plycount_distribution()
    print("Sorting plycount distribution")
    sorted_plycount_distribution = pgn.sort_plycount_distribution_by_key(plycount_distribution)
    print(sorted_plycount_distribution)
    print("Plotting plycount distribution")
    pgn.plot_plycount_distribution(sorted_plycount_distribution)

    print("Scatter plotting plycount distribution")
    pgn.scatter_plot_plycount_distribution(sorted_plycount_distribution)



    print(f"Time: {time.time() - start_time}")
        

start_time = time.time()
main()


    