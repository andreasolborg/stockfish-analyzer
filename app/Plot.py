import matplotlib.pyplot as plt
from Database import Database 

class Plot:
    
    def plot_multiple_move_count_histogram_cumulative(self, dict_with_lists_of_games, filename):
        fig, ax = plt.subplots()
        fig.set_size_inches(10,5)

        for key, value in dict_with_lists_of_games.items():
            self.plot_move_count_histogram_cumulative(value, key, filename)
        
        plt.legend()
        plt.savefig(filename)

    def plot_move_count_histogram_cumulative(self, list_of_games, textinfo, filename, axis=None):
        move_count_distribution = self.get_move_count_distribution(list_of_games)
        move_count_distribution = self.sort_dict(move_count_distribution)
        data = [(moves, games) for moves, games in move_count_distribution]
        data = sorted([(moves, games) for moves, games in data], reverse=True)
        # calculate the cumulative sum of the games for each move count
        cumulative_data = []
        cumulative_sum = 0
        for moves, games in data:
            cumulative_sum += games
            cumulative_data.append((moves, cumulative_sum))
        # plot the cumulative frequency as a function of the move count
        x = [moves for moves, games in cumulative_data]
        y = [games for moves, games in cumulative_data]
        if axis is None:  # if no axis is given, create a new one
            axis = plt.gca() # get current axis
        axis.plot(x, y, label=textinfo)
        axis.set_xlim(15, 125)
        axis.set_xlabel('Number of Moves')
        axis.set_ylabel('Cumulative Number of Games')
        axis.set_title('Reverse Histogram of Chess Game Length')

    def get_move_count_distribution(self, list_of_games):
        move_count_distribution = {}
        for game in list_of_games:
            move_count = len(game.get_moves())
            if move_count in move_count_distribution:
                move_count_distribution[move_count] += 1
            else:
                move_count_distribution[move_count] = 1
        return move_count_distribution

    def sort_dict(self, dict):
        return sorted(dict.items(), key=lambda x: x[0])
    
    def plot_plycount_distribution(self, list_of_games):
        plycount_distribution = self.get_move_count_distribution(list_of_games)
        plycount_distribution = self.sort_dict(plycount_distribution)
        #Clear plot
        x = []
        y = []
        for key, value in plycount_distribution:
            x.append(key)
            y.append(value)
        plt.figure(figsize=(10,3))
        plt.plot(x, y)
        plt.xlim(15, 250)
        plt.ylim(0, 150)
        plt.savefig('./plots/plycount_distribution.png')
        # plt.show()

    def plot_move_count_distribution(self, list_of_games):
        move_count_distribution = self.get_move_count_distribution(list_of_games)
        move_count_distribution = self.sort_dict(move_count_distribution)
        #Clear plot
        x = []
        y = []
        for key, value in move_count_distribution:
            x.append(key)
            y.append(value)
        #Min and max values for x and y axis
        plt.ylim(0, 150)        
        plt.xlim(15, 125)
        plt.figure(figsize=(50,100))
        plt.xlabel('Number of moves')
        plt.ylabel('Number of games')
        plt.plot(x, y)
        plt.fill_between(x, y, color='blue', alpha=0.5)
        plt.savefig('./plots/move_count_distribution.png')

    def save_histogram(self, path):
        plt.savefig(path)

    def clear_plot(self):
        plt.clf()


def main():
    
    database = Database()
    database.parse_from_pgn("./databases/2600_games.pgn")

    list_of_games = database.get_list_of_games()
    list_of_games_where_stockfish_is_white = database.get_list_of_games_where_stockfish_is_white()
    list_of_games_where_stockfish_is_black = database.get_list_of_games_where_stockfish_is_black()

    dictionary = {"All games": list_of_games, "Games where Stockfish is white": list_of_games_where_stockfish_is_white, "Games where Stockfish is black": list_of_games_where_stockfish_is_black} 

    plot = Plot()
    plot.plot_multiple_move_count_histogram_cumulative(dictionary, "./plots/test.png")

    
if __name__ == "__main__":
    main()
    
