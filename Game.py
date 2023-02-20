import re


class Game:
    def __init__(self):
        self.meta_data = {}
        self.moves = []
    
    def add_move(self, move) -> None:
        self.moves.append(move)

    def add_meta_data(self, key, value) -> None:
        self.meta_data[key] = value
    
    def get_moves(self) -> list:
        return self.moves
    
    def get_last_move(self):
        return self.moves[-1]
    
    def export_to_file(self, filename):
    
        return 

@staticmethod
def import_from_file(filename):
    game = Game()
    step = 1
    file = open(filename, "r")
    line = file.readline().rstrip()
    if line == "":
        return None
    while True:
        if step==1: # Read a game
            if line==None: # End of file
                break # Exit the loop
            else:
                step = 2
        elif step==2: # Read meta-data
            if re.match("\[", line):
                match = re.search("\[([a-zA-Z]+)", line)
                if match:
                    key = match.group(1) # key = Event, White, Black, etc.
                match = re.search(r'"([^"]+)"', line)
                if match:
                    value = match.group(1) # value = "World Championship 2018"
                game.add_meta_data(key, value)
                line = file.readline().rstrip()
                if line==None:
                    break
            else:
                step = 3
        elif step==3: # read moves
            if line==None:
                break
            line = file.readline().rstrip()
            # Split at each move indicated by "1., 2., 3., etc."
            moves = re.split("\d+\.", line) 
            print(moves)
            for move in moves:
                game.add_move(move)
            if re.match("\[", line):
                step = 2
                

    file.close()
    return game




def main():
    game = import_from_file("./2005-12.commented.[534].pgn")
    print(game.get_moves())
main()
