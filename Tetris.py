import tkinter as tk
import random
import json
import os

# Constants
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 30
SIDE_PANEL_WIDTH = 200  # Added side panel width
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Initialize the main window
root = tk.Tk()
root.title("Tetris")
root.geometry(f"{(BOARD_WIDTH * CELL_SIZE) + SIDE_PANEL_WIDTH}x{BOARD_HEIGHT * CELL_SIZE}")
root.configure(bg="#000000")

# High scores file
HIGH_SCORES_FILE = "high_scores.json"

# Load high scores
def load_high_scores():
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, "r") as file:
            return json.load(file)
    return []

# Save high scores
def save_high_scores(high_scores):
    with open(HIGH_SCORES_FILE, "w") as file:
        json.dump(high_scores, file)

# Get top 10 high scores
def get_top_high_scores():
    high_scores = load_high_scores()
    high_scores.sort(key=lambda x: x["score"], reverse=True)
    return high_scores[:10]

# Create the canvas for the game board
canvas = tk.Canvas(root, width=(BOARD_WIDTH * CELL_SIZE) + SIDE_PANEL_WIDTH, 
                  height=BOARD_HEIGHT * CELL_SIZE, bg="#000000")
canvas.pack()

# Draw grid lines
for i in range(BOARD_WIDTH):
    canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE, fill="#333333")
for i in range(BOARD_HEIGHT):
    canvas.create_line(0, i * CELL_SIZE, BOARD_WIDTH * CELL_SIZE, i * CELL_SIZE, fill="#333333")

# Game variables
board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
current_shape = random.choice(SHAPES)
current_x = BOARD_WIDTH // 2 - len(current_shape[0]) // 2
current_y = 0
score = 0
high_scores = get_top_high_scores()
high_score = high_scores[0]["score"] if high_scores else 0
speed_level = 1
game_over_flag = False
paused = False

def draw_shape():
    canvas.delete("all")
    draw_grid()
    draw_border()
    draw_board()
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell:
                canvas.create_rectangle(
                    (current_x + x) * CELL_SIZE, (current_y + y) * CELL_SIZE,
                    (current_x + x + 1) * CELL_SIZE, (current_y + y + 1) * CELL_SIZE,
                    fill="#00FF00", outline="#000000"
                )
    draw_score()

def draw_grid():
    for i in range(BOARD_WIDTH):
        canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE, fill="#333333")
    for i in range(BOARD_HEIGHT):
        canvas.create_line(0, i * CELL_SIZE, BOARD_WIDTH * CELL_SIZE, i * CELL_SIZE, fill="#333333")

def draw_border():
    canvas.create_rectangle(0, 0, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE, outline="#FFFFFF", width=2)

def draw_board():
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                canvas.create_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE,
                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                    fill="#00FF00", outline="#000000"
                )

