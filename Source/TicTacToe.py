import numpy as np
import tkinter as tk
import copy
import pickle

class Game:
    def __init__(self, master, player1, player2, Q_learn=None, Q={}, alpha=0.3, gamma=0.9):
        self.master = master
        master.title("Tic Tac Toe")

        # Create a dedicated frame for the game board
        frame = tk.Frame(master, bg="lightblue", padx=10, pady=10)
        frame.pack(pady=10)  # Use pack instead of grid to avoid conflicts

        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
        self.empty_text = ""
        self.board = Board()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    frame, height=3, width=6, text=self.empty_text,
                    font=("Arial", 16, "bold"), bg="white", fg="black",
                    command=lambda i=i, j=j: self.callback(self.buttons[i][j])
                )
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.reset_button = tk.Button(
            master, text="Reset", font=("Arial", 14, "bold"),
            bg="orange", fg="white", command=self.reset
        )
        self.reset_button.pack(pady=10)  # Use pack for the reset button

        self.status_label = tk.Label(
            master, text="Player X's Turn", font=("Arial", 14, "bold"),
            bg="lightblue", fg="darkblue"
        )
        self.status_label.pack(pady=10)  # Use pack for the status label

        self.Q_learn = Q_learn
        if self.Q_learn:
            self.Q = Q
            self.alpha = alpha          # Learning rate
            self.gamma = gamma          # Discount rate
            self.share_Q_with_players()

    @property
    def Q_learn(self):
        if self._Q_learn is not None:
            return self._Q_learn
        if isinstance(self.player1, QPlayer) or isinstance(self.player2, QPlayer):
            return True

    @Q_learn.setter
    def Q_learn(self, _Q_learn):
        self._Q_learn = _Q_learn

    def share_Q_with_players(self):             # The action value table Q is shared with the QPlayers to help them make their move decisions
        if isinstance(self.player1, QPlayer):
            self.player1.Q = self.Q
        if isinstance(self.player2, QPlayer):
            self.player2.Q = self.Q

    def callback(self, button):
        if self.board.over():
            return
        if isinstance(self.current_player, HumanPlayer):
            if self.empty(button):
                move = self.get_move(button)
                self.handle_move(move)
                if not self.board.over() and isinstance(self.current_player, ComputerPlayer):
                    # Trigger bot's move immediately after user's move
                    self.master.after(100, self.bot_move)
        elif isinstance(self.current_player, ComputerPlayer):
            self.bot_move()

    def bot_move(self):
        move = self.current_player.get_move(self.board)
        self.handle_move(move)
        if not self.board.over():
            self.status_label.config(text=f"Player {self.other_player.mark}'s Turn")

    def empty(self, button):
        return button["text"] == self.empty_text

    def get_move(self, button):
        info = button.grid_info()
        move = (int(info["row"]), int(info["column"]))                # Get move coordinates from the button's metadata
        return move

    def handle_move(self, move):
        if self.Q_learn:
            self.learn_Q(move)
        i, j = move         # Get row and column number of the corresponding button
        self.buttons[i][j].configure(text=self.current_player.mark)     # Change the label on the button to the current player's mark
        self.board.place_mark(move, self.current_player.mark)           # Update the board
        if self.board.over():
            winner = self.board.winner()
            if winner:
                self.status_label.config(text=f"Player {winner} Wins!", fg="green")
            else:
                self.status_label.config(text="It's a Draw!", fg="red")
        else:
            self.switch_players()

    def declare_outcome(self):
        if self.board.winner() is None:
            print("It's a draw!")
        else:
            print(f"The game is over. Player '{self.current_player.mark}' won!")

    def reset(self, suppress_output=False):
        if not suppress_output:
            print("Resetting the game...")
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=self.empty_text)
        self.board = Board(grid=np.ones((3, 3)) * np.nan)
        self.current_player = self.player1
        self.other_player = self.player2
        self.status_label.config(text="Player X's Turn", fg="darkblue")
        if not suppress_output:
            print("Game reset complete.")

    def switch_players(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2

    def play(self):
        if isinstance(self.player1, HumanPlayer) and isinstance(self.player2, HumanPlayer):
            pass        # For human vs. human, play relies on the callback from button presses
        elif isinstance(self.player1, HumanPlayer) and isinstance(self.player2, ComputerPlayer):
            pass
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, HumanPlayer):
            first_computer_move = self.player1.get_move(self.board)      # If player 1 is a computer, it needs to be triggered to make the first move.
            self.handle_move(first_computer_move)
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, ComputerPlayer):
            while not self.board.over():        # Make the two computer players play against each other without button presses
                self.play_turn()

    def play_turn(self):
        move = self.current_player.get_move(self.board)
        self.handle_move(move)

    def learn_Q(self, move):                        # If Q-learning is toggled on, "learn_Q" should be called after receiving a move from an instance of Player and before implementing the move (using Board's "place_mark" method)
        state_key = QPlayer.make_and_maybe_add_key(self.board, self.current_player.mark, self.Q)
        next_board = self.board.get_next_board(move, self.current_player.mark)
        reward = next_board.give_reward()
        next_state_key = QPlayer.make_and_maybe_add_key(next_board, self.other_player.mark, self.Q)
        if next_board.over():
            expected = reward
        else:
            next_Qs = self.Q[next_state_key]             # The Q values represent the expected future reward for player X for each available move in the next state (after the move has been made)
            if self.current_player.mark == "X":
                expected = reward + (self.gamma * min(next_Qs.values()))        # If the current player is X, the next player is O, and the move with the minimum Q value should be chosen according to our "sign convention"
            elif self.current_player.mark == "O":
                expected = reward + (self.gamma * max(next_Qs.values()))        # If the current player is O, the next player is X, and the move with the maximum Q vlue should be chosen
        change = self.alpha * (expected - self.Q[state_key][move])
        self.Q[state_key][move] += change


