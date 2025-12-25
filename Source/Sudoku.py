import numpy as np
import pygame
import time
import sys
import random
from typing import Optional, Tuple

# UI Constants
WIDTH = 850
HEIGHT = 650
BOARD_SIZE = 540
CELL_SIZE = 60
OFFSET_X = 20
OFFSET_Y = 70

# Colors - Modern dark theme
BG_COLOR = (30, 30, 40)
BOARD_BG = (45, 45, 60)
GRID_LIGHT = (70, 70, 90)
GRID_THICK = (100, 100, 120)
HIGHLIGHT_COLOR = (79, 172, 254, 100)
SAME_NUM_COLOR = (79, 172, 254, 50)
SELECTED_COLOR = (255, 215, 0, 150)
CORRECT_COLOR = (46, 204, 113)
WRONG_COLOR = (231, 76, 60)
ORIGINAL_NUM_COLOR = (255, 255, 255)
INPUT_NUM_COLOR = (52, 152, 219)
BUTTON_NORMAL = (52, 73, 94)
BUTTON_HOVER = (79, 172, 254)
BUTTON_CLICK = (41, 128, 185)
TEXT_COLOR = (236, 240, 241)
ACCENT_COLOR = (155, 89, 182)

# Difficulty Levels
EASY = 30
MEDIUM = 45
HARD = 60

