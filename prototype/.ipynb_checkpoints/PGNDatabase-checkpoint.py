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
    
    def get_stockfish_draws(self, list_of_drawed_games):
        stockfish_draws_as_white = [game for game in list_of_drawed_games if game.lookup_meta_data('White') == 'Stockfish 15 64-bit']
        stockfish_draws_as_black = [game for game in list_of_drawed_games if game.lookup_meta_data('Black') == 'Stockfish 15 64-bit']
        return stockfish_draws_as_white, stockfish_draws_as_black

    def get_stockfish_wins(self, list_of_games):
        stockfish_wins_as_white = [game for game in list_of_games if game.lookup_meta_data('White') == 'Stockfish 15 64-bit' and game.lookup_meta_data('Result') == '1-0']
        stockfish_wins_as_black = [game for game in list_of_games if game.lookup_meta_data('Black') == 'Stockfish 15 64-bit' and game.lookup_meta_data('Result') == '0-1']
        return stockfish_wins_as_white, stockfish_wins_as_black

    def get_stockfish_losses(self, list_of_games):
        stockfish_losses_as_white = [game for game in list_of_games if game.lookup_meta_data('White') == 'Stockfish 15 64-bit' and game.lookup_meta_data('Result') == '0-1']
        stockfish_losses_as_black = [game for game in list_of_games if game.lookup_meta_data('Black') == 'Stockfish 15 64-bit' and game.lookup_meta_data('Result') == '1-0']
        return stockfish_losses_as_white, stockfish_losses_as_black


    def plot_plycount_distribution(self, plycount_distribution):
        x = []
        y = []
        for key, value in plycount_distribution:
            x.append(key)
            y.append(value)
        plt.bar(x, y)
        plt.show()

    def compose(self):
        # TODO
        # fix correct linebreak in the moves; http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#c4.3
        # fix parse function so it collects the score after all the moves correct
        
        pgn_data = ""
        for game in self.games:
            meta_data = ""
            for key, value in game.get_meta_data().items():
                line = "[" + str(key) + " \"" + str(value) + "\"]"
                meta_data = meta_data + line + "\n"
            
            pgn_data += meta_data + "\n"

            moves = ""
            for move in game.get_moves(): 
                moves += move.get_number() + ". "
                moves += move.get_white_move() + " "
                
                # Comment might not exist
                if move.get_white_comment() is not None:
                    moves += move.get_white_comment() + " "
                
                moves += move.get_black_move() + " "
                
                # Comment might not exist
                if move.get_black_comment() is not None:
                    moves += move.get_black_comment() + " "
         
            pgn_data += moves + "\n\n"
        
        pgn_file = open("test.pgn","w")
        pgn_file.write(pgn_data)
        pgn_file.close()
            
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
            
def test():
    start_time = time.time()
    pgn = PGNDatabase("./sample.pgn")
    
    # manual testing
    for i, g in enumerate(pgn.get_games()):
        pass
        #print("-----------------" + str(i) + "-----------------")
        #print(g.meta_data)
        #print("")
        for m in g.moves:
            pass
            #print(m)
    
    pgn.compose()
    
    print(f"Time: {time.time() - start_time}")

test()
            
            

def main():
    start_time = time.time()

    # pgn = PGNDatabase("./prototype/sample.pgn")
    # pgn = PGNDatabase("./prototype/test.pgn")
    # pgn = PGNDatabase("./prototype/bigger_sample.pgn")


    pgn = PGNDatabase("./Stockfish_15_64-bit.commented.[2600].pgn")
    # game_list = pgn.parse2("./Stockfish_15_64-bit.commented.[2600].pgn")
    print(f"Time: {time.time() - start_time}")

    
    # print(f"White wins: {len(pgn.white_wins)}")
    # print(f"Black wins: {len(pgn.black_wins)}")
    # print(f"Draws: {len(pgn.draws)}")

    # print("Getting plycount distribution")
    # plycount_distribution = pgn.get_plycount_distribution()
    # print("Sorting plycount distribution")
    # sorted_plycount_distribution = pgn.sort_plycount_distribution_by_key(plycount_distribution)
    # print(sorted_plycount_distribution)
    # print("Plotting plycount distribution")
    # pgn.plot_plycount_distribution(sorted_plycount_distribution)
    start_time = time.time()
    print("Getting games")
    list_of_games = pgn.get_games()
    list_of_draws = pgn.get_draws()
    print("Getting stockfish wins")
    stockfish_wins_as_white, stockfish_wins_as_black = pgn.get_stockfish_wins(list_of_games)
    print(f"Stockfish wins as white: {len(stockfish_wins_as_white)}")
    print(f"Stockfish wins as black: {len(stockfish_wins_as_black)}")

    print("Getting stockfish losses")
    stockfish_losses_as_white, stockfish_losses_as_black = pgn.get_stockfish_losses(list_of_games)
    print(f"Stockfish losses as white: {len(stockfish_losses_as_white)}")
    print(f"Stockfish losses as black: {len(stockfish_losses_as_black)}")

    print("Getting stockfish draws")
    stockfish_draws_as_white, stockfish_draws_as_black = pgn.get_stockfish_draws(list_of_draws)
    print(f"Stockfish draws as white: {len(stockfish_draws_as_white)}")
    print(f"Stockfish draws as black: {len(stockfish_draws_as_black)}")



    print(f"Time: {time.time() - start_time}")
        

#main()


    