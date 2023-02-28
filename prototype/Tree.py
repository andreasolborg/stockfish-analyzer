
from PGNDatabase import PGNDatabase
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import os



class TreeNode:
    def __init__(self, move, results, color):
        self.move = move
        self.results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}	
        self.children = []
        self.parent = None

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

    
        
        
    
    

class OpeningTree:
    def __init__(self, database):
        self.database = database
        self.root = TreeNode(None, None, None)
        self.create_tree()


    def create_tree(self):
        for game in self.database.get_games():
            result = game.get_result()
            moves = game.get_moves_without_comments()
            current_node = self.root
            for move in moves:
                child_node = None
                for child in current_node.get_children():
                    if child.get_move() == move:
                        child_node = child
                        break
                if child_node is None:
                    child_node = TreeNode(move, result, None)
                    print(len(moves))
                    child_node.increment_result(result)
                    current_node.add_child(child_node)
                current_node = child_node

    def print_tree(self, depth):
        with open("tree.dot", "w") as dot_file:
            dot_file.write("digraph G {\n")
            self.print_node(self.root, depth, 0, dot_file)
            dot_file.write("}\n")

    def print_node(self, node, depth, current_depth, dot_file):
        if current_depth < depth:
            for child in node.get_children():
                sequence_of_moves = []
                current_node = child
                while current_node.get_parent() is not None:
                    sequence_of_moves.append(current_node.get_move())
                    current_node = current_node.get_parent()
                sequence_of_moves.reverse()
                games_with_sequence = self.database.get_games_with_move_sequence(sequence_of_moves)
                for game in games_with_sequence:
                    node.increment_result(game.get_result())
                # print(sequence_of_moves)
                print(node.get_result())
                
                # print(statistics_for_sequence)
                
                dot_file.write('{} -> {} [label="{}"]\n'.format(str(node.get_move()), str(child.get_move()), node.get_result()))
                self.print_node(child, depth, current_depth + 1, dot_file)
                
        else:
            dot_file.write('{} [label="{}"]\n'.format(str(id(node)), len(node.get_children())))
        
        

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
    database = PGNDatabase("./prototype/sample.pgn")
    # database = PGNDatabase("./Stockfish_15_64-bit.commented.[2600].pgn")
    
    tree = OpeningTree(database)
    # tree.print_tree(3)
    # tree.print_node(tree.get_node_from_moves([]), 20, 0, open("tree.dot", "w"))
    
    tree.print_tree(3)
    
    os.system("dot -Tpng tree.dot -o tree.png")
    print("43")

    
    
if __name__ == "__main__":
    main()
    

