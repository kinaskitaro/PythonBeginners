import numpy as np
import tkinter as tk
from tkinter import font as tkfont
import copy
import pickle

class Game:
    def __init__(self, master, player1, player2, Q_learn=None, Q={}, alpha=0.3, gamma=0.9):
        self.master = master
        master.title("Tic Tac Toe")
        master.geometry("500x650")
        master.configure(bg="#1e1e2e")
        master.resizable(False, False)

        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
        self.empty_text = ""
        self.board = Board()
        self.x_score = 0
        self.o_score = 0

        self.create_widgets()

        self.Q_learn = Q_learn
        if self.Q_learn:
            self.Q = Q
            self.alpha = alpha
            self.gamma = gamma
            self.share_Q_with_players()

    def create_widgets(self):
        title_font = tkfont.Font(family="Segoe UI", size=32, weight="bold")
        label_font = tkfont.Font(family="Segoe UI", size=14)
        button_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        reset_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")

        header_frame = tk.Frame(self.master, bg="#1e1e2e")
        header_frame.pack(pady=20)

        title_label = tk.Label(
            header_frame,
            text="Tic Tac Toe",
            font=title_font,
            bg="#1e1e2e",
            fg="#ffffff"
        )
        title_label.pack()

        score_frame = tk.Frame(self.master, bg="#1e1e2e")
        score_frame.pack(pady=10)

        self.score_x_label = tk.Label(
            score_frame,
            text=f"X: {self.x_score}",
            font=tkfont.Font(family="Segoe UI", size=18, weight="bold"),
            bg="#1e1e2e",
            fg="#ff6b6b"
        )
        self.score_x_label.pack(side=tk.LEFT, padx=30)

        self.score_o_label = tk.Label(
            score_frame,
            text=f"O: {self.o_score}",
            font=tkfont.Font(family="Segoe UI", size=18, weight="bold"),
            bg="#1e1e2e",
            fg="#4ecdc4"
        )
        self.score_o_label.pack(side=tk.LEFT, padx=30)

        self.status_label = tk.Label(
            self.master,
            text="Player X's Turn",
            font=label_font,
            bg="#1e1e2e",
            fg="#a0a0a0"
        )
        self.status_label.pack(pady=10)

        board_frame = tk.Frame(self.master, bg="#1e1e2e", padx=20)
        board_frame.pack(pady=10)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    board_frame,
                    height=2,
                    width=5,
                    text=self.empty_text,
                    font=button_font,
                    bg="#2d2d44",
                    fg="#ffffff",
                    activebackground="#3d3d5c",
                    relief="flat",
                    cursor="hand2",
                    command=lambda i=i, j=j: self.callback(self.buttons[i][j])
                )
                self.buttons[i][j].grid(row=i, column=j, padx=4, pady=4)

        buttons_frame = tk.Frame(self.master, bg="#1e1e2e")
        buttons_frame.pack(pady=20)

        self.reset_button = tk.Button(
            buttons_frame,
            text="New Game",
            font=reset_font,
            bg="#6c5ce7",
            fg="#ffffff",
            activebackground="#5b4cc4",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.reset
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)

        menu_button = tk.Button(
            buttons_frame,
            text="Menu",
            font=reset_font,
            bg="#636e72",
            fg="#ffffff",
            activebackground="#52565a",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=10,
            command=lambda: [self.master.destroy(), main_menu()]
        )
        menu_button.pack(side=tk.LEFT, padx=10)

    @property
    def Q_learn(self):
        if hasattr(self, '_Q_learn') and self._Q_learn is not None:
            return self._Q_learn
        if hasattr(self, 'player1') and hasattr(self, 'player2'):
            if isinstance(self.player1, QPlayer) or isinstance(self.player2, QPlayer):
                return True
        return None

    @Q_learn.setter
    def Q_learn(self, _Q_learn):
        self._Q_learn = _Q_learn

    def share_Q_with_players(self):
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
                    self.master.after(500, self.bot_move)
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
        move = (int(info["row"]), int(info["column"]))
        return move

    def handle_move(self, move):
        if self.Q_learn:
            self.learn_Q(move)
        i, j = move
        self.buttons[i][j].configure(text=self.current_player.mark)
        
        if self.current_player.mark == "X":
            self.buttons[i][j].config(fg="#ff6b6b")
        else:
            self.buttons[i][j].config(fg="#4ecdc4")
        
        self.board.place_mark(move, self.current_player.mark)
        if self.board.over():
            winner = self.board.winner()
            if winner:
                self.status_label.config(text=f"Player {winner} Wins!", fg="#ffd93d")
                if winner == "X":
                    self.x_score += 1
                    self.score_x_label.config(text=f"X: {self.x_score}")
                else:
                    self.o_score += 1
                    self.score_o_label.config(text=f"O: {self.o_score}")
                self.highlight_winner()
            else:
                self.status_label.config(text="It's a Draw!", fg="#a0a0a0")
        else:
            self.switch_players()
            self.status_label.config(text=f"Player {self.current_player.mark}'s Turn")

    def highlight_winner(self):
        winner = self.board.winner()
        if winner:
            rows = [self.board.grid[i,:] for i in range(3)]
            cols = [self.board.grid[:,j] for j in range(3)]
            diag = [np.array([self.board.grid[i,i] for i in range(3)])]
            cross_diag = [np.array([self.board.grid[2-i,i] for i in range(3)])]
            lanes = np.concatenate((rows, cols, diag, cross_diag))

            target = 1 if winner == "X" else 0
            for i in range(3):
                if np.array_equal(rows[i], np.full(3, target)):
                    self.highlight_row(i, True)
                if np.array_equal(cols[i], np.full(3, target)):
                    self.highlight_row(i, False)
            if np.array_equal(diag[0], np.full(3, target)):
                self.highlight_diagonal(True)
            if np.array_equal(cross_diag[0], np.full(3, target)):
                self.highlight_diagonal(False)

    def highlight_row(self, index, is_row):
        for i in range(3):
            if is_row:
                self.buttons[index][i].config(bg="#ffd93d", fg="#1e1e2e")
            else:
                self.buttons[i][index].config(bg="#ffd93d", fg="#1e1e2e")

    def highlight_diagonal(self, is_main):
        for i in range(3):
            if is_main:
                self.buttons[i][i].config(bg="#ffd93d", fg="#1e1e2e")
            else:
                self.buttons[2-i][i].config(bg="#ffd93d", fg="#1e1e2e")

    def reset(self, suppress_output=False):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=self.empty_text, bg="#2d2d44", fg="#ffffff")
        self.board = Board(grid=np.ones((3, 3)) * np.nan)
        self.current_player = self.player1
        self.other_player = self.player2
        self.status_label.config(text="Player X's Turn", fg="#a0a0a0")

    def switch_players(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2

    def play(self):
        if isinstance(self.player1, HumanPlayer) and isinstance(self.player2, HumanPlayer):
            pass
        elif isinstance(self.player1, HumanPlayer) and isinstance(self.player2, ComputerPlayer):
            pass
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, HumanPlayer):
            first_computer_move = self.player1.get_move(self.board)
            self.handle_move(first_computer_move)
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, ComputerPlayer):
            while not self.board.over():
                self.play_turn()

    def play_turn(self):
        move = self.current_player.get_move(self.board)
        self.handle_move(move)

    def learn_Q(self, move):
        state_key = QPlayer.make_and_maybe_add_key(self.board, self.current_player.mark, self.Q)
        next_board = self.board.get_next_board(move, self.current_player.mark)
        reward = next_board.give_reward()
        next_state_key = QPlayer.make_and_maybe_add_key(next_board, self.other_player.mark, self.Q)
        if next_board.over():
            expected = reward
        else:
            next_Qs = self.Q[next_state_key]
            if self.current_player.mark == "X":
                expected = reward + (self.gamma * min(next_Qs.values()))
            elif self.current_player.mark == "O":
                expected = reward + (self.gamma * max(next_Qs.values()))
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
        lanes = np.concatenate((rows, cols, diag, cross_diag))

        any_lane = lambda x: any([np.array_equal(lane, x) for lane in lanes])
        if any_lane(np.ones(3)):
            return "X"
        elif any_lane(np.zeros(3)):
            return "O"

    def over(self):
        return (not np.any(np.isnan(self.grid))) or (self.winner() is not None)

    def place_mark(self, move, mark):
        num = Board.mark2num(mark)
        self.grid[tuple(move)] = num

    @staticmethod
    def mark2num(mark):
        d = {"X": 1, "O": 0}
        return d[mark]

    def available_moves(self):
        return [(i,j) for i in range(3) for j in range(3) if np.isnan(self.grid[i][j])]

    def get_next_board(self, move, mark):
        next_board = copy.deepcopy(self)
        next_board.place_mark(move, mark)
        return next_board

    def make_key(self, mark):
        fill_value = 9
        filled_grid = copy.deepcopy(self.grid)
        np.place(filled_grid, np.isnan(filled_grid), fill_value)
        return "".join(map(str, (list(map(int, filled_grid.flatten()))))) + mark

    def give_reward(self):
        if self.over():
            if self.winner() is not None:
                if self.winner() == "X":
                    return 1.0
                elif self.winner() == "O":
                    return -1.0
            else:
                return 0.5
        return 0.0


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
        if moves:
            return moves[np.random.choice(len(moves))]

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
        if np.random.uniform() < self.epsilon:
            return RandomPlayer.get_move(board)
        else:
            state_key = QPlayer.make_and_maybe_add_key(board, self.mark, self.Q)
            Qs = self.Q[state_key]
            if self.mark == "X":
                return QPlayer.stochastic_argminmax(Qs, max)
            elif self.mark == "O":
                return QPlayer.stochastic_argminmax(Qs, min)

    @staticmethod
    def make_and_maybe_add_key(board, mark, Q):
        default_Qvalue = 1.0
        state_key = board.make_key(mark)
        if state_key not in Q:
            moves = board.available_moves()
            Q[state_key] = {move: default_Qvalue for move in moves}
        return state_key

    @staticmethod
    def stochastic_argminmax(Qs, min_or_max):
        min_or_maxQ = min_or_max(list(Qs.values()))
        if list(Qs.values()).count(min_or_maxQ) > 1:
            best_options = [move for move in list(Qs.keys()) if Qs[move] == min_or_maxQ]
            move = best_options[np.random.choice(len(best_options))]
        else:
            move = min_or_max(Qs, key=Qs.get)
        return move

