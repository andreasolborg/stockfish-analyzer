#from PNGGame import *
#from PNGMove import *

class PGNDatabase:
    '''
    Encapsultaes all games TODO, skriv bedre
    '''
    
    def __init__(self):  
        pass

    
    def parse(self,path):
        file = open(path, 'r')
        pgn_data = file.read()
        
        games = list(filter(lambda x: len(x) > 0, pgn_data.split('\n\n[')))
        
        for i, game in enumerate(games, start=1):
            print(i)
            
            g = list(filter(lambda x: len(x) > 0, game.split('\n\n')))
            
            meta_data = g[0]
            moves = g[1]
            
            print repr(moves)
  
            print("dsffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
            
            

def main():
    
    pgn = PGNDatabase()
    pgn.parse("./sample.pgn")
 
main()


    