# Required packages and software:
- GraphViz
- python-docx
- openpyxl

# General overview:
## Classes:
- Game: 		Data structure for a single chessgame. Includes a list of Move objects, and the games metadata as a dictionary.
- Move: 		Data structure for a single chessmove. Encapsulates a parsed chessmove, including all of the moves data such as the movenumber, the moves themselves, and their comments respectively.
- Database: 	Data structure for managing multiple chessgames. Includes functions for parsing a PGN-file, and composing a PGN-file. Also includes functions for parsing and composing an Excel-file. 
- OpeningTree:	Data structure for managing a tree of chessgames. Includes functions for creating the tree, and printing the tree.
- TreeNode: 	Data structure for a single node in the OpeningTree.
- Plot:			Class that encapsulates functions used for plotting given a list of games. 
- Document:	 	Class that encapsulates functions used for creating a Word document given a list of games. Also includes functions for creating tables and inserting images. 

# Proposed solution for each task:
## 2.1 Games
Task 1 is solved in the PGNGame class, where each game has a list of PGNMove objects. Each game has a dictionary of meta data, and a ordered list of moves
Task 2 and 3 are solved in the PGNDatabase class, in the parse_from_pgn and compose_to_pgn functions. For task 3, we assume you mean design function to export a game TO a textfile, and not from a textfile.
Task 4: PGNDatabase includes a list of games. The parsing functionality implemented in task 2 supports managing multiple chessgames aswell as a single chessgame. jon skriv mer
Task 5: Solved in PGNDatabase with the compose_to_excel and parse_to_excel functions. These function uses 

## 2.2 Statistics

Task 6: 	The functionality for creating Word documents is in the Document.py using the python-docx package.

Task 7: 	Functions for extracting out a list of games based on color and/or results is in the Database class.
			These functions are called upon initializing a Document object to ensure that these variables gets assigned to the Document object aswell.
			The Document class has a function for making tables based upon what these variables contain.

Task 8: 	To plot the porportion of still ongoing games after n moves, we choose to make a reverse cumulative histogram plot. 
			The functionality for plotting takes place inside the Plot class.
			Calculations of mean and standard deviations of games are implemented in the Database object, while table-insertion belongs to the Document class. 
			For plotting multiple histograms on the same figure, the plot_multiple_move_count_histogram_cumulative() function in Plot.py iterates over a dictionary {"List_name": list_of_games} plotting each value, with the key as the plot-label.
	
## 2.3 Openings
Task 9:		The data structures for encoding trees are in the Tree.py file. This file contains two classes related to the data structure of a tree. 
			Opon creating a new OpeningTree object with a chosen Database object as input parameter, it creates a tree by iterating through the moves for each game. If we encounter a new move (current node does not have a child with this move sequence), we create a new node and adds it as a child of the current node. If the move already is a child of the current node, we increment its result.

Task 10: 	An OpeningTree object takes in a list of games as a parameter, and creates a tree by iterating over the moves for each game in the databases list_of_games. We 

Task 11: 	Printing the tree is an iterative process, and takes place in the print_node function inside the OpeningTree class. In the function we are also writing the information about the nodes and edges to a .DOT file, while also labeling the nodes with the result and amount of games in each node. GraphViz is required for visualizing the trees and converting the .DOT files to .PNGs.
	 		Since the DOT files are converted to a PNG-image, we use the document.add_picture() to add the trees into the report. We have also have added a hyperlink in the document that opens the up image locally if the image is scaled down to a size which makes the node information blurry.

Task 12: 	The user are required to give some input in order to generate the document report. This includes a list of desired openings to print trees for, and their desired max_tree_depth, and minimum_games_on_node_to_keep_going_on_a_branch. The latter serves as a threshold value, and restricts the visualisation of tree such that stop generating a branch when a nodes number of games reaches this value.
	 		Lastly, the user must choose the minimum_opening_occurences_to_add_to_table, and this variable controls which openings that to store in the documents final table.