def train_QPlayer():
    root = tk.Tk()
    root.title("Tic Tac Toe Training")
    root.geometry("400x450")
    root.configure(bg="#1e1e2e")
    root.resizable(False, False)

    title_font = tkfont.Font(family="Segoe UI", size=24, weight="bold")
    label_font = tkfont.Font(family="Segoe UI", size=14)
    button_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")

    title_label = tk.Label(
        root,
        text="Train AI Bot",
        font=title_font,
        bg="#1e1e2e",
        fg="#ffffff"
    )
    title_label.pack(pady=30)

    input_frame = tk.Frame(root, bg="#1e1e2e")
    input_frame.pack(pady=20)

    tk.Label(
        input_frame,
        text="Episodes:",
        font=label_font,
        bg="#1e1e2e",
        fg="#a0a0a0"
    ).pack(side=tk.LEFT, padx=5)

    entry = tk.Entry(
        input_frame,
        font=label_font,
        bg="#2d2d44",
        fg="#ffffff",
        insertbackground="#6c5ce7",
        relief="flat",
        width=15
    )
    entry.insert(0, "10000")
    entry.pack(side=tk.LEFT, padx=5)

    error_label = tk.Label(root, text="", font=tkfont.Font(family="Segoe UI", size=10), fg="#ff6b6b", bg="#1e1e2e")
    error_label.pack(pady=5)

    def start_training():
        try:
            N_episodes = int(entry.get())
            if N_episodes <= 0:
                raise ValueError("Number must be positive.")
        except ValueError as e:
            error_label.config(text=f"Error: {e}")
            return

        progress_label.config(text="Training in progress...")
        start_button.config(state="disabled", bg="#636e72")

        def train():
            epsilon = 0.9
            player1 = QPlayer(mark="X", epsilon=epsilon)
            player2 = QPlayer(mark="O", epsilon=epsilon)
            game = Game(root, player1, player2)

            for episodes in range(N_episodes):
                game.play()
                game.reset(suppress_output=True)
                if episodes % 1000 == 0 and episodes > 0:
                    progress = int((episodes / N_episodes) * 100)
                    progress_label.config(text=f"Training: {progress}%")

            Q = game.Q
            filename = f"Bot_Training.p"
            pickle.dump(Q, open(filename, "wb"))

            progress_label.config(text="Training Complete!", fg="#4ecdc4")
            root.after(2000, lambda: [root.destroy(), main_menu()])

        root.after(100, train)

    start_button = tk.Button(
        root,
        text="Start Training",
        font=button_font,
        bg="#6c5ce7",
        fg="#ffffff",
        activebackground="#5b4cc4",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        command=start_training,
        padx=30,
        pady=10
    )
    start_button.pack(pady=20)

    progress_label = tk.Label(root, text="", font=label_font, bg="#1e1e2e", fg="#a0a0a0")
    progress_label.pack(pady=10)

    back_button = tk.Button(
        root,
        text="Back",
        font=button_font,
        bg="#636e72",
        fg="#ffffff",
        activebackground="#52565a",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        command=lambda: [root.destroy(), main_menu()],
        padx=20,
        pady=8
    )
    back_button.pack(pady=10)

    root.mainloop()

