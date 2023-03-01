from PGNDatabase import PGNDatabase
import os

class TreeNode:
    def __init__(self, move, move_number):
        self.move = move
        self.move_number = move_number
        self.parent = None
        self.color = None
        self.results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}
        self.children = []
        
        self.set_color(move_number)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_move(self):
        return self.move

    def get_result(self):
        return self.results

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def __str__(self):
        return str(self.move)
    
    def increment_result(self, result):
        self.results[result] += 1
        
    def set_color(self, number):
        if number != None:
            if number % 2 == 0:
                self.color = "white"
            else:
                self.color = "grey"
        else:
            self.color = "white"
    
    def get_color(self):
        return self.color
    
    def get_move_number(self):
        return self.move_number
        
class OpeningTree:
    
    def __init__(self, list_of_games):
        self.list_of_games = list_of_games
        self.root = TreeNode(None, None)
        self.create_tree()

    def create_tree(self):
        for game in self.list_of_games:
            
            result = game.get_result()
            moves = game.get_moves_without_comments()
            
            current_node = self.root
            move_number = 0
            
            for move in moves:
                child_node = None
     
                for existing_child in current_node.get_children(): # check if child already exists
                    if existing_child.get_move() == move: # if child exists, increment result
                        child_node = existing_child # and
                        child_node.increment_result(result)
                        break # break out of loop
                        
                if child_node is None: # if child does not exist, create it 
                    child_node = TreeNode(move, move_number) # create child
                    child_node.increment_result(result) # and increment result
                    current_node.add_child(child_node) # add child to parent
                
                current_node = child_node
                move_number += 1

    def print_tree(self, depth, filename):
        with open("./graphs/{}.dot".format(filename), "w") as dot_file:
            dot_file.write("digraph G {\n")
            self.print_node(self.root, depth, 0, dot_file)
            dot_file.write("}\n")
        # os.system("dot -Tpng ./graphs/{}.dot -o ./graphs/{}.png".format(filename, filename))

    def print_node(self, node, depth, current_depth, dot_file):
        if current_depth < depth:
            for child in node.get_children():
                dot_file.write('{} [label="{}" fillcolor="{}", style="filled"] \n'.format(str(id(node)), node.get_result(), node.get_color()))
                dot_file.write('{} -> {} [label="{}"]\n'.format(str(id(node)), str(id(child)), child.get_move()))
                self.print_node(child, depth, current_depth + 1, dot_file)
        else: # leaf node
            dot_file.write('{} [label="{}" fillcolor="{}", style="filled"] \n'.format(str(id(node)), node.get_result(), node.get_color()))
            
    
def save_tree_to_file(tree, depth, filename):
    if os.path.exists("./graphs/{}.dot".format(filename)):
        os.remove("./graphs/{}.dot".format(filename))
    if os.path.exists("./graphs/{}.png".format(filename)):
        os.remove("./graphs/{}.png".format(filename))
    tree.print_tree(depth, filename)
    os.system("dot -Tpng ./graphs/{}.dot -o ./graphs/{}.png".format(filename, filename))


def save_mulitple_trees_from_openings(database, openings, depth, filename):
    for opening in openings:
        print("Creating tree for {}".format(opening))
        list_of_games = database.get_games_with_opening(opening)
        tree = OpeningTree(list_of_games)
        save_tree_to_file(tree, depth, "{}_{}".format(filename, opening.replace(" ", "_")))
        os.system("dot -Tpng ./graphs/{}.dot -o ./graphs/{}.png".format("{}_{}".format(filename, opening.replace(" ", "_")), "{}_{}".format(filename, opening.replace(" ", "_"))))
             
def main():
    # database = PGNDatabase("./databases/sample.pgn")
    database = PGNDatabase("./databases/Stockfish_15_64-bit.commented.[2600].pgn")
    # database = PGNDatabase("./databases/100_games.pgn")
    list_of_games = database.get_games_with_opening("A03")
    print(len(list_of_games))
    
    
    openings = database.get_openings_that_occurred_at_least_n_times(60)
    save_mulitple_trees_from_openings(database, openings, 5, "tree")
    
    
    # tree = OpeningTree(list_of_games)
    
    # tree.print_tree(26, "tree")
    
    # os.system("dot -Tpng tree.dot -o tree.png")
    
    # tree.save_tree_to_file(26, "tre")

    
    
if __name__ == "__main__":
    main()
    

