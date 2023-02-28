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

import pydot
from PGNDatabase import PGNDatabase
from anytree import Node as AnyNode, RenderTree

class Node:
    def __init__(self):
        self.player = None
        self.moves = []
        self.game_counts = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}
        self.children = {}
    
    def increment_game_count(self, result):
        self.game_counts[result] += 1
    
    def get_statistics(self):
        return self.game_counts
    
    def get_or_create_child(self, move):
        if move not in self.children:
            self.children[move] = Node()
        return self.children[move]
        

class OpeningTree:
    def __init__(self):
        self.root = Node()
    
    def add_game(self, moves, result):
        node = self.root
        node.increment_game_count(result)
        for move in moves:
            node = node.get_or_create_child(move)
            node.increment_game_count(result)
    
    def get_node(self, move_sequence):
        node = self.root
        for move in move_sequence:
            node = node.children.get(move)
            if not node:
                return None
        return node
    
    def get_statistics(self, move_sequence=[]):
        node = self.get_node(move_sequence)
        if not node:
            return None
        return node.get_statistics()
    
    def get_moves(self, move_sequence=[]):
        node = self.get_node(move_sequence)
        if not node:
            return None
        return list(node.children.keys())


      

def main():
    pgn = PGNDatabase("./Stockfish_15_64-bit.commented.[2600].pgn")
    # pgn = PGNDatabase("./prototype/sample.pgn")
    
    tree = OpeningTree()
    for game in pgn.get_games():
        moves = game.get_moves_without_comments()
        result = game.get_result()
        tree.add_game(moves, result)
    
    # Print out the whole tree in a nice way
    
    level_0 = tree.get_moves()
    for move in level_0:
        print(tree.get_moves([move]))
        
        
    print(tree.get_statistics(["e4", "c5"]))
        
        

    # # Anytree package
    # from anytree import Node, RenderTree
    # from anytree.exporter import DotExporter
    
    
    # for game in pgn.get_games():
    #     parent_node = Node(game.get_move(0))
    #     for move in game.get_moves():
    #         child = Node(move, parent=parent_node)
    #         parent_node = child
        
        

        
    # udo = Node("Udo")
    # marc = Node("Marc", parent=udo)
    # lian = Node("Lian", parent=marc)
    # dan = Node("Dan", parent=udo)
    # jet = Node("Jet", parent=dan)
    # jan = Node("Jan", parent=dan)
    # joe = Node("Joe", parent=dan)
    # print(udo)
    # DotExporter(udo).to_picture("udo.png")



    ## pydot package
    
    # graph = pydot.Dot("my_graph", graph_type="graph", bgcolor="white")
    # # Add nodes
    # my_node = pydot.Node("a", label="Foo")
    # graph.add_node(my_node)
    # # Or, without using an intermediate variable:
    # graph.add_node(pydot.Node("b", shape="circle"))

    # # Add edges
    # my_edge = pydot.Edge("a", "b", color="blue")x
    # graph.add_edge(my_edge)
    # # Or, without using an intermediate variable:
    # graph.add_edge(pydot.Edge("b", "c", color="blue"))

    # graph.write_png("output.png")

if __name__ == '__main__':
    main()
        
    