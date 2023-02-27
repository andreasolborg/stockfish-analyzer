class Tree:
    '''
    TODO: write class desc
    '''
    def __init__(self, color, games):
        '''
        Params
            color: Either the character 'w' for white or 'b' for black
            games: A list with instances of PGNGame
        '''
        self.color = color
        self.games = games
        
    