def play_human_vs_QPlayer():
    try:
        with open("Bot_Training.p", "rb") as file:
            Q = pickle.load(file)
    except (FileNotFoundError, pickle.UnpicklingError):
        Q = {}
        with open("Bot_Training.p", "wb") as file:
            pickle.dump(Q, file)

    root = tk.Tk()
    root.configure(bg="#1e1e2e")

    player1 = HumanPlayer(mark="X")
    player2 = QPlayer(mark="O", epsilon=0)

    game = Game(root, player1, player2, Q=Q)
    game.reset(suppress_output=True)
    game.play()

    if isinstance(game.current_player, QPlayer):
        move = game.current_player.get_move(game.board)
        game.handle_move(move)

    root.mainloop()

def play_human_vs_human():
    root = tk.Tk()
    root.configure(bg="#1e1e2e")

    player1 = HumanPlayer(mark="X")
    player2 = HumanPlayer(mark="O")

    game = Game(root, player1, player2)
    game.play()
    root.mainloop()

def main_menu():
    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.geometry("450x500")
    root.configure(bg="#1e1e2e")
    root.resizable(False, False)

    title_font = tkfont.Font(family="Segoe UI", size=40, weight="bold")
    button_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")

    title_label = tk.Label(
        root,
        text="Tic Tac Toe",
        font=title_font,
        bg="#1e1e2e",
        fg="#ffffff"
    )
    title_label.pack(pady=50)

    buttons_frame = tk.Frame(root, bg="#1e1e2e")
    buttons_frame.pack(pady=20)

    play_human_button = tk.Button(
        buttons_frame,
        text="👥 Two Players",
        font=button_font,
        bg="#6c5ce7",
        fg="#ffffff",
        activebackground="#5b4cc4",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        width=20,
        pady=15,
        command=lambda: [root.destroy(), play_human_vs_human()]
    )
    play_human_button.pack(pady=10)

    play_bot_button = tk.Button(
        buttons_frame,
        text="🤖 Play vs AI",
        font=button_font,
        bg="#00b894",
        fg="#ffffff",
        activebackground="#00a383",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        width=20,
        pady=15,
        command=lambda: [root.destroy(), play_human_vs_QPlayer()]
    )
    play_bot_button.pack(pady=10)

    train_button = tk.Button(
        buttons_frame,
        text="🎓 Train AI",
        font=button_font,
        bg="#e17055",
        fg="#ffffff",
        activebackground="#d65d42",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        width=20,
        pady=15,
        command=lambda: [root.destroy(), train_QPlayer()]
    )
    train_button.pack(pady=10)

    exit_button = tk.Button(
        buttons_frame,
        text="❌ Exit",
        font=button_font,
        bg="#636e72",
        fg="#ffffff",
        activebackground="#52565a",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        width=20,
        pady=15,
        command=root.destroy
    )
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
