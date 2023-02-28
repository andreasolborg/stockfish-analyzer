class Node:
    '''
    A class representing a node in the chess opening tree.
    '''
    def __init__(self, color, children, meta_data):
        '''
        Params:
            color: Either the character 'w' for white or 'b' for black
            games: A list with instances of PGNGame
        '''
        self.move # string of move, acts like as ID
        self.degree # move number
        self.color = color # w/b
        self.children = children # list of all moves done from this
        self.meta_data = meta_data 
    
    def add_child(self):
        pass
    
    