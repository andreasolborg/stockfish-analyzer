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

class Tree:
    '''
    TODO: write class desc
    '''
    def __init__(self, games):
        '''
        Params:
            player_color: Either 'w' or 'b'. This is the color of the player we want to analyze openings for
            games: A list with instances of PGNGame
        '''
        self.nodes = [] # When we parse self.games we should get this filled up
        # self.root_node = root_node # We must choose the root node we want? Or do we create a three starting from no move?
        self.games = games
        
        
    def create_tree(self):
        pass
    
    def visualize(self):
        pass
    

def main():
    #pgn = PGNDatabase("sample.pgn")
    #tree = Tree(pgn)

    # Anytree package
    #from anytree import Node, RenderTree
    #from anytree.exporter import DotExporter
    
    
    #for game in pgn.get_games():
    #    parent_node = Node(game.get_move(0))
    #    for move in game.get_moves():
    #        child = Node(move, parent=parent_node)
    #        parent_node = child
        
        

        
    #udo = Node("Udo")
    #marc = Node("Marc", parent=udo)
    #lian = Node("Lian", parent=marc)
    #dan = Node("Dan", parent=udo)
    #jet = Node("Jet", parent=dan)
    #jan = Node("Jan", parent=dan)
    #joe = Node("Joe", parent=dan)
    #print(udo)
    #DotExporter(udo).to_picture("udo.png")



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
        
    