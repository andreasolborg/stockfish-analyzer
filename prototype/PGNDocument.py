import os
import time
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
from PGNDatabase import PGNDatabase


class PGNDocument:
    '''
    Encapsulates a single PGN document
    '''
    def __init__(self, database):
        self.database = database
        self.document = Document()

    def create_document(self):
        self.create_document_heading()
        self.create_document_body()
        self.create_document_conclusion()
        self.save_document()

    def create_document_heading(self):
        self.document.add_heading('Chess Database', 0)

    def create_document_introduction(self):
        self.document.add_heading('1. Introduction', level=1)
        self.document.add_paragraph('This document is a summary of the chess database.')

    
    def create_document_body(self):
        self.create_document_introduction()
        self.create_document_body_game_count()
        self.create_document_result_table_with_stockfish()
        self.create_document_body_plycount_distribution()

    def create_document_body_game_count(self):
        # Should include a table with game count for each player
        self.document.add_heading('2. Games', level=1)
        self.document.add_paragraph('\tThe database contains ' + str(len(self.database.get_games())) + ' games. The following sections describe the games in more detail.')

    def create_document_result_table_with_stockfish(self):
        list_of_games = self.database.get_games()
        list_of_drawed_games = self.database.get_draws()
        stockfish_wins_as_white, stockfish_wins_as_black = self.database.get_stockfish_wins(list_of_games)
        stockfish_losses_as_white, stockfish_losses_as_black = self.database.get_stockfish_losses(list_of_games)
        stockfish_draws_as_white, stockfish_draws_as_black = self.database.get_stockfish_draws(list_of_drawed_games)
        self.document.add_heading('2.1.2 Result table for Stockfish', level=3)
        self.document.add_paragraph('The following table shows the results of games where Stockfish either won or lost, depending on Stockfish color.')
        table = self.document.add_table(rows=1, cols=5)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = ''
        hdr_cells[1].text = 'Wins'
        hdr_cells[2].text = 'Draws'
        hdr_cells[3].text = 'Losses'
        hdr_cells[4].text = 'Percentage'
        row_cells = table.add_row().cells
        row_cells[0].text = 'Starts as white'
        row_cells[1].text = str(len(stockfish_wins_as_white))
        row_cells[2].text = str(len(stockfish_draws_as_white))
        row_cells[3].text = str(len(stockfish_losses_as_white))
        row_cells[4].text = str(round((len(stockfish_wins_as_white) / (len(stockfish_wins_as_white) + len(stockfish_losses_as_white))) * 100, 2)) + '%'
        row_cells = table.add_row().cells
        row_cells[0].text = 'Starts as black'
        row_cells[1].text = str(len(stockfish_wins_as_black))
        row_cells[2].text = str(len(stockfish_draws_as_black))
        row_cells[3].text = str(len(stockfish_losses_as_black))
        row_cells[4].text = str(round((len(stockfish_wins_as_black) / (len(stockfish_wins_as_black) + len(stockfish_losses_as_black))) * 100, 2)) + '%'
        row_cells = table.add_row().cells
        row_cells[0].text = 'Total'
        row_cells[1].text = str(len(stockfish_wins_as_white) + len(stockfish_wins_as_black))
        row_cells[2].text = str(len(stockfish_draws_as_white) + len(stockfish_draws_as_black))
        row_cells[3].text = str(len(stockfish_losses_as_white) + len(stockfish_losses_as_black))
        row_cells[4].text = str(round(((len(stockfish_wins_as_white) + len(stockfish_wins_as_black)) / (len(stockfish_wins_as_white) + len(stockfish_wins_as_black) + len(stockfish_losses_as_white) + len(stockfish_losses_as_black))) * 100, 2)) + '%'


    def create_document_body_plycount_distribution(self):
        self.document.add_heading('2.3 Plycount distribution', level=2)
        self.document.add_paragraph('\tThe following graph shows the distribution of plycount in the database.')
        self.document.add_paragraph('\tThe x-axis shows the plycount, and the y-axis shows the number of games with that plycount.')
        plycount_distribution = self.database.get_plycount_distribution()
        sorted_plycount_distribution = self.database.sort_plycount_distribution_by_key(plycount_distribution)
        self.database.plot_plycount_distribution(sorted_plycount_distribution)
        self.document.add_picture('plycount_distribution.png', width=Inches(6))

    
    def create_document_conclusion(self):
        self.document.add_heading('3. Conclusion', level=1)
        self.document.add_paragraph('This document is a summary of the chess database.')


    def save_document(self):
        os.remove('ChessDatabase.docx') # Remove the file if it already exists to avoid an error
        self.document.save('ChessDatabase.docx')


def main():
    start_time = time.time()
    database = PGNDatabase("./Stockfish_15_64-bit.commented.[2600].pgn")
    document = PGNDocument(database)
    document.create_document()

    print("Time elapsed: " + (str(time.time() - start_time)) + " seconds")

if __name__ == "__main__":
    main()




    
