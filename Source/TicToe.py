import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        self.player = 'X'
        self.bot_mode = False
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.move_count = 0
        self.show_mode_selection()

    def show_mode_selection(self):
        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack()
        tk.Label(self.mode_frame, text="Choose Game Mode", font=('Arial', 20)).pack()
        tk.Button(self.mode_frame, text="Play with Bot", font=('Arial', 15), command=self.start_bot_mode).pack(pady=10)
        tk.Button(self.mode_frame, text="Play with Another User", font=('Arial', 15), command=self.start_user_mode).pack(pady=10)

    def start_bot_mode(self):
        self.bot_mode = True
        self.mode_frame.destroy()
        self.create_board()

    def start_user_mode(self):
        self.bot_mode = False
        self.mode_frame.destroy()
        self.create_board()

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text='', font=('Arial', 40), width=5, height=2,
                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def on_button_click(self, row, col):
        if self.buttons[row][col]['text'] == '' and not self.check_winner():
            self.buttons[row][col]['text'] = self.player
            self.move_count += 1
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
                self.reset_board()
                return  # Stop further execution after a win
            elif self.check_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_board()
                return  # Stop further execution after a draw
            else:
                if self.bot_mode and self.player == 'X':  # Ensure bot plays after user
                    self.player = 'O'
                    self.bot_move()
                else:
                    self.player = 'O' if self.player == 'X' else 'X'

    def bot_move(self):
        if self.check_winner() or self.check_draw():
            return  # Prevent bot from playing if the game is already over
        if self.try_to_win_or_block('O'):
            self.move_count += 1  # Increment move count for bot
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_board()
            else:
                self.player = 'X'  # Switch back to user
            return
        if self.try_to_win_or_block('X'):
            self.move_count += 1  # Increment move count for bot
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_board()
            else:
                self.player = 'X'  # Switch back to user
            return
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.buttons[r][c]['text'] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.buttons[row][col]['text'] = self.player
            self.move_count += 1  # Increment move count for bot
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_board()
            else:
                self.player = 'X'  # Switch back to user

    def try_to_win_or_block(self, mark):
        for row in range(3):
            if self.buttons[row][0]['text'] == self.buttons[row][1]['text'] == mark and self.buttons[row][2]['text'] == '':
                self.buttons[row][2]['text'] = self.player
                return True
            if self.buttons[row][0]['text'] == self.buttons[row][2]['text'] == mark and self.buttons[row][1]['text'] == '':
                self.buttons[row][1]['text'] = self.player
                return True
            if self.buttons[row][1]['text'] == self.buttons[row][2]['text'] == mark and self.buttons[row][0]['text'] == '':
                self.buttons[row][0]['text'] = self.player
                return True
        for col in range(3):
            if self.buttons[0][col]['text'] == self.buttons[1][col]['text'] == mark and self.buttons[2][col]['text'] == '':
                self.buttons[2][col]['text'] = self.player
                return True
            if self.buttons[0][col]['text'] == self.buttons[2][col]['text'] == mark and self.buttons[1][col]['text'] == '':
                self.buttons[1][col]['text'] = self.player
                return True
            if self.buttons[1][col]['text'] == self.buttons[2][col]['text'] == mark and self.buttons[0][col]['text'] == '':
                self.buttons[0][col]['text'] = self.player
                return True
        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == mark and self.buttons[2][2]['text'] == '':
            self.buttons[2][2]['text'] = self.player
            return True
        if self.buttons[0][0]['text'] == self.buttons[2][2]['text'] == mark and self.buttons[1][1]['text'] == '':
            self.buttons[1][1]['text'] = self.player
            return True
        if self.buttons[1][1]['text'] == self.buttons[2][2]['text'] == mark and self.buttons[0][0]['text'] == '':
            self.buttons[0][0]['text'] = self.player
            return True
        if self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == mark and self.buttons[2][0]['text'] == '':
            self.buttons[2][0]['text'] = self.player
            return True
        if self.buttons[0][2]['text'] == self.buttons[2][0]['text'] == mark and self.buttons[1][1]['text'] == '':
            self.buttons[1][1]['text'] = self.player
            return True
        if self.buttons[1][1]['text'] == self.buttons[2][0]['text'] == mark and self.buttons[0][2]['text'] == '':
            self.buttons[0][2]['text'] = self.player
            return True
        return False

    def check_winner(self):
        for row in range(3):
            if self.buttons[row][0]['text'] == self.buttons[row][1]['text'] == self.buttons[row][2]['text'] != '':
                return True
        for col in range(3):
            if self.buttons[0][col]['text'] == self.buttons[1][col]['text'] == self.buttons[2][col]['text'] != '':
                return True
        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != '':
            return True
        if self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == self.buttons[2][0]['text'] != '':
            return True
        return False

    def check_draw(self):
        for row in range(3):
            for col in range(3):
                if self.buttons[row][col]['text'] == '':
                    return False
        return True

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]['text'] = ''
        self.player = 'X'
        self.move_count = 0

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