def draw_score():
    # Score panel on the right side
    panel_x = BOARD_WIDTH * CELL_SIZE + (SIDE_PANEL_WIDTH // 2)
    
    # Move scores up slightly
    canvas.create_text(panel_x, 30, text=f"Score: {score}", 
                      fill="yellow", font=("Helvetica", 16, "bold"))
    
    # Get the best high score from the top 10 high scores
    best_high_score = max(high_scores, key=lambda x: x["score"])["score"] if high_scores else 0
    canvas.create_text(panel_x, 70, text=f"High Score: {best_high_score}", 
                      fill="yellow", font=("Helvetica", 16, "bold"))
    
    canvas.create_text(panel_x, 110, text=f"Speed Level: {speed_level}", 
                      fill="yellow", font=("Helvetica", 16, "bold"))
    
    # Adjust control text positions
    canvas.create_text(panel_x, (BOARD_HEIGHT * CELL_SIZE // 2) - 100,
                      text="Controls:", fill="white", font=("Helvetica", 14, "bold"))
    canvas.create_text(panel_x, (BOARD_HEIGHT * CELL_SIZE // 2) - 70,
                      text="←→ Move left/right", fill="white", font=("Helvetica", 12))
    canvas.create_text(panel_x, (BOARD_HEIGHT * CELL_SIZE // 2) - 50,
                      text="↑ Rotate", fill="white", font=("Helvetica", 12))
    canvas.create_text(panel_x, (BOARD_HEIGHT * CELL_SIZE // 2) - 30,
                      text="↓ Move down", fill="white", font=("Helvetica", 12))
    canvas.create_text(panel_x, (BOARD_HEIGHT * CELL_SIZE // 2) - 10,
                      text="P Pause game", fill="white", font=("Helvetica", 12))

    # Display top 10 high scores
    top_ten_x = panel_x - 50  # Move the top ten list to the left
    canvas.create_text(panel_x, (BOARD_HEIGHT * CELL_SIZE // 2) + 20,
                      text="Top 10 High Scores:", fill="white", font=("Helvetica", 14, "bold"))
    for index, high_score in enumerate(high_scores):
        canvas.create_text(top_ten_x, (BOARD_HEIGHT * CELL_SIZE // 2) + 50 + (index * 20),
                          text=f"{index + 1}. {high_score['name']}:\t {high_score['score']}", fill="white", font=("Helvetica", 14), anchor="w")

    if paused:
        canvas.create_text(BOARD_WIDTH * CELL_SIZE // 2, BOARD_HEIGHT * CELL_SIZE // 2,
                         text="PAUSED", fill="white", font=("Helvetica", 24, "bold"))
        canvas.create_text(BOARD_WIDTH * CELL_SIZE // 2, BOARD_HEIGHT * CELL_SIZE // 2 + 30,
                         text="Press P to resume", fill="white", font=("Helvetica", 16))

def auto_drop():
    if not game_over_flag and not paused:
        move_shape(0, 1)
    root.after(1000 // speed_level, auto_drop)

def move_shape(dx, dy, manual=False):
    global current_x, current_y, current_shape, board, score, speed_level
    if game_over_flag:
        return
    new_x = current_x + dx
    new_y = current_y + dy
    if not check_collision(new_x, new_y, current_shape):
        current_x = new_x
        current_y = new_y
    else:
        if dy > 0 and not manual:  # If the collision is due to downward movement and not manual
            place_shape()
            lines_cleared = clear_lines()
            score += lines_cleared * 1
            speed_level = score // 30 + 1
            current_shape = random.choice(SHAPES)
            current_x = BOARD_WIDTH // 2 - len(current_shape[0]) // 2
            current_y = 0
            if check_collision(current_x, current_y, current_shape):
                game_over()
    if not game_over_flag:
        canvas.delete("all")
        draw_shape()

def place_shape():
    global board, current_shape, current_x, current_y
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell:
                if 0 <= current_y + y < BOARD_HEIGHT and 0 <= current_x + x < BOARD_WIDTH:
                    board[current_y + y][current_x + x] = cell

def clear_lines():
    global board
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    new_board = [[0] * BOARD_WIDTH for _ in range(lines_cleared)] + new_board
    board = new_board
    return lines_cleared

def game_over():
    global high_score, score, speed_level, game_over_flag, entry_frame, name_entry
    game_over_flag = True
    if score > high_score:
        high_score = score
    canvas.delete("all")
    draw_grid()
    draw_border()
    draw_board()
    draw_score()
    canvas.create_text(BOARD_WIDTH * CELL_SIZE // 2, BOARD_HEIGHT * CELL_SIZE // 2, text="Game Over", fill="red", font=("Helvetica", 24, "bold"))
    canvas.create_text(BOARD_WIDTH * CELL_SIZE // 2, BOARD_HEIGHT * CELL_SIZE // 2 + 30, text="Enter your name:", fill="white", font=("Helvetica", 16, "bold"))
    
    # Create a frame for the entry widget and button
    entry_frame = tk.Frame(root, bg="#000000")
    entry_frame.place(x=BOARD_WIDTH * CELL_SIZE // 2 - 100, y=BOARD_HEIGHT * CELL_SIZE // 2 + 60, width=200, height=30)
    
    name_entry = tk.Entry(entry_frame, font=("Helvetica", 14))
    name_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    name_entry.focus_set()
    
    submit_button = tk.Button(entry_frame, text="Submit", command=submit_name, font=("Helvetica", 14))
    submit_button.pack(side=tk.RIGHT)
    
    name_entry.bind("<Return>", lambda event: submit_name())  # Bind Enter key to submit_name function
    
    root.update()
    root.bind("<Key>", on_key_press_game_over)

def submit_name():
    save_score(name_entry.get())

def save_score(name):
    global high_scores, entry_frame
    high_scores.append({"name": name, "score": score})
    high_scores = sorted(high_scores, key=lambda x: x["score"], reverse=True)[:10]
    save_high_scores(high_scores)
    entry_frame.destroy()  # Destroy the entry frame after submitting the score
    reset_game()

def reset_game():
    global board, current_shape, current_x, current_y, score, speed_level, game_over_flag
    canvas.delete("all")
    board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    current_shape = random.choice(SHAPES)
    current_x = BOARD_WIDTH // 2 - len(current_shape[0]) // 2
    current_y = 0
    score = 0
    speed_level = 1
    game_over_flag = False
    root.bind("<Key>", on_key_press)
    draw_shape()
    auto_drop()

def check_collision(x, y, shape):
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                if (x + col_index < 0 or x + col_index >= BOARD_WIDTH or
                        y + row_index >= BOARD_HEIGHT or
                        (y + row_index >= 0 and board[y + row_index][x + col_index])):
                    return True
    return False

def rotate_shape():
    global current_shape, current_x
    rotated_shape = [list(row) for row in zip(*current_shape[::-1])]
    if not check_collision(current_x, current_y, rotated_shape):
        current_shape = rotated_shape
    canvas.delete("all")
    draw_shape()

def toggle_pause():
    global paused
    paused = not paused
    draw_shape()

def on_key_press(event):
    if event.keysym == "p":
        toggle_pause()
        return
    if not paused:
        if event.keysym == "Left":
            move_shape(-1, 0)
        elif event.keysym == "Right":
            move_shape(1, 0)
        elif event.keysym == "Down":
            move_shape(0, 1, manual=True)
        elif event.keysym == "Up":
            rotate_shape()

def on_key_press_game_over(event):
    if event.keysym == "space":
        reset_game()

# Bind key events
root.bind("<Key>", on_key_press)

# Start the game
draw_shape()
auto_drop()
root.mainloop()
