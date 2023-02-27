from PGNGame import *
from PGNMove import *
import re
import time

import os
from docx import Document
from docx.shared import Inches

import numpy as np
import matplotlib.pyplot as plt

from openpyxl import Workbook
from openpyxl import load_workbook

class PGNDatabase:
    '''
    Encapsulate all games parsed from a PGN file.
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
    
    def get_games_where_stockfish_is_white(self):
        stockfish_white = []
        for game in self.games:
            if game.lookup_meta_data('White') == 'Stockfish 15 64-bit':
                stockfish_white.append(game)
        return stockfish_white
    
    def get_games_where_stockfish_is_black(self):
        stockfish_black = []
        for game in self.games:
            if game.lookup_meta_data('Black') == 'Stockfish 15 64-bit':
                stockfish_black.append(game)
        return stockfish_black


    ##### TASK 8 ########
    def get_standard_deviation_of_moves(self):
        amount_of_moves = []
        for game in self.games:
            amount_of_moves.append(len(game.get_moves()))
        return np.std(amount_of_moves)

    def get_mean_number_of_moves(self):
        amount_of_moves = []
        for game in self.games:
            amount_of_moves.append(len(game.get_moves()))
        return np.mean(amount_of_moves)

    def get_move_count_distribution(self, list_of_games):
        move_count_distribution = {}
        for game in list_of_games:
            move_count = len(game.get_moves())
            if move_count in move_count_distribution:
                move_count_distribution[move_count] += 1
            else:
                move_count_distribution[move_count] = 1
        return move_count_distribution

    def get_plycount_distribution(self):
        plycount_distribution = {}
        for game in self.games:
            plycount = int(game.lookup_meta_data('PlyCount'))
            if plycount in plycount_distribution:
                plycount_distribution[plycount] += 1
            else:
                plycount_distribution[plycount] = 1
        return plycount_distribution

    def sort_dict(self, dict):
        return sorted(dict.items(), key=lambda x: x[0])
    
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
        #Clear plot
        plt.clf()
        x = []
        y = []
        for key, value in plycount_distribution:
            x.append(key)
            y.append(value)
        plt.plot(x, y)
        plt.savefig('plycount_distribution.png')
        
        
    def plot_move_count_distribution(self, move_count_distribution):
        #Clear plot
        plt.clf()
        x = []
        y = []
        for key, value in move_count_distribution:
            x.append(key)
            y.append(value)
        plt.plot(x, y)
        plt.xlabel('Number of moves')
        plt.ylabel('Number of games')
        plt.fill_between(x, y, color='blue', alpha=0.5)

        plt.savefig('move_count_distribution.png')
    
    def compose_to_excel(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'pgn_as_excel'
        
        i = 1
        for game in self.games:
         
            for key, value in game.get_meta_data().items():
                worksheet.cell(row=i, column=1, value=key)
                worksheet.cell(row=i, column=2, value=value)
                i += 1
            i += 1  
            
            for move in game.get_moves():
                worksheet.cell(row=i, column=1, value=move.get_number())
                worksheet.cell(row=i, column=2, value=move.get_white_move())
                worksheet.cell(row=i, column=3, value=move.get_white_comment())
                worksheet.cell(row=i, column=4, value=move.get_black_move())
                worksheet.cell(row=i, column=5, value=move.get_black_comment())
                i += 1
                
            i += 1
        workbook.save(filename='pgn_as_excel.xlsx')
    
    def parse_from_excel(self):
        workbook = load_workbook(filename='pgn_as_excel.xlsx')
        worksheet = workbook['pgn_as_excel']

        new_game=False
        phase = 0
        
        meta_data = {}
        moves = []
        for row in worksheet.iter_rows(min_row=1, values_only=True):
            
            if phase == 0:
                if row[0] is None:
                    phase = 1
                    continue
                
                meta_data[row[0]] = row[1]
                
            if phase == 1:
                if row[0] is None:
                    phase = 2
                    continue
                
                number = row[0]
                white_move = row[1]
                white_move_comment = row[2]
                black_move = row[3]
                black_move_comment = row[4]
                
                moves.append(PGNMove(number, white_move, white_move_comment, black_move, black_move_comment))
                
            if phase == 2:
                self.games.append(PGNGame(meta_data, moves))
                meta_data = {}
                moves = []
                phase = 0
                continue
        
    def compose(self):
        # TODO fix correct linebreak in the moves
        
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
                
                if move.get_white_move() is not None:
                    moves += move.get_white_move() + " "
               
                if move.get_white_comment() is not None:
                    moves += move.get_white_comment() + " "
               
                if move.get_black_move() is not None:
                    moves += move.get_black_move() + " "
             
                if move.get_black_comment() is not None:
                    moves += move.get_black_comment() + " "
            
            score = game.get_meta_data()["Result"]
            pgn_data += moves + score + "\n\n"
        
        pgn_file = open("test.pgn","w")
        pgn_file.write(pgn_data)
        pgn_file.close()
    
    def parse(self,path):
        file = open(path, 'r')
        pgn_data = file.read()
        games = list(filter(lambda x: len(x) > 0, pgn_data.split('\n\n[')))
        
        game_list = []
        
        for game in games:
            chessgame = PGNGame({}, [])            
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
            
            # remove score at the end of the moves
            moves = re.sub(r'\s(1\/2-1\/2|1-0|0-1)$', '', moves)
            
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
    print(pgn.games)
    for i, g in enumerate(pgn.get_games()):
        pass
        print("-----------------" + str(i) + "-----------------")
        print(g.meta_data)
        print("")
        for m in g.moves:
            pass
            print(m)
    
    
    pgn.games = []
    
    print(pgn.games)
    

    
    #pgn.compose_to_excel()
    pgn.parse_from_excel()

    for i, g in enumerate(pgn.get_games()):
        pass
        print("-----------------" + str(i) + "-----------------")
        print(g.meta_data)
        print("")
        for m in g.moves:
            pass
            print(m)
    
    print(f"Time: {time.time() - start_time}")

test()
            
def main():
    start_time = time.time()

    # pgn = PGNDatabase("./prototype/sample.pgn")
    # pgn = PGNDatabase("./prototype/test.pgn")
    # pgn = PGNDatabase("./prototype/bigger_sample.pgn")

    pgn = PGNDatabase("./sample.pgn")

    list_of_drawed_games = pgn.get_draws()
    list_of_games = pgn.get_games()
    
    list_of_games_where_stockfish_is_white = pgn.get_games_where_stockfish_is_white()

    move_count_distribution = pgn.get_move_count_distribution(list_of_games)
    sorted_dict = pgn.sort_dict(move_count_distribution)
    print(sorted_dict)
    pgn.plot_move_count_distribution(sorted_dict)

    plycount_distribution = pgn.get_plycount_distribution()
    sorted_dict = pgn.sort_dict(plycount_distribution)
    pgn.plot_plycount_distribution(sorted_dict)


    print(f"Time: {time.time() - start_time}")
        

if __name__ == "__main__":
    #main()
    pass
    

    