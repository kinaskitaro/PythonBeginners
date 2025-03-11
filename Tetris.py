import tkinter as tk
import random

# Constants
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 30
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
root.geometry(f"{BOARD_WIDTH * CELL_SIZE}x{BOARD_HEIGHT * CELL_SIZE}")
root.configure(bg="#000000")

# Create the canvas for the game board
canvas = tk.Canvas(root, width=BOARD_WIDTH * CELL_SIZE, height=BOARD_HEIGHT * CELL_SIZE, bg="#000000")
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
high_score = 0
speed_level = 1
game_over_flag = False

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
    canvas.create_text(BOARD_WIDTH * CELL_SIZE // 2, 10, text=f"Score: {score}", fill="yellow", font=("Helvetica", 16, "bold"))
    canvas.create_text(BOARD_WIDTH * CELL_SIZE // 2, 30, text=f"High Score: {high_score}", fill="yellow", font=("Helvetica", 16, "bold"))
    canvas.create_text(BOARD_WIDTH * CELL_SIZE // 2, 50, text=f"Speed Level: {speed_level}", fill="yellow", font=("Helvetica", 16, "bold"))

def auto_drop():
    if not game_over_flag:
        move_shape(0, 1)
        root.after(750 // speed_level, auto_drop)

def move_shape(dx, dy):
    global current_x, current_y, current_shape, board, score, speed_level
    if game_over_flag:
        return
    new_x = current_x + dx
    new_y = current_y + dy
    if not check_collision(new_x, new_y, current_shape):
        current_x = new_x
        current_y = new_y
    else:
        if dy > 0:  # If the collision is due to downward movement
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
    global high_score, score, speed_level, game_over_flag
    game_over_flag = True
    if score > high_score:
        high_score = score
    canvas.delete("all")
    draw_grid()
    draw_border()
    draw_board()
    draw_score()
    canvas.create_text(BOARD_WIDTH * CELL_SIZE // 2, BOARD_HEIGHT * CELL_SIZE // 2, text="Game Over", fill="red", font=("Helvetica", 24, "bold"))
    canvas.create_text(BOARD_WIDTH * CELL_SIZE // 2, BOARD_HEIGHT * CELL_SIZE // 2 + 30, text="Press Space to Replay", fill="white", font=("Helvetica", 16, "bold"))
    root.update()
    root.bind("<Key>", on_key_press_game_over)

def on_key_press_game_over(event):
    if event.keysym == "space":
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

def on_key_press(event):
    if event.keysym == "Left":
        move_shape(-1, 0)
    elif event.keysym == "Right":
        move_shape(1, 0)
    elif event.keysym == "Down":
        move_shape(0, 1)
    elif event.keysym == "Up":
        rotate_shape()

# Bind key events
root.bind("<Key>", on_key_press)

# Start the game
draw_shape()
auto_drop()
root.mainloop()
