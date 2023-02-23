from PGNMove import *


class PGNGame:
    '''
    Describes a single chess game in PGN format.
    '''
    
    def __init__(self):  
        self.meta_data = {}
        self.moves = []

    def add_move(self, Move) -> None:
        self.moves.append(Move)

    def add_meta_data(self, key, value) -> None:
        self.meta_data[key] = value

    def get_meta_data(self) -> dict:
        return self.meta_data
    
    def get_moves(self) -> list:
        return self.moves
    
    def get_last_move(self):
        return self.moves[-1]

    def lookup_meta_data(self, key):
        return self.meta_data[key]
    
    def __str__(self):
        return str(self.meta_data)



