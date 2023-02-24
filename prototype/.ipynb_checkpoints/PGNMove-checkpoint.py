class PGNMove:  
    '''
    Describes a single chess move in PGN format.
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
        
    #def __str__(self):
    #    return str(self.number) + " " + self.white_move + " " + self.white_comment  + " " + self.black_move + " " 

    

    def main():
        pass


if __name__ == '__main__':
    main()

    
        