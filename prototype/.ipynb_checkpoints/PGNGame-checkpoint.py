from PGNMove import *


class PGNGame:
    '''
    Describes a single chess game in PGN format.
    '''
    
    def __init__(self):  
        self.meta_data = {}
        self.moves = []

    def add_move(self, move) -> None:
        self.moves.append(move)

    def add_meta_data(self, key, value) -> None:
        self.meta_data[key] = value
    
    def get_moves(self) -> list:
        return self.moves
    
    def get_last_move(self):
        return self.moves[-1]

    

