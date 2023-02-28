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
import graphviz

class Tree:
    '''
    TODO: write class desc
    '''
    def __init__(self, player_color, games):
        '''
        Params:
            player_color: Either 'w' or 'b'. This is the color of the player we want to analyze openings for
            games: A list with instances of PGNGame
        '''
        self.nodes = [] # When we parse self.games we should get this filled up
        self.player_color = player_color
        self.root_node = root_node # We must choose the root node we want? Or do we create a three starting from no move?
        self.games = games
        
        
    def create_tree(self):
        pass
    
    def visualize(self):
        pass
        
    