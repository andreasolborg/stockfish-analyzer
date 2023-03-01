import time
from PGNDatabase import PGNDatabase
from anytree import RenderTree
from graphviz import Digraph

class Node:
    '''
    A class representing a node in the chess opening tree.
    '''
    def __init__(self, moves_list):
        '''
        Params:
            TODO
        '''
        if len(moves_list) < 2:
            self.parent_moves_token = ""
        else:
            self.parent_moves_token = "".join(moves_list[:-1])
            
        self.moves_token = ''.join(moves_list)
        self.moves_list = moves_list
        self.children = []

    def get_moves_token(self):
        return self.moves_token
    
    def get_parent_moves_token(self):
        return self.parent_moves_token
    
    def add_child(self, node):
        self.children.append(node)
        
    def get_label(self):
        if self.moves_list:
            return self.moves_list[-1]
        return "root"
    
class Tree:
    '''
    A class that creates the chess opening tree of nodes
    '''
    def __init__(self, database):
        '''
        Params:
            TODO
        '''
        self.database = database
        self.root_node = Node([])
        self.node_lookup = {}
        self.add_node_to_lookup(self.root_node)
    
    def add_node_to_lookup(self, node):
        self.node_lookup[node.get_moves_token()] = node
    
    def get_node_from_lookup(self, moves_token):
        return self.node_lookup[moves_token]
    
    def create_white_tree(self, depth):
        games = self.database.get_games_where_stockfish_is_white()
        
        for i in range(depth):
            for game in games:
                moves_list = []

                for j in range(i+1):
                    moves_list.append(game.get_half_move(j))
                    
                moves_token = ''.join(moves_list)

                if moves_token not in self.node_lookup:
                    node = Node(moves_list)
                    self.add_node_to_lookup(node)
                    self.get_node_from_lookup(node.get_parent_moves_token()).add_child(node)
                else:
                    
    
    def visualize_tree_in_terminal(self):
        for pre, _, node in RenderTree(self.root_node):
            print(f"{pre}{node.moves_token}")
    
    def visualize_tree_in_png(self):
        dot = Digraph()
        for pre, _, node in RenderTree(self.root_node):
            dot.node(node.get_moves_token(), label=node.get_label())  
            if node.get_moves_token() != "":
                dot.edge(node.get_parent_moves_token(), node.get_moves_token())
     
        dot.render('tree', format='png')
        

def main():
    start_time = time.time()
    pgn = PGNDatabase("sample.pgn")
    
    tree = Tree(pgn)
    tree.create_white_tree(20) #TODO; list out of index
    #tree.visualize_tree_in_terminal()
    tree.visualize_tree_in_png()
    

    print(f"Time: {time.time() - start_time}")


main()
        
    