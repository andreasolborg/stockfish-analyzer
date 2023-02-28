
from PGNDatabase import PGNDatabase
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import os

class TreeNode:
    def __init__(self, move, result):
        self.move = move
        self.result = result
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_move(self):
        return self.move

    def get_result(self):
        return self.result

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def __str__(self):
        return str(self.move)
    

class OpeningTree:
    def __init__(self, database):
        self.database = database
        self.tree = {}
        self.create_tree()

    def get_tree(self):
        return self.tree

    def create_tree(self):
        for game in self.database.get_games():
            result = game.get_result()
            moves = game.get_moves_without_comments()
            current_node = self.tree
            for move in moves:
                if move in current_node:
                    current_node = current_node[move]
                else:
                    current_node[move] = {}
                    current_node = current_node[move]

    def print_tree(self, depth):
        self.print_node(self.tree, depth, 0)
        

    def print_node(self, node, depth, current_depth, dot_file):
        if current_depth < depth:
            for key in node:
                dot_file.write('{} -> {} [label="{}"]\n'.format(str(id(node)), str(id(node[key])), key))
                self.print_node(node[key], depth, current_depth + 1, dot_file)
            
        else:
            dot_file.write('{} [label="{}"]\n'.format(str(id(node)), len(node)))
        
            
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
    
    tree = OpeningTree(database)
    # tree.print_tree(3)
    # tree.print_node(tree.get_node_from_moves([]), 20, 0, open("tree.dot", "w"))
    with open('tree.dot', 'w') as f:
        f.write('digraph G {\n')
        tree.print_node(tree.get_tree(), 10, 0, f)
        f.write('}\n')
        
    os.system('dot -Tpng tree.dot -o tree.png')

    
    
if __name__ == "__main__":
    main()
    

