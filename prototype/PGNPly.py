class PGNPly:  
    '''
    A Ply is a half a move in a game, either white or blacks side of the move
    '''

    def __init__(self, move, comment):
        self.move = move
        self.comment = comment

    def get_move(self):
        return self.move

    def get_comment(self):
        return self.comment



    def __str__(self):
        return self.move + " " + self.comment