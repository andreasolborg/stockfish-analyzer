class PGNMove:  
    '''
    Describes a single chess move from PGN format.
    '''
    def __init__(self, number, white_move, white_comment, black_move, black_comment):
        self.number = number
        self.white_move = white_move
        self.white_comment = white_comment
        self.black_move = black_move
        self.black_comment = black_comment

    def get_number(self):
        return self.number
    
    def get_white_move(self):
        return self.white_move
    
    def get_white_comment(self):
        return self.white_comment
    
    def get_black_move(self):
        return self.black_move

    def get_black_comment(self):
        return self.black_comment
        
    def __str__(self):     
        number = ""
        white_move = ""
        white_comment = ""
        black_move = ""
        black_comment = ""
        
        if self.number is not None:
            number = self.number
            
        if self.white_move is not None:
            white_move = self.white_move
            
        if self.white_comment is not None:
            white_comment = self.white_comment
            
        if self.black_move is not None:
            black_move = self.black_move
            
        if self.black_comment is not None:
            black_comment = self.black_comment
        
        return number + " " + white_move + " " + white_comment  + " " + black_move + " " + black_comment

    

    def main():
        pass


if __name__ == '__main__':
    main()

    
        