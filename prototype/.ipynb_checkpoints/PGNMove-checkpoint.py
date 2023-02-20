class PGNMove:  
    '''
    Describes a single chess move in PGN format.
    '''
    
    def __init__(self, number, white, black):
        self.number = number
        self.white = white
        self.black = black

    def get_number(self):
        return self.number

    def get_white(self):
        return self.white_move

    def get_black(self):
        return self.white_comment


    def __str__(self):
        return self.number + " " + self.white + " " + self.black

    

    
        