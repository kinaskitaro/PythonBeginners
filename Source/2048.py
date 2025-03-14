import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.grid = [[0] * 4 for _ in range(4)]
        self.animation_speed = 50  # Speed of animation in milliseconds
        self.score = 0
        self.highscore = 0
        self.create_widgets()
        self.create_score_widgets()
        self.start_game()

    def create_widgets(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Label(self.master, text="", width=4, height=2, font=("Helvetica", 24), bg="lightgray", fg="black", borderwidth=2, relief="groove")
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)
        self.master.bind("<Key>", self.key_pressed)

    def create_score_widgets(self):
        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.grid(row=4, column=0, columnspan=2)
        self.highscore_label = tk.Label(self.master, text=f"High Score: {self.highscore}", font=("Helvetica", 16))
        self.highscore_label.grid(row=4, column=2, columnspan=2)

    def start_game(self):
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
                self.cells[i][j].config(text=str(value) if value != 0 else "", bg=self.get_color(value))
        self.update_score()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.highscore_label.config(text=f"High Score: {self.highscore}")

    def get_color(self, value):
        colors = {
            0: "lightgray", 2: "lightyellow", 4: "lightgoldenrodyellow", 8: "orange", 16: "darkorange",
            32: "tomato", 64: "red", 128: "yellow", 256: "gold", 512: "lightgreen", 1024: "green", 2048: "blue"
        }
        return colors.get(value, "black")

    def key_pressed(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.move(event.keysym)
            self.master.after(self.animation_speed, self.add_new_tile)
            self.master.after(self.animation_speed, self.update_grid)
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
                if direction == "Up":
                    new_col = slide(combine(slide(col)))
                else:
                    new_col = slide(combine(slide(col[::-1])))[::-1]
                if col != new_col:
                    moved = True
                for j in range(4):
                    self.grid[j][i] = new_col[j]
            else:
                row = self.grid[i]
                if direction == "Left":
                    new_row = slide(combine(slide(row)))
                else:
                    new_row = slide(combine(slide(row[::-1])))[::-1]
                if row != new_row:
                    moved = True
                self.grid[i] = new_row

        if moved:
            self.animate_move()
            if self.score > self.highscore:
                self.highscore = self.score

    def animate_move(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                self.cells[i][j].config(text=str(value) if value != 0 else "", bg=self.get_color(value))
        self.master.after(self.animation_speed, self.update_grid)

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
        game_over_label = tk.Label(self.master, text="Game Over!", font=("Helvetica", 24), bg="red", fg="white")
        game_over_label.grid(row=2, column=0, columnspan=4, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
