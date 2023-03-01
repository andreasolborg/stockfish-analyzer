from PGNMove import *


class PGNGame:
    '''
    Describes a single chess game from PGN format.
    '''
    def __init__(self, meta_data, moves):  
        self.meta_data = meta_data
        self.moves = moves

    # 0 will give you the first black ply
    # 1 will give you the first white ply
    # 2 will give you the second white ply
    # etc ...
    def get_half_move(self, number):
        if number % 2 == 0:
            return self.moves[number//2].get_white_move()
        else: 
            return self.moves[number//2].get_black_move()
        
    def add_move(self, Move) -> None:
        self.moves.append(Move)

    def add_meta_data(self, key, value) -> None:
        self.meta_data[key] = value

    def get_meta_data(self) -> dict:
        return self.meta_data
    
    def get_moves(self) -> list:
        return self.moves
    
    def get_moves_without_comments(self) -> list:
        moves = []
        for move in self.moves:
            if move.get_white_move() is not None:
                moves.append(move.get_white_move())
            if move.get_black_move() is not None:
                moves.append(move.get_black_move())
        return moves
    
    
    
    def get_last_move(self):
        return self.moves[-1]
    
    def get_move(self, move_number):
        return self.moves[move_number]
    
    def get_result(self):
        return self.meta_data["Result"]
    

    def lookup_meta_data(self, key):
        return self.meta_data[key]
    
    def __str__(self):
        return str(self.meta_data)



