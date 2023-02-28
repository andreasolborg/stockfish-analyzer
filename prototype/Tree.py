'''
# PLAN

### Task 9: 
- Each position is only stored once in the chess tree. This means that regardless of the moves played to reach it, the exact same information will be stored
    - The number of games won by white in this position
    - The number of games win by black in this position
    - The number of games resulted in a draw in this position
    - The name of the opening
    - The move
    - The children nodes
    - The degree (move number)
    
### Task 10: 
- We use PGNDatabase functions and send a list of games into this class as a argument
    - For example, get_games_where_stockfish_is_black()
- TODO: how do we parse this game an create a tree??

root = Node(color, children, meta_data)
node2 = Node(color2, children2, meta_data2)
node3 = Node(...)
node4 = Node(...)
node5 = Node(...)
node6 = Node(...)

root.add_child(node2)
root.add_child(node3)
node2.add_child(node4)
node2.add_child(node5)
node3.add_child(node6)

tree = Tree(root)
tree.visualize()

### Task 11: 
- Depth is number of half moves
- We print the opening tree using graphviz

### Task 12


'''



import time
from PGNDatabase import PGNDatabase
from anytree import Node, RenderTree

class Node:
    '''
    A class representing a node in the chess opening tree.
    '''
    def __init__(self, moves_token):
        '''
        Params:
            color: Either the character 'w' for white or 'b' for black
            games: A list with instances of PGNGame
        '''
        
        self.moves_token = moves_token   
        self.children = []
        self.count = 1

    def get_moves_token(self):
        return self.moves_token
    
    def add_child(self, node):
        self.children.append(node)
    
    def get_all_children(self):
        return self.children
    
    def increase_count(self):
        self.count += 1


class Tree:
    '''
    TODO: write class desc
    '''
    def __init__(self, database):
        '''
        Params:
     
        '''
        self.database = database
        self.root_node = Node("")
        self.node_lookup = {}
        self.add_node_to_lookup(self.root_node)
        
    def get_node_by_move_token(self):
        pass
    
    def add_node_to_lookup(self, node):
        self.node_lookup[node.get_moves_token()] = node
    
    def get_node_from_lookup(self, moves_token):
        return self.node_lookup[moves_token]
    
    def create_white_tree(self, depth):
        games = self.database.get_games_where_stockfish_is_white()
        
        for i in range(depth):
            #print("####",i, "####")
            
            for game in games:
                parent_moves_token = ""
                new_moves_token = ""
                
                # this will create a string token for the parent and the new node
                for j in range(i+1):
                    if j != i:
                        parent_moves_token += game.get_half_move(j) + " "
                    new_moves_token += game.get_half_move(j) + " "
                
                # if the sequence of moves does not exist as a node we create a new node and add it to the children of its parent
                if new_moves_token not in self.node_lookup:
                    new_node = Node(new_moves_token)
                    self.add_node_to_lookup(new_node)
                    self.get_node_from_lookup(parent_moves_token).add_child(new_node)
                # if the node exist we can add meta data etc to it
                else:
                    
                    ## legg til win/tap/draw på eksiterende node
                    
                    self.get_node_from_lookup(new_moves_token).increase_count()
            
    
    def visualize_tree(self):
        for pre, _, node in RenderTree(self.root_node):
            print(f"{pre}{node.moves_token}")
    

def main():
    start_time = time.time()
    pgn = PGNDatabase("sample.pgn")
    
    tree = Tree(pgn)
    tree.create_white_tree(20)
    tree.visualize_tree()
    
    #print(len(tree.get_node_from_lookup("").get_all_children()))
    #print(len(tree.get_node_from_lookup("e4 c5 Nf3 ").get_all_children()))
    #print(len(tree.get_node_from_lookup("e4 c5 Nf3 d6 ").get_all_children()))
    #print(len(tree.get_node_from_lookup("e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 Bg5 e6 f4 Nbd7 Qf3 Qc7 O-O-O b5 ").get_all_children()))
    
    
    print(f"Time: {time.time() - start_time}")


main()
        
    