class Board:
    def __init__(self, grid=np.ones((3,3))*np.nan):
        self.grid = grid

    def winner(self):
        rows = [self.grid[i,:] for i in range(3)]
        cols = [self.grid[:,j] for j in range(3)]
        diag = [np.array([self.grid[i,i] for i in range(3)])]
        cross_diag = [np.array([self.grid[2-i,i] for i in range(3)])]
        lanes = np.concatenate((rows, cols, diag, cross_diag))      # A "lane" is defined as a row, column, diagonal, or cross-diagonal

        any_lane = lambda x: any([np.array_equal(lane, x) for lane in lanes])   # Returns true if any lane is equal to the input argument "x"
        if any_lane(np.ones(3)):
            return "X"
        elif any_lane(np.zeros(3)):
            return "O"

    def over(self):             # The game is over if there is a winner or if no squares remain empty (cat's game)
        return (not np.any(np.isnan(self.grid))) or (self.winner() is not None)

    def place_mark(self, move, mark):       # Place a mark on the board
        num = Board.mark2num(mark)
        self.grid[tuple(move)] = num

    @staticmethod
    def mark2num(mark):         # Convert's a player's mark to a number to be inserted in the Numpy array representing the board. The mark must be either "X" or "O".
        d = {"X": 1, "O": 0}
        return d[mark]

    def available_moves(self):
        return [(i,j) for i in range(3) for j in range(3) if np.isnan(self.grid[i][j])]

    def get_next_board(self, move, mark):
        next_board = copy.deepcopy(self)
        next_board.place_mark(move, mark)
        return next_board

    def make_key(self, mark):          # For Q-learning, returns a 10-character string representing the state of the board and the player whose turn it is
        fill_value = 9
        filled_grid = copy.deepcopy(self.grid)
        np.place(filled_grid, np.isnan(filled_grid), fill_value)
        return "".join(map(str, (list(map(int, filled_grid.flatten()))))) + mark

    def give_reward(self):                          # Assign a reward for the player with mark X in the current board position.
        if self.over():
            if self.winner() is not None:
                if self.winner() == "X":
                    return 1.0  # Positive reward for X
                elif self.winner() == "O":
                    return -1.0  # Negative reward for O
            else:
                return 0.5  # Neutral reward for a draw
        return 0.0  # No reward if the game is ongoing


class Player(object):
    def __init__(self, mark):
        self.mark = mark

    @property
    def opponent_mark(self):
        if self.mark == 'X':
            return 'O'
        elif self.mark == 'O':
            return 'X'
        else:
            print("The player's mark must be either 'X' or 'O'.")

class HumanPlayer(Player):
    pass

class ComputerPlayer(Player):
    pass

class RandomPlayer(ComputerPlayer):
    @staticmethod
    def get_move(board):
        moves = board.available_moves()
        if moves:   # If "moves" is not an empty list (as it would be if cat's game were reached)
            return moves[np.random.choice(len(moves))]    # Apply random selection to the index, as otherwise it will be seen as a 2D array

class THandPlayer(ComputerPlayer):
    def __init__(self, mark):
        super(THandPlayer, self).__init__(mark=mark)

    def get_move(self, board):
        moves = board.available_moves()
        if moves:
            for move in moves:
                if THandPlayer.next_move_winner(board, move, self.mark):
                    return move
                elif THandPlayer.next_move_winner(board, move, self.opponent_mark):
                    return move
            else:
                return RandomPlayer.get_move(board)

    @staticmethod
    def next_move_winner(board, move, mark):
        return board.get_next_board(move, mark).winner() == mark


