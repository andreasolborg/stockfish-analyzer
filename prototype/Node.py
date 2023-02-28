class Node:
    '''
    A class representing a node in the chess opening tree.
    '''
    def __init__(self, moves_token):
        '''
        Params:
            color: Either the character 'w' for white or 'b' for black
            games: A list with instances of PGNGame
        '''
        
        self.moves_token = moves_token   
        self.children = children # list of all moves done from this

    
    def add_child(self):
        pass
    
    