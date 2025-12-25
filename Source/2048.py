import tkinter as tk
from tkinter import messagebox
import random
import json
import os

HIGHSCORE_FILE = "2048_highscore.json"

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.master.geometry("600x700")
        self.master.resizable(False, False)
        self.master.configure(bg="#faf8ef")
        
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.highscore = self.load_highscore()
        self.is_game_over = False
        self.has_won = False
        self.game_over_widgets = []
        
        self.create_widgets()
        self.start_game()
    
    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('highscore', 0)
            except (json.JSONDecodeError, IOError):
                pass
        return 0
    
    def save_highscore(self):
        try:
            with open(HIGHSCORE_FILE, 'w') as f:
                json.dump({'highscore': self.highscore}, f)
        except IOError:
            pass

    def create_widgets(self):
        header_frame = tk.Frame(self.master, bg="#faf8ef")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=8)
        
        title_label = tk.Label(header_frame, text="2048", font=("Arial", 42, "bold"), bg="#faf8ef", fg="#776e65")
        title_label.pack(side="left")
        
        score_frame = tk.Frame(header_frame, bg="#bbada0", padx=12, pady=4)
        score_frame.pack(side="right")
        
        tk.Label(score_frame, text="SCORE", font=("Arial", 9, "bold"), bg="#bbada0", fg="#eee4da").pack()
        self.score_label = tk.Label(score_frame, text=str(self.score), font=("Arial", 16, "bold"), bg="#bbada0", fg="white")
        self.score_label.pack()
        
        highscore_frame = tk.Frame(header_frame, bg="#bbada0", padx=12, pady=4)
        highscore_frame.pack(side="right", padx=(0, 8))
        
        tk.Label(highscore_frame, text="BEST", font=("Arial", 9, "bold"), bg="#bbada0", fg="#eee4da").pack()
        self.highscore_label = tk.Label(highscore_frame, text=str(self.highscore), font=("Arial", 16, "bold"), bg="#bbada0", fg="white")
        self.highscore_label.pack()
        
        tk.Label(self.master, text="Join the numbers and get to the 2048 tile!", 
                font=("Arial", 10), bg="#faf8ef", fg="#776e65").grid(row=1, column=0, pady=(0, 6))
        
        new_game_btn = tk.Button(self.master, text="New Game", font=("Arial", 11, "bold"), 
                                bg="#8f7a66", fg="white", activebackground="#9f8a76", 
                                relief="flat", padx=18, pady=4, command=self.restart_game)
        new_game_btn.grid(row=2, column=0, pady=(0, 8))
        
        game_frame = tk.Frame(self.master, bg="#bbada0", padx=6, pady=6)
        game_frame.grid(row=3, column=0)
        
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Label(game_frame, text="", width=7, height=3, 
                              font=("Arial", 24, "bold"), bg="#cdc1b4", 
                              fg="#776e65", relief="flat")
                cell.grid(row=i, column=j, padx=4, pady=4)
                row.append(cell)
            self.cells.append(row)
        
        tk.Label(self.master, text="Use Arrow Keys or WASD to move tiles", 
                font=("Arial", 8), bg="#faf8ef", fg="#776e65").grid(row=4, column=0, pady=(8, 5))
        
        self.master.bind("<Key>", self.key_pressed)

    def start_game(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.is_game_over = False
        self.has_won = False
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                bg_color, fg_color = self.get_colors(value)
                if value == 0:
                    font_size = 24
                elif value < 100:
                    font_size = 24
                elif value < 1000:
                    font_size = 20
                elif value < 10000:
                    font_size = 16
                else:
                    font_size = 14
                self.cells[i][j].config(text=str(value) if value != 0 else "", 
                                       bg=bg_color, fg=fg_color,
                                       font=("Arial", font_size, "bold"))
        self.update_score()

    def update_score(self):
        self.score_label.config(text=str(self.score))
        self.highscore_label.config(text=str(self.highscore))

    def get_colors(self, value):
        colors = {
            0: ("#cdc1b4", "#776e65"),
            2: ("#eee4da", "#776e65"),
            4: ("#ede0c8", "#776e65"),
            8: ("#f2b179", "#f9f6f2"),
            16: ("#f59563", "#f9f6f2"),
            32: ("#f67c5f", "#f9f6f2"),
            64: ("#f65e3b", "#f9f6f2"),
            128: ("#edcf72", "#f9f6f2"),
            256: ("#edcc61", "#f9f6f2"),
            512: ("#edc850", "#f9f6f2"),
            1024: ("#edc53f", "#f9f6f2"),
            2048: ("#edc22e", "#f9f6f2"),
            4096: ("#3c3a32", "#f9f6f2"),
            8192: ("#3c3a32", "#f9f6f2")
        }
        return colors.get(value, ("#3c3a32", "#f9f6f2"))

    def key_pressed(self, event):
        if self.is_game_over:
            return
        key_map = {"Up": "Up", "Down": "Down", "Left": "Left", "Right": "Right",
                   "w": "Up", "s": "Down", "a": "Left", "d": "Right",
                   "W": "Up", "S": "Down", "A": "Left", "D": "Right"}
        direction = key_map.get(event.keysym)
        if direction:
            moved = self.move(direction)
            if moved:
                self.add_new_tile()
                self.update_grid()
                self.check_win()
                if self.check_game_over():
                    self.game_over()

    def move(self, direction):
        def slide(row):
            new_row = [i for i in row if i != 0]
            new_row += [0] * (4 - len(new_row))
            return new_row

        def combine(row):
            for i in range(3):
                if row[i] == row[i + 1] and row[i] != 0:
                    row[i] *= 2
                    self.score += row[i]
                    row[i + 1] = 0
            return row

        moved = False
        for i in range(4):
            if direction in ["Up", "Down"]:
                col = [self.grid[j][i] for j in range(4)]
                original_col = col[:]
                if direction == "Up":
                    new_col = slide(combine(slide(col)))
                else:
                    new_col = slide(combine(slide(col[::-1])))[::-1]
                if original_col != new_col:
                    moved = True
                for j in range(4):
                    self.grid[j][i] = new_col[j]
            else:
                row = self.grid[i][:]
                original_row = row[:]
                if direction == "Left":
                    new_row = slide(combine(slide(row)))
                else:
                    new_row = slide(combine(slide(row[::-1])))[::-1]
                if original_row != new_row:
                    moved = True
                self.grid[i] = new_row

        if moved:
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()
        
        return moved

    def check_win(self):
        if not self.has_won:
            for i in range(4):
                for j in range(4):
                    if self.grid[i][j] == 2048:
                        self.has_won = True
                        messagebox.showinfo("Congratulations!", "You reached 2048!\n\nYou can continue playing to get higher scores!")
                        return True
        return False

    def check_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
                if j < 3 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        return True

    def game_over(self):
        self.is_game_over = True
        
        overlay_frame = tk.Frame(self.master, bg="#eee4da", bd=3, relief="raised")
        overlay_frame.place(relx=0.5, rely=0.55, anchor="center", width=240, height=130)
        
        tk.Label(overlay_frame, text="Game Over!", font=("Arial", 22, "bold"), 
                bg="#eee4da", fg="#776e65").pack(pady=(15, 8))
        
        restart_btn = tk.Button(overlay_frame, text="Try Again", font=("Arial", 12, "bold"), 
                               bg="#8f7a66", fg="white", activebackground="#9f8a76",
                               relief="flat", padx=25, pady=6, command=self.restart_game)
        restart_btn.pack(pady=(5, 12))
        
        self.game_over_widgets = [overlay_frame]
    
    def restart_game(self):
        for widget in self.game_over_widgets:
            widget.destroy()
        self.game_over_widgets = []
        self.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
