import tkinter as tk
from tkinter import font as tkfont
import random
import json
import os
from typing import List, Optional

class TetrisGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetris")
        self.root.geometry("550x700")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
        
        # Constants
        self.BOARD_WIDTH = 10
        self.BOARD_HEIGHT = 20
        self.CELL_SIZE = 28
        self.HIGH_SCORES_FILE = "tetris_high_scores.json"
        
        # Colors for different pieces
        self.PIECE_COLORS = {
            'I': '#00f5ff',
            'O': '#ffea00',
            'T': '#b829ff',
            'S': '#00ff5f',
            'Z': '#ff5f00',
            'L': '#ffaa00',
            'J': '#0055ff'
        }
        
        # Shape definitions
        self.SHAPES = {
            'I': [[1, 1, 1, 1]],
            'O': [[1, 1], [1, 1]],
            'T': [[0, 1, 0], [1, 1, 1]],
            'S': [[0, 1, 1], [1, 1, 0]],
            'Z': [[1, 1, 0], [0, 1, 1]],
            'L': [[1, 1, 1], [1, 0, 0]],
            'J': [[1, 1, 1], [0, 0, 1]]
        }
        
        # Game state
        self.board: List[List[Optional[str]]] = [[None for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        self.current_piece: Optional[str] = None
        self.current_x: int = 0
        self.current_y: int = 0
        self.current_color: str = ""
        self.next_piece: Optional[str] = None
        self.next_piece_color: str = ""
        
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.auto_drop_active = False
        
        self.high_scores = self.load_high_scores()
        self.high_score = max([s['score'] for s in self.high_scores]) if self.high_scores else 0
        
        self.create_ui()
        self.draw_initial_state()
        
    def load_high_scores(self):
        if os.path.exists(self.HIGH_SCORES_FILE):
            try:
                with open(self.HIGH_SCORES_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_high_scores(self):
        with open(self.HIGH_SCORES_FILE, 'w') as f:
            json.dump(self.high_scores, f)
    
    def create_ui(self):
        title_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        label_font = tkfont.Font(family="Segoe UI", size=12)
        score_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        
        # Header
        header_frame = tk.Frame(self.root, bg="#1e1e2e")
        header_frame.pack(pady=15)
        
        title_label = tk.Label(
            header_frame,
            text="TETRIS",
            font=title_font,
            bg="#1e1e2e",
            fg="#ff00ff"
        )
        title_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack()
        
        # Game board frame
        board_frame = tk.Frame(
            main_frame,
            bg="#0d1117",
            highlightbackground="#30363d",
            highlightthickness=2
        )
        board_frame.pack(side=tk.LEFT, padx=15)
        
        board_width = self.BOARD_WIDTH * self.CELL_SIZE
        board_height = self.BOARD_HEIGHT * self.CELL_SIZE
        
        self.canvas = tk.Canvas(
            board_frame,
            width=board_width,
            height=board_height,
            bg="#0d1117",
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Right panel
        right_panel = tk.Frame(main_frame, bg="#1e1e2e", padx=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Next piece preview
        next_frame = tk.Frame(right_panel, bg="#2d2d44", padx=10, pady=10)
        next_frame.pack(pady=10)
        
        tk.Label(
            next_frame,
            text="NEXT",
            font=tkfont.Font(family="Segoe UI", size=12, weight="bold"),
            bg="#2d2d44",
            fg="#a0a0a0"
        ).pack()
        
        self.next_canvas = tk.Canvas(
            next_frame,
            width=100,
            height=100,
            bg="#2d2d44",
            highlightthickness=0
        )
        self.next_canvas.pack(pady=5)
        
        # Score section
        score_frame = tk.Frame(right_panel, bg="#2d2d44", padx=15, pady=15)
        score_frame.pack(pady=5)
        
        tk.Label(
            score_frame,
            text="SCORE",
            font=tkfont.Font(family="Segoe UI", size=11),
            bg="#2d2d44",
            fg="#a0a0a0"
        ).pack()
        self.score_label = tk.Label(
            score_frame,
            text="0",
            font=tkfont.Font(family="Segoe UI", size=20, weight="bold"),
            bg="#2d2d44",
            fg="#00ff5f"
        )
        self.score_label.pack()
        
        tk.Label(
            score_frame,
            text="LEVEL",
            font=tkfont.Font(family="Segoe UI", size=11),
            bg="#2d2d44",
            fg="#a0a0a0"
        ).pack(pady=(10, 0))
        self.level_label = tk.Label(
            score_frame,
            text="1",
            font=tkfont.Font(family="Segoe UI", size=18, weight="bold"),
            bg="#2d2d44",
            fg="#ffea00"
        )
        self.level_label.pack()
        
        tk.Label(
            score_frame,
            text="HIGH SCORE",
            font=tkfont.Font(family="Segoe UI", size=11),
            bg="#2d2d44",
            fg="#a0a0a0"
        ).pack(pady=(10, 0))
        self.high_score_label = tk.Label(
            score_frame,
            text=str(self.high_score),
            font=tkfont.Font(family="Segoe UI", size=14, weight="bold"),
            bg="#2d2d44",
            fg="#ff0055"
        )
        self.high_score_label.pack()
        
        # Controls
        controls_frame = tk.Frame(right_panel, bg="#1e1e2e")
        controls_frame.pack(pady=10)
        
        controls = [
            "← → : Move",
            "↑ : Rotate",
            "↓ : Soft Drop",
            "Space : Hard Drop",
            "P : Pause"
        ]
        
        for control in controls:
            tk.Label(
                controls_frame,
                text=control,
                font=tkfont.Font(family="Segoe UI", size=10),
                bg="#1e1e2e",
                fg="#6b7280"
            ).pack(anchor="w")
        
        # Start button
        self.start_button = tk.Button(
            right_panel,
            text="START",
            font=tkfont.Font(family="Segoe UI", size=12, weight="bold"),
            bg="#00ff5f",
            fg="#0d1117",
            activebackground="#00cc4d",
            activeforeground="#0d1117",
            relief="flat",
            cursor="hand2",
            command=self.start_game,
            width=15,
            pady=8
        )
        self.start_button.pack(pady=10)
        
        # Key bindings
        self.root.bind("<Key>", self.on_key_press)
    
    def spawn_piece(self):
        if self.next_piece:
            self.current_piece = self.next_piece
            self.current_color = self.next_piece_color
        else:
            self.current_piece = random.choice(list(self.SHAPES.keys()))
            self.current_color = self.PIECE_COLORS[self.current_piece]
        
        self.next_piece = random.choice(list(self.SHAPES.keys()))
        self.next_piece_color = self.PIECE_COLORS[self.next_piece]
        
        shape = self.SHAPES[self.current_piece]
        self.current_x = (self.BOARD_WIDTH - len(shape[0])) // 2
        self.current_y = 0
        
        self.draw_next_piece()
        
        if self.check_collision(self.current_x, self.current_y, shape):
            self.game_over = True
            self.auto_drop_active = False
            self.show_game_over()
    
    def draw_initial_state(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_board()
        
        # Draw start message
        self.canvas.create_text(
            (self.BOARD_WIDTH * self.CELL_SIZE) // 2,
            (self.BOARD_HEIGHT * self.CELL_SIZE) // 2,
            text="Press START",
            fill="#6b7280",
            font=tkfont.Font(family="Segoe UI", size=16, weight="bold")
        )
        
        self.draw_next_piece()
    
    def draw_grid(self):
        for x in range(1, self.BOARD_WIDTH):
            self.canvas.create_line(
                x * self.CELL_SIZE, 0,
                x * self.CELL_SIZE, self.BOARD_HEIGHT * self.CELL_SIZE,
                fill="#161b22"
            )
        for y in range(1, self.BOARD_HEIGHT):
            self.canvas.create_line(
                0, y * self.CELL_SIZE,
                self.BOARD_WIDTH * self.CELL_SIZE, y * self.CELL_SIZE,
                fill="#161b22"
            )
    
    def draw_board(self):
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                if self.board[y][x]:
                    self.draw_cell(x, y, self.board[y][x])
    
    def draw_cell(self, x, y, color):
        self.canvas.create_rectangle(
            x * self.CELL_SIZE + 1,
            y * self.CELL_SIZE + 1,
            (x + 1) * self.CELL_SIZE - 1,
            (y + 1) * self.CELL_SIZE - 1,
            fill=color,
            outline="",
            tags="cell"
        )
        # Add highlight effect
        self.canvas.create_rectangle(
            x * self.CELL_SIZE + 2,
            y * self.CELL_SIZE + 2,
            (x + 1) * self.CELL_SIZE - 2,
            y * self.CELL_SIZE + 8,
            fill="",
            outline="#ffffff",
            width=1,
            tags="cell"
        )
    
    def draw_current_piece(self):
        if not self.current_piece:
            return
        shape = self.SHAPES[self.current_piece]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_cell(
                        self.current_x + x,
                        self.current_y + y,
                        self.current_color
                    )
    
    def draw_next_piece(self):
        self.next_canvas.delete("all")
        if not self.next_piece:
            return
        
        shape = self.SHAPES[self.next_piece]
        cell_size = 20
        offset_x = (100 - len(shape[0]) * cell_size) // 2
        offset_y = (100 - len(shape) * cell_size) // 2
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    px = offset_x + x * cell_size
                    py = offset_y + y * cell_size
                    self.next_canvas.create_rectangle(
                        px, py, px + cell_size - 2, py + cell_size - 2,
                        fill=self.next_piece_color,
                        outline=""
                    )
                    self.next_canvas.create_rectangle(
                        px + 1, py + 1, px + cell_size - 3, py + 6,
                        fill="",
                        outline="#ffffff",
                        width=1
                    )
    
    def update_display(self):
        self.canvas.delete("cell")
        self.draw_board()
        if not self.game_over and self.current_piece:
            self.draw_current_piece()
        
        if self.paused:
            self.canvas.create_text(
                (self.BOARD_WIDTH * self.CELL_SIZE) // 2,
                (self.BOARD_HEIGHT * self.CELL_SIZE) // 2,
                text="PAUSED",
                fill="#ffffff",
                font=tkfont.Font(family="Segoe UI", size=24, weight="bold")
            )
    
    def check_collision(self, x, y, shape):
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    new_x = x + col_idx
                    new_y = y + row_idx
                    
                    if new_x < 0 or new_x >= self.BOARD_WIDTH:
                        return True
                    if new_y >= self.BOARD_HEIGHT:
                        return True
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return True
        return False
    
    def rotate_piece(self):
        if not self.current_piece:
            return
        shape = self.SHAPES[self.current_piece]
        rotated = [list(row) for row in zip(*shape[::-1])]
        
        if not self.check_collision(self.current_x, self.current_y, rotated):
            self.SHAPES[self.current_piece] = rotated
            self.update_display()
    
    def move_piece(self, dx, dy):
        if self.game_over or self.paused or not self.current_piece:
            return
        
        new_x = self.current_x + dx
        new_y = self.current_y + dy
        shape = self.SHAPES[self.current_piece]
        
        if not self.check_collision(new_x, new_y, shape):
            self.current_x = new_x
            self.current_y = new_y
            self.update_display()
            return True
        elif dy > 0:
            self.lock_piece()
            return False
        return False
    
    def hard_drop(self):
        if self.game_over or self.paused:
            return
        
        while self.move_piece(0, 1):
            self.score += 2
            self.update_score_display()
    
    def lock_piece(self):
        if not self.current_piece:
            return
        shape = self.SHAPES[self.current_piece]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_x + x
                    board_y = self.current_y + y
                    if 0 <= board_y < self.BOARD_HEIGHT and 0 <= board_x < self.BOARD_WIDTH:
                        self.board[board_y][board_x] = self.current_color
        
        self.clear_lines()
        self.spawn_piece()
        self.update_display()
    
    def clear_lines(self):
        lines_to_clear = []
        
        for y in range(self.BOARD_HEIGHT):
            if all(self.board[y]):
                lines_to_clear.append(y)
        
        for y in sorted(lines_to_clear, reverse=True):
            del self.board[y]
            self.board.insert(0, [None for _ in range(self.BOARD_WIDTH)])
        
        if lines_to_clear:
            lines_count = len(lines_to_clear)
            self.lines_cleared += lines_count
            
            # Scoring: 100, 300, 500, 800 points for 1, 2, 3, 4 lines
            points = [0, 100, 300, 500, 800]
            self.score += points[lines_count] * self.level
            
            # Level up every 10 lines
            self.level = self.lines_cleared // 10 + 1
            self.high_score = max(self.high_score, self.score)
            
            self.update_score_display()
    
    def update_score_display(self):
        self.score_label.config(text=str(self.score))
        self.level_label.config(text=str(self.level))
        self.high_score_label.config(text=str(self.high_score))
    
    def auto_drop(self):
        if not self.auto_drop_active or self.game_over:
            return
        
        if not self.paused:
            self.move_piece(0, 1)
        
        drop_speed = max(100, 1000 - (self.level - 1) * 100)
        self.root.after(drop_speed, self.auto_drop)
    
    def start_game(self):
        self.board = [[None for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.auto_drop_active = True
        
        self.update_score_display()
        self.start_button.config(text="RESTART")
        
        self.spawn_piece()
        self.update_display()
        self.auto_drop()
    
    def show_game_over(self):
        self.update_display()
        
        overlay = tk.Frame(self.root, bg="rgba(0,0,0,0.8)")
        
        self.canvas.create_text(
            (self.BOARD_WIDTH * self.CELL_SIZE) // 2,
            (self.BOARD_HEIGHT * self.CELL_SIZE) // 2 - 30,
            text="GAME OVER",
            fill="#ff0055",
            font=tkfont.Font(family="Segoe UI", size=24, weight="bold")
        )
        self.canvas.create_text(
            (self.BOARD_WIDTH * self.CELL_SIZE) // 2,
            (self.BOARD_HEIGHT * self.CELL_SIZE) // 2 + 10,
            text=f"Score: {self.score}",
            fill="#ffffff",
            font=tkfont.Font(family="Segoe UI", size=16)
        )
        
        self.save_high_score()
    
    def save_high_score(self):
        name = f"Player{len(self.high_scores) + 1}"
        self.high_scores.append({'name': name, 'score': self.score})
        self.high_scores = sorted(self.high_scores, key=lambda x: x['score'], reverse=True)[:10]
        self.save_high_scores()
    
    def toggle_pause(self):
        if self.game_over or not self.auto_drop_active:
            return
        
        self.paused = not self.paused
        self.update_display()
    
    def on_key_press(self, event):
        if event.keysym.lower() == 'p':
            self.toggle_pause()
            return
        
        if self.game_over or self.paused:
            return
        
        if event.keysym == 'Left':
            self.move_piece(-1, 0)
        elif event.keysym == 'Right':
            self.move_piece(1, 0)
        elif event.keysym == 'Down':
            self.move_piece(0, 1)
            self.score += 1
            self.update_score_display()
        elif event.keysym == 'Up':
            self.rotate_piece()
        elif event.keysym == 'space':
            self.hard_drop()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()
