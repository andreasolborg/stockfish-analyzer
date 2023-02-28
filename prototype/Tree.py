
from PGNDatabase import PGNDatabase
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import os



class TreeNode:
    def __init__(self, move,  move_number, results, color):
        self.move = move
        self.move_number = move_number
        self.results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}	
        self.children = []
        self.parent = None
        self.color = color

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
        
    def get_color(self):
        if self.move_number != None:
            if self.move_number % 2 == 0:
                return "white"
            else:
                return "grey"
        else:
            return "white"

    
    def set_color(self, color):
        self.color = color
        
    def get_move_number(self):
        return self.move_number
        
    

class OpeningTree:
    def __init__(self, database):
        self.database = database
        self.root = TreeNode(None, None, None, None)
        self.create_tree()


    def create_tree(self):
        for game in self.database.get_games():
            result = game.get_result()
            moves = game.get_moves_without_comments()
            current_node = self.root
            move_number = 0
            for move in moves:
                child_node = None
                for child in current_node.get_children(): # check if child already exists
                    if child.get_move() == move: # if child exists, increment result
                        child_node = child # and
                        child.increment_result(result)

                        break # break out of loop
                if child_node is None: # if child does not exist, create it 
                    child_node = TreeNode(move, move_number, None, None) # create child
                    color = child_node.get_color() # get color
                    child_node.set_color(color) # set color
                    child_node.increment_result(result) # and increment result

                    current_node.add_child(child_node) # add child to parent
                current_node = child_node
                move_number += 1

    def print_tree(self, depth):
        with open("tree.dot", "w") as dot_file:
            dot_file.write("digraph G {\n")
            self.print_node(self.root, depth, 0, dot_file)
            dot_file.write("}\n")

    def print_node(self, node, depth, current_depth, dot_file):
        if current_depth < depth:
            for child in node.get_children():
                dot_file.write('{} [label="{}" fillcolor="{}", style="filled"] \n'.format(str(id(node)), node.get_move(), node.get_color()))
                dot_file.write('{} -> {} [label="{}"]\n'.format(str(id(node)), str(id(child)), node.get_result()))

                self.print_node(child, depth, current_depth + 1, dot_file)
        else: # leaf node
            dot_file.write('{} [label="{}"]\n'.format(str(id(node)), node.get_result()))
        
        

    # def print_node(self, node, depth, current_depth, dot_file):
    #     if current_depth < depth:
    #         for child in node.get_children():
    #             dot_file.write('{} -> {}\n'.format(str(id(node)), str(id(child))))
    #             self.print_node(child, depth, current_depth + 1, dot_file)
            
        # else:
        #     dot_file.write('{} [label="{}"]\n'.format(str(id(node)), len(node)))
        
            
    def get_node(self, node, moves):
        if len(moves) == 0:
            return node
        
        else:
            return self.get_node(node[moves[0]], moves[1:])
        
    def get_node_from_moves(self, moves):
        return self.get_node(self.tree, moves)

    def get_node_from_game(self, game):
        return self.get_node_from_moves(game.get_moves_without_comments())
    

def main():
    # database = PGNDatabase("./prototype/sample.pgn")
    # database = PGNDatabase("./Stockfish_15_64-bit.commented.[2600].pgn")
    database = PGNDatabase("./100_games.pgn")
    for data in database():
        print(data)
    
    
    tree = OpeningTree(database)
    # tree.print_tree(3)
    # tree.print_node(tree.get_node_from_moves([]), 20, 0, open("tree.dot", "w"))
    
    tree.print_tree(3)
    
    os.system("dot -Tpng tree.dot -o tree.png")

    
    
if __name__ == "__main__":
    main()
    