class QPlayer(ComputerPlayer):
    def __init__(self, mark, Q={}, epsilon=0.2):
        super(QPlayer, self).__init__(mark=mark)
        self.Q = Q
        self.epsilon = epsilon

    def get_move(self, board):
        if np.random.uniform() < self.epsilon:  # Exploration
            return RandomPlayer.get_move(board)
        else:  # Exploitation
            state_key = QPlayer.make_and_maybe_add_key(board, self.mark, self.Q)
            Qs = self.Q[state_key]
            if self.mark == "X":
                return QPlayer.stochastic_argminmax(Qs, max)
            elif self.mark == "O":
                return QPlayer.stochastic_argminmax(Qs, min)

    @staticmethod
    def make_and_maybe_add_key(board, mark, Q):
        default_Qvalue = 1.0  # Encourage exploration
        state_key = board.make_key(mark)
        if state_key not in Q:
            moves = board.available_moves()
            Q[state_key] = {move: default_Qvalue for move in moves}
        return state_key

    @staticmethod
    def stochastic_argminmax(Qs, min_or_max):       # Determines either the argmin or argmax of the array Qs such that if there are 'ties', one is chosen at random
        min_or_maxQ = min_or_max(list(Qs.values()))
        if list(Qs.values()).count(min_or_maxQ) > 1:      # If there is more than one move corresponding to the maximum Q-value, choose one at random
            best_options = [move for move in list(Qs.keys()) if Qs[move] == min_or_maxQ]
            move = best_options[np.random.choice(len(best_options))]
        else:
            move = min_or_max(Qs, key=Qs.get)
        return move

def train_QPlayer():
    root = tk.Tk()
    root.title("Tic Tac Toe Training")
    root.geometry("400x400")
    root.configure(bg="lightblue")

    def start_training():
        try:
            N_episodes = int(entry.get())
            if N_episodes <= 0:
                raise ValueError("Number of episodes must be positive.")
        except ValueError as e:
            error_label.config(text=f"Error: {e}")
            return

        epsilon = 0.9
        player1 = QPlayer(mark="X", epsilon=epsilon)
        player2 = QPlayer(mark="O", epsilon=epsilon)
        game = Game(root, player1, player2)

        for episodes in range(N_episodes):
            if episodes % 1000 == 0:
                print(f"Training progress: {episodes}/{N_episodes} episodes completed.")
            game.play()
            game.reset(suppress_output=True)  # Suppress reset messages during training

        Q = game.Q
        filename = f"Bot_Training.p"
        pickle.dump(Q, open(filename, "wb"))

        print("Training completed. Q-table saved to", filename)
        root.destroy()
        main_menu()  # Return to the main menu after training

    label = tk.Label(
        root, text="Enter number of training episodes:", font=("Arial", 14),
        bg="lightblue", fg="darkblue"
    )
    label.pack(pady=10)

    entry = tk.Entry(root, font=("Arial", 14))
    entry.pack(pady=10)

    error_label = tk.Label(root, text="", font=("Arial", 12), fg="red", bg="lightblue")
    error_label.pack(pady=5)

    start_button = tk.Button(
        root, text="Start Training", font=("Arial", 14, "bold"),
        bg="orange", fg="white", command=start_training
    )
    start_button.pack(pady=10)

    root.mainloop()

def play_human_vs_QPlayer():
    try:
        with open("Bot_Training.p", "rb") as file:
            Q = pickle.load(file)
        print("Q-table loaded successfully.")
    except (FileNotFoundError, pickle.UnpicklingError):
        print("Q-table file is missing or corrupted. Creating a new empty Q-table...")
        Q = {}
        with open("Bot_Training.p", "wb") as file:
            pickle.dump(Q, file)
        print("Empty Q-table created. You can now play with the bot.")

    root = tk.Tk()
    root.configure(bg="lightblue")

    player1 = HumanPlayer(mark="X")
    player2 = QPlayer(mark="O", epsilon=0)

    game = Game(root, player1, player2, Q=Q)
    game.reset(suppress_output=True)  # Ensure the game is properly reset
    game.play()

    # Automatically trigger the bot's move if it is the first player's turn
    if isinstance(game.current_player, QPlayer):
        move = game.current_player.get_move(game.board)
        game.handle_move(move)

    root.mainloop()

def play_human_vs_human():
    root = tk.Tk()
    root.configure(bg="lightblue")

    player1 = HumanPlayer(mark="X")
    player2 = HumanPlayer(mark="O")

    game = Game(root, player1, player2)
    game.play()
    root.mainloop()

def main_menu():
    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.geometry("400x400")
    root.configure(bg="lightblue")

    title_label = tk.Label(
        root, text="Tic Tac Toe", font=("Arial", 24, "bold"),
        bg="lightblue", fg="darkblue"
    )
    title_label.pack(pady=20)

    train_button = tk.Button(
        root, text="Train Bot", font=("Arial", 16, "bold"),
        bg="orange", fg="white", command=lambda: [root.destroy(), train_QPlayer()]
    )
    train_button.pack(pady=10)

    play_bot_button = tk.Button(
        root, text="Play with Bot", font=("Arial", 16, "bold"),
        bg="green", fg="white", command=lambda: [root.destroy(), play_human_vs_QPlayer()]
    )
    play_bot_button.pack(pady=10)

    play_human_button = tk.Button(
        root, text="Play with Another Player", font=("Arial", 16, "bold"),
        bg="blue", fg="white", command=lambda: [root.destroy(), play_human_vs_human()]
    )
    play_human_button.pack(pady=10)

    exit_button = tk.Button(
        root, text="Exit", font=("Arial", 16, "bold"),
        bg="red", fg="white", command=root.destroy
    )
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_menu()