class Sudoku:
    def __init__(self, board):
        self.board = np.array(board)
        self.original_board = self.board.copy()
        
        # Initialize pygame once
        if not pygame.font.get_init():
            pygame.init()
        
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku")
        
        # Fonts
        self.font_large = pygame.font.SysFont('Segoe UI', 36, bold=True)
        self.font_medium = pygame.font.SysFont('Segoe UI', 24, bold=True)
        self.font_small = pygame.font.SysFont('Segoe UI', 18)
        
        # Buttons
        self.buttons = {
            'easy': pygame.Rect(620, 100, 200, 50),
            'medium': pygame.Rect(620, 170, 200, 50),
            'hard': pygame.Rect(620, 240, 200, 50),
            'new': pygame.Rect(620, 320, 200, 50),
            'reset': pygame.Rect(620, 390, 200, 50),
            'check': pygame.Rect(620, 460, 200, 50),
            'menu': pygame.Rect(620, 530, 200, 50)
        }
        
        self.button_colors = {key: BUTTON_NORMAL for key in self.buttons}
        self.button_hovered = {key: False for key in self.buttons}
        
        # Game state
        self.selected_cell: Optional[Tuple[int, int]] = None
        self.number_counts = {i: 9 for i in range(1, 10)}
        self.update_number_counts()
        
        # Timer
        self.start_time = time.time()
        self.elapsed_time = 0
        self.timer_running = True
        
        # Game state
        self.puzzle_solved = False
        self.difficulty = MEDIUM
        self.show_mistakes = False
        
        # Particles for celebration
        self.particles = []
        
        self.draw_board()
    
    def is_valid(self, num: int, pos: Tuple[int, int]) -> bool:
        row, col = pos
        
        # Check row
        for i in range(9):
            if self.board[row][i] == num and i != col:
                return False
        
        # Check column
        for i in range(9):
            if self.board[i][col] == num and i != row:
                return False
        
        # Check 3x3 box
        box_row, box_col = row // 3, col // 3
        for i in range(box_row * 3, box_row * 3 + 3):
            for j in range(box_col * 3, box_col * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False
        
        return True
    
    def solve(self) -> bool:
        empty = self.find_empty()
        if not empty:
            return True
        
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        
        return False
    
    def find_empty(self) -> Optional[Tuple[int, int]]:
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def update_number_counts(self):
        self.number_counts = {i: 9 for i in range(1, 10)}
        for i in range(9):
            for j in range(9):
                num = abs(self.board[i][j])
                if num != 0:
                    self.number_counts[num] -= 1
    
    def draw_rounded_rect(self, surface, color, rect, radius=10, width=0):
        pygame.draw.rect(surface, color, rect, width, border_radius=radius)
    
    def draw_button(self, key: str, text: str):
        rect = self.buttons[key]
        color = self.button_colors[key]
        
        if self.button_hovered.get(key, False):
            color = BUTTON_HOVER
        
        self.draw_rounded_rect(self.window, color, rect, radius=10)
        
        text_surface = self.font_medium.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        self.window.blit(text_surface, text_rect)
    
    def draw_grid(self):
        # Draw board background
        board_rect = pygame.Rect(OFFSET_X, OFFSET_Y, BOARD_SIZE, BOARD_SIZE)
        self.draw_rounded_rect(self.window, BOARD_BG, board_rect, radius=15)
        
        # Draw grid lines
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            color = GRID_THICK if i % 3 == 0 else GRID_LIGHT
            
            # Vertical lines
            x = OFFSET_X + i * CELL_SIZE
            pygame.draw.line(self.window, color, (x, OFFSET_Y), (x, OFFSET_Y + BOARD_SIZE), thickness)
            
            # Horizontal lines
            y = OFFSET_Y + i * CELL_SIZE
            pygame.draw.line(self.window, color, (OFFSET_X, y), (OFFSET_X + BOARD_SIZE, y), thickness)
    
    def draw_numbers(self):
        for row in range(9):
            for col in range(9):
                num = self.board[row][col]
                if num != 0:
                    x = OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                    y = OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                    
                    # Determine color based on cell type
                    if self.original_board[row][col] != 0:
                        color = ORIGINAL_NUM_COLOR
                    elif num < 0:
                        color = WRONG_COLOR
                    elif self.show_mistakes and not self.is_valid(abs(num), (row, col)):
                        color = WRONG_COLOR
                    else:
                        color = INPUT_NUM_COLOR
                    
                    text = self.font_large.render(str(abs(num)), True, color)
                    text_rect = text.get_rect(center=(x, y))
                    self.window.blit(text, text_rect)
    
    def draw_highlight(self):
        if self.selected_cell:
            row, col = self.selected_cell
            
            # Highlight selected cell
            selected_rect = pygame.Rect(
                OFFSET_X + col * CELL_SIZE + 2,
                OFFSET_Y + row * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4
            )
            s = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4), pygame.SRCALPHA)
            s.fill(SELECTED_COLOR)
            self.window.blit(s, selected_rect)
            
            # Highlight same numbers
            num = abs(self.board[row][col])
            if num != 0:
                for i in range(9):
                    for j in range(9):
                        if abs(self.board[i][j]) == num and (i, j) != (row, col):
                            same_rect = pygame.Rect(
                                OFFSET_X + j * CELL_SIZE + 2,
                                OFFSET_Y + i * CELL_SIZE + 2,
                                CELL_SIZE - 4,
                                CELL_SIZE - 4
                            )
                            s = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4), pygame.SRCALPHA)
                            s.fill(SAME_NUM_COLOR)
                            self.window.blit(s, same_rect)
            
            # Highlight row and column
            for i in range(9):
                if i != col:
                    col_rect = pygame.Rect(
                        OFFSET_X + i * CELL_SIZE + 2,
                        OFFSET_Y + row * CELL_SIZE + 2,
                        CELL_SIZE - 4,
                        CELL_SIZE - 4
                    )
                    s = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4), pygame.SRCALPHA)
                    s.fill(HIGHLIGHT_COLOR)
                    self.window.blit(s, col_rect)
                
                if i != row:
                    row_rect = pygame.Rect(
                        OFFSET_X + col * CELL_SIZE + 2,
                        OFFSET_Y + i * CELL_SIZE + 2,
                        CELL_SIZE - 4,
                        CELL_SIZE - 4
                    )
                    s = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4), pygame.SRCALPHA)
                    s.fill(HIGHLIGHT_COLOR)
                    self.window.blit(s, row_rect)
            
            # Highlight 3x3 box
            box_row, box_col = row // 3, col // 3
            for i in range(box_row * 3, box_row * 3 + 3):
                for j in range(box_col * 3, box_col * 3 + 3):
                    if (i, j) != (row, col):
                        box_rect = pygame.Rect(
                            OFFSET_X + j * CELL_SIZE + 2,
                            OFFSET_Y + i * CELL_SIZE + 2,
                            CELL_SIZE - 4,
                            CELL_SIZE - 4
                        )
                        s = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4), pygame.SRCALPHA)
                        s.fill(HIGHLIGHT_COLOR)
                        self.window.blit(s, box_rect)
    
    def draw_side_panel(self):
        # Title
        title = self.font_large.render("SUDOKU", True, ACCENT_COLOR)
        title_rect = title.get_rect(center=(WIDTH - 115, 35))
        self.window.blit(title, title_rect)
        
        # Timer
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time
        
        mins, secs = divmod(int(self.elapsed_time), 60)
        time_text = f"{mins:02d}:{secs:02d}"
        timer = self.font_medium.render(f"Time: {time_text}", True, TEXT_COLOR)
        timer_rect = timer.get_rect(center=(WIDTH - 115, 560))
        self.window.blit(timer, timer_rect)
        
        # Difficulty
        diff_text = {EASY: "Easy", MEDIUM: "Medium", HARD: "Hard"}.get(self.difficulty, "Medium")
        diff = self.font_small.render(f"Level: {diff_text}", True, (150, 150, 170))
        self.window.blit(diff, (WIDTH - 190, 590))
        
        # Draw buttons
        self.draw_button('new', "New Game")
        self.draw_button('reset', "Reset")
        self.draw_button('check', "Check")
        self.draw_button('menu', "Menu")
    
    def draw_number_panel(self):
        panel_y = 615
        for num in range(1, 10):
            count = self.number_counts[num]
            color = TEXT_COLOR if count > 0 else (80, 80, 100)
            
            text = self.font_small.render(f"{num}: {count}", True, color)
            self.window.blit(text, (OFFSET_X + (num - 1) * 55, panel_y))
    
    def draw_board(self):
        self.window.fill(BG_COLOR)
        self.draw_grid()
        self.draw_highlight()
        self.draw_numbers()
        self.draw_side_panel()
        self.draw_number_panel()
        pygame.display.flip()
    
    def get_cell_from_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        x, y = pos
        if OFFSET_X <= x < OFFSET_X + BOARD_SIZE and OFFSET_Y <= y < OFFSET_Y + BOARD_SIZE:
            col = (x - OFFSET_X) // CELL_SIZE
            row = (y - OFFSET_Y) // CELL_SIZE
            return (int(row), int(col))
        return None
    
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                pos = pygame.mouse.get_pos()
                
                # Check board click
                cell = self.get_cell_from_pos(pos)
                if cell and not self.puzzle_solved:
                    self.selected_cell = cell
                    self.draw_board()
                else:
                    self.selected_cell = None
                    
                    # Check button clicks
                    for key in ['new', 'reset', 'check', 'menu']:
                        if self.buttons[key].collidepoint(pos):
                            if key == 'new':
                                self.restart()
                            elif key == 'reset':
                                self.reset()
                            elif key == 'check':
                                self.check_solution()
                            elif key == 'menu':
                                return True  # Signal to go back to menu
                    self.draw_board()
        
        elif event.type == pygame.KEYDOWN and self.selected_cell and not self.puzzle_solved:
            row, col = self.selected_cell
            
            if self.original_board[row][col] == 0:
                if event.unicode.isdigit() and '1' <= event.unicode <= '9':
                    num = int(event.unicode)
                    self.board[row][col] = num
                    self.update_number_counts()
                    self.draw_board()
                    
                    # Auto-check for mistakes if enabled
                    if self.show_mistakes and not self.is_valid(num, (row, col)):
                        pass  # Number will be shown in red
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.board[row][col] = 0
                    self.update_number_counts()
                    self.draw_board()
    
    def update_button_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        for key in self.buttons:
            self.button_hovered[key] = self.buttons[key].collidepoint(mouse_pos)
    
    def reset(self):
        self.board = self.original_board.copy()
        self.selected_cell = None
        self.elapsed_time = 0
        self.start_time = time.time()
        self.update_number_counts()
        self.draw_board()
    
    def check_solution(self):
        self.show_mistakes = True
        mistakes = 0
        empty = 0
        
        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                if num == 0:
                    empty += 1
                elif not self.is_valid(abs(num), (i, j)):
                    mistakes += 1
        
        self.draw_board()
        
        if mistakes == 0 and empty == 0:
            self.puzzle_solved = True
            self.timer_running = False
            self.celebrate()
    
    def celebrate(self):
        # Create particles
        for _ in range(100):
            self.particles.append({
                'x': random.randint(OFFSET_X, OFFSET_X + BOARD_SIZE),
                'y': random.randint(OFFSET_Y, OFFSET_Y + BOARD_SIZE),
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-5, 5),
                'color': random.choice([CORRECT_COLOR, ACCENT_COLOR, BUTTON_HOVER, (255, 215, 0)]),
                'size': random.randint(3, 8),
                'life': 100
            })
        
        # Animate particles
        start_time = time.time()
        while time.time() - start_time < 3:
            self.window.fill(BG_COLOR)
            self.draw_grid()
            self.draw_numbers()
            self.draw_side_panel()
            
            # Update and draw particles
            for p in self.particles[:]:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] += 0.2  # Gravity
                p['life'] -= 1
                
                if p['life'] <= 0:
                    self.particles.remove(p)
                else:
                    pygame.draw.circle(self.window, p['color'], (int(p['x']), int(p['y'])), p['size'])
            
            # Draw victory message
            victory = self.font_large.render("SOLVED!", True, CORRECT_COLOR)
            victory_rect = victory.get_rect(center=(WIDTH - 115, 300))
            self.window.blit(victory, victory_rect)
            
            pygame.display.flip()
            pygame.time.wait(20)
        
        self.draw_board()
    
    def restart(self):
        difficulty = self.difficulty
        board = generate_random_board(difficulty)
        self.__init__(board)
        return self.play()
    
    def play(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.update_button_hover()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                
                result = self.handle_input(event)
                if result == True:  # Menu button clicked
                    return True  # Return True to indicate menu should be shown
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        return False


def generate_random_board(difficulty: int = MEDIUM) -> np.ndarray:
    # Create empty board
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill diagonal 3x3 boxes (independent)
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for row in range(3):
            for col in range(3):
                board[i + row][i + col] = nums.pop()
    
    # Solve to fill the board
    temp_sudoku = Sudoku(board)
    temp_sudoku.solve()
    filled_board = temp_sudoku.board.copy()
    
    # Remove numbers based on difficulty
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    
    removed = 0
    for cell in cells:
        if removed >= difficulty:
            break
        row, col = cell
        backup = filled_board[row][col]
        filled_board[row][col] = 0
        
        # Check if still solvable
        test_board = filled_board.copy()
        temp_sudoku2 = Sudoku(test_board)
        temp_sudoku2.solve()
        
        if temp_sudoku2.solve():
            removed += 1
        else:
            filled_board[row][col] = backup
    
    return filled_board


def select_difficulty() -> int:
    pygame.init()
    window = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Select Difficulty")
    
    font_large = pygame.font.SysFont('Segoe UI', 36, bold=True)
    font_medium = pygame.font.SysFont('Segoe UI', 24, bold=True)
    
    buttons = {
        'easy': pygame.Rect(100, 100, 200, 50),
        'medium': pygame.Rect(100, 180, 200, 50),
        'hard': pygame.Rect(100, 260, 200, 50)
    }
    
    running = True
    while running:
        window.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()
        
        # Title
        title = font_large.render("SUDOKU", True, ACCENT_COLOR)
        title_rect = title.get_rect(center=(200, 50))
        window.blit(title, title_rect)
        
        # Draw buttons
        for key, rect in buttons.items():
            color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_NORMAL
            pygame.draw.rect(window, color, rect, border_radius=10)
            
            text = key.capitalize()
            text_surface = font_medium.render(text, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            window.blit(text_surface, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons['easy'].collidepoint(event.pos):
                        return EASY
                    elif buttons['medium'].collidepoint(event.pos):
                        return MEDIUM
                    elif buttons['hard'].collidepoint(event.pos):
                        return HARD
        
        pygame.time.wait(16)
    
    return MEDIUM


if __name__ == "__main__":
    while True:
        difficulty = select_difficulty()
        if difficulty is None:
            break
        board = generate_random_board(difficulty)
        game = Sudoku(board)
        to_menu = game.play()
        if to_menu:
            continue  # Go back to difficulty selection
        else:
            break  # Game quit normally
