class PGNMove:  
    '''
    Describes a single chess move in PGN format.
    '''
    
    def __init__(self, number, white, white_comment, black, black_comment):
        self.number = number
        self.white = white
        self.white_comment = white_comment
        self.black = black
        self.black_comment = black_comment

    def get_number(self):
        return self.number
    
    def get_white(self):
        return self.white
    
    def get_white_comment(self):
        return self.white_comment
    
    def get_black_comment(self):
        return self.black_comment

    def get_black(self):
        return self.black
        
    def __str__(self):
        return self.number + " " + self.white + " " + self.black

    

    def main():
        pass


if __name__ == '__main__':
    main()

    
        