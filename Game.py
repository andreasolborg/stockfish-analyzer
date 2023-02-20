
class Game:
    def _init__(self):
        self.moves = []
    
    def add_move(self, move) -> None:
        self.moves.append(move)
    
    def get_moves(self) -> list:
        return self.moves
    

    def get_last_move(self) -> str: 
        return self.moves[-1]
    
    def export_to_file(self, filename):
        with open(filename, 'w') as f:
            for move in self.moves:
                f.write(move + '\n')
    
    @staticmethod
    def import_from_file(filename):
        game = Game()
        with open(filename, 'r') as f:
            for line in f:
                move = line.strip()
                game.add_move(move)
        return game


def main():
    print("HEI")
    return


main()
