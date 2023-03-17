"""
Authors: Andreas Olborg and Jon Grendstad
Group: group_4
"""

from Database import Database
import os
import time
  
class OpeningTree:  
    def __init__(self, list_of_games):
        self.list_of_games = list_of_games
        self.root = TreeNode(None, None)
        self.create_tree()
        self.root_label = "Opening: " + self.list_of_games[0].lookup_meta_data("Opening") + "\n" + "Number of games: " + str(len(self.list_of_games))

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
                    child_node.increment_result(result) # increment result
                    current_node.add_child(child_node) # add child to parent
                
                current_node = child_node
                move_number += 1

    def print_node(self, node, max_tree_depth, minimum_games_on_node_to_continue_on_branch, current_depth, dot_file):
        if node.get_number_of_games() <= minimum_games_on_node_to_continue_on_branch and node.get_parent() is not None: # if number of games inside the node is less than 5, we do not want to plot any children. But we should label the node
            dot_file.write('{} [label="{}", fillcolor="{}", fontcolor="{}", style="filled", fontsize="60pt"];\n'.format(str(id(node)), "Games: " + str(node.get_number_of_games()) +"\n " + node.get_result(), node.get_color(), node.get_text_color())) # write node
            return # return from function
        if current_depth < max_tree_depth: # not leaf node and not at max depth
            for child in node.get_children():
                # if number of games inside the node is less than given threshold, we do not want to plot any children
                dot_file.write('{} [label="{}", fillcolor="{}", fontcolor="{}", style="filled", fontsize="60pt"];\n'.format(str(id(node)), "Games: " + str(node.get_number_of_games()) +"\n " + node.get_result(), node.get_color(), node.get_text_color())) # write node
                dot_file.write('{} -> {} [label="{}" fontsize="60pt" arrowsize="3"];\n'.format(str(id(node)), str(id(child)), child.get_move())) # write edge 
                self.print_node(child, max_tree_depth, minimum_games_on_node_to_continue_on_branch, current_depth + 1, dot_file) # recursive call to print child nodes
        else: # leaf node
            dot_file.write('{} [label="{}", fillcolor="{}", fontcolor="{}", style="filled" fontsize="60pt"];\n'.format(str(id(node)), "Games: " + str(node.get_number_of_games()) +"\n " + node.get_result(), node.get_color(), node.get_text_color())) # write node
        if node.get_parent() is None: # if node is root node
            dot_file.write('{} [label="{}", fillcolor="{}", fontcolor="{}", style="filled" fontsize="60pt"];\n'.format(str(id(node)), self.root_label, node.get_color(), node.get_text_color())) # write root node


    def save_tree(self, max_tree_depth, minimum_games_on_node_to_continue_on_branch, filename):
        print("Saving tree to file {}".format(filename)) # print to console
        if os.path.exists("graphs/{}.dot".format(filename)): # if file already exists, delete it
            os.remove("graphs/{}.dot".format(filename))
        if os.path.exists("graphs/{}.png".format(filename)): # if file already exists, delete it
            os.remove("graphs/{}.png".format(filename))
        with open("graphs/{}.dot".format(filename), "w") as dot_file: 
            dot_file.write("digraph G {\n")
            dot_file.write('rankdir=LR;\ncenter=true;\nsize="10,7"\n')
            self.print_node(self.root, max_tree_depth, minimum_games_on_node_to_continue_on_branch, 0, dot_file) # recursive call to print nodes
            dot_file.write("}\n")
        os.system("dot -Tpng -Gdpi=500 graphs/{}.dot -o graphs/{}.png".format(filename, filename)) # create png from dot file
             
class TreeNode:
    def __init__(self, move, move_number):
        self.move = move
        self.move_number = move_number
        self.parent = None
        self.color = None
        self.text_color = "black"
        self.results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}
        self.children = []
        self.set_color(move_number)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_move(self):
        return self.move

    def get_result(self):
        return "W:{} D:{} B:{}".format(self.results["1-0"], self.results["1/2-1/2"], self.results["0-1"])
    
    def get_number_of_games(self):
        return self.results["1-0"] + self.results["1/2-1/2"] + self.results["0-1"]

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def increment_result(self, result):
        self.results[result] += 1
        
    def set_color(self, number):
        if number != None:
            if number % 2 == 0:
                self.color = "#2c2c2c"
                self.text_color = "white"
            else:
                self.color = "white"
                self.text_color = "black"
        else:
            self.color = "white"
            self.text_color = "black"
    
    def get_color(self):
        return self.color

    def get_text_color(self):
        return self.text_color
    
    def __str__(self):
        return str(self.move)

def main():
    time_start = time.time()

    database = Database()
    database.parse_from_pgn("databases/Stockfish_15_64-bit.commented.[2600].pgn")
    sicilian_list = database.get_list_with_opening("Sicilian")
    
    tree = OpeningTree(sicilian_list)

    # Parameters that the user can play with and adjust
    max_tree_depth = 15
    minimum_games_on_node_to_continue_on_branch = 4
    filename = "tree_Sicilian"

    tree.save_tree(max_tree_depth, minimum_games_on_node_to_continue_on_branch, filename)

    print(f"Time: {time.time() - time_start}")

if __name__ == "__main__":
    main()
    

