import numpy as np
import pygame
import time  # Add import for time
import sys

# Suppress Pygame welcome message
class NullWriter:
    def write(self, _):
        pass

null_writer = NullWriter()
original_stdout = sys.stdout
sys.stdout = null_writer

# UI Constants
WIDTH = 550
HEIGHT = 600
BACKGROUND_COLOR = (245, 251, 250)
HIGHLIGHT_COLOR = (188, 214, 236)  # Light blue highlight
BUFFER = 5

# Difficulty Levels
EASY = 30    # Remove 30 numbers
MEDIUM = 45  # Remove 45 numbers
HARD = 60    # Remove 60 numbers

class Sudoku:
    def __init__(self, board):
        self.board = np.array(board)
        self.original_board = self.board.copy()  # Keep a copy of the original board
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku Game")
        self.font = pygame.font.SysFont('Comic Sans MS', 35)
        self.submit_button_color = (0, 0, 0)  # Default color for submit button
        self.submit_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 80, 150, 40)  # Define submit button
        self.setup_ui()
        self.start_time = time.time()  # Record start time

    def is_valid(self, num, pos):
        # Check row
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False

    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)  # row, col

        return None

    def setup_ui(self):
        self.window.fill(BACKGROUND_COLOR)
        # Draw grid lines
        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(self.window, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 4)
                pygame.draw.line(self.window, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4)
            else:
                pygame.draw.line(self.window, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 2)
                pygame.draw.line(self.window, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2)
        self.update_board_display()
        self.submit_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 80, 150, 40)  # Define submit button
        pygame.draw.rect(self.window, self.submit_button_color, self.submit_button)  # Draw submit button background
        pygame.draw.rect(self.window, (0, 0, 0), self.submit_button, 2)  # Draw submit button border
        submit_text = self.font.render("Submit", True, (255, 255, 255))
        text_rect = submit_text.get_rect(center=self.submit_button.center)
        self.window.blit(submit_text, text_rect)
        pygame.display.update()

    def update_board_display(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    # Use blue for static numbers, black for inputted numbers, and red for wrong numbers
                    if self.board[i][j] < 0:
                        value_color = (255, 0, 0)  # Red for wrong numbers
                        value = self.font.render(str(-self.board[i][j]), True, value_color)
                    else:
                        value_color = (52, 31, 151) if self.original_board[i][j] != 0 else (0, 0, 0)
                        value = self.font.render(str(self.board[i][j]), True, value_color)
                    self.window.blit(value, ((j+1)*50 + 15, (i+1)*50))
        pygame.display.update()

    def highlight_same_number(self, selected):
        if selected:
            num = abs(self.board[selected[0]][selected[1]])
            if num != 0:
                for i in range(9):
                    for j in range(9):
                        if abs(self.board[i][j]) == num:
                            pygame.draw.rect(self.window, HIGHLIGHT_COLOR,  # Light blue background
                                ((j+1)*50 + BUFFER, (i+1)*50 + BUFFER,
                                50 - 2*BUFFER, 50 - 2*BUFFER))
                            # Redraw number if cell is not empty
                            if self.board[i][j] != 0:
                                if self.board[i][j] < 0:
                                    value_color = (255, 0, 0)  # Red for wrong numbers
                                    value = self.font.render(str(-self.board[i][j]), True, value_color)
                                else:
                                    value_color = (52, 31, 151) if self.original_board[i][j] != 0 else (0, 0, 0)
                                    value = self.font.render(str(self.board[i][j]), True, value_color)
                                self.window.blit(value, ((j+1)*50 + 15, (i+1)*50))
                pygame.display.update()

    def highlight_cell(self, selected):
        # Clear previous highlights by redrawing background
        self.setup_ui()
        self.update_board_display()
        if selected:
            row, col = selected
            pygame.draw.rect(self.window, (255, 255, 0),  # Yellow border
                ((col+1)*50 + BUFFER, (row+1)*50 + BUFFER,
                50 - 2*BUFFER, 50 - 2*BUFFER), 3)
            # Redraw number if cell is not empty
            if self.board[row][col] != 0:
                if self.board[row][col] < 0:
                    value_color = (255, 0, 0)  # Red for wrong numbers
                    value = self.font.render(str(-self.board[row][col]), True, value_color)
                else:
                    value_color = (52, 31, 151) if self.original_board[row][col] != 0 else (0, 0, 0)
                    value = self.font.render(str(self.board[row][col]), True, value_color)
                self.window.blit(value, ((col+1)*50 + 15, (row+1)*50))
        self.highlight_same_number(selected)
        pygame.display.update()

    def handle_submit(self):
        incorrect_cells = []
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))
                elif self.board[i][j] < 0 or not self.is_valid(abs(self.board[i][j]), (i, j)):
                    incorrect_cells.append((i, j))

        if empty_cells or incorrect_cells:
            for cell in empty_cells:
                pygame.draw.rect(self.window, (255, 0, 0),  # Red border for empty cells
                                 ((cell[1] + 1) * 50 + BUFFER, (cell[0] + 1) * 50 + BUFFER,
                                  50 - 2 * BUFFER, 50 - 2 * BUFFER), 3)
            for cell in incorrect_cells:
                value = self.font.render(str(abs(self.board[cell[0]][cell[1]])), True, (255, 0, 0))  # Red number for incorrect cells
                self.window.blit(value, ((cell[1] + 1) * 50 + 15, (cell[0] + 1) * 50))
            pygame.display.update()
        else:
            self.display_play_time()

    def play(self):
        selected = None
        puzzle_solved = False
        while True:
            mouse_pos = pygame.mouse.get_pos()
            if self.submit_button.collidepoint(mouse_pos):
                new_color = (100, 100, 255)  # Change color on hover
            else:
                new_color = (0, 0, 0)  # Default color

            if new_color != self.submit_button_color:
                self.submit_button_color = new_color
                pygame.draw.rect(self.window, self.submit_button_color, self.submit_button)  # Draw submit button background
                pygame.draw.rect(self.window, (0, 0, 0), self.submit_button, 2)  # Draw submit button border
                submit_text = self.font.render("Submit", True, (255, 255, 255))
                text_rect = submit_text.get_rect(center=self.submit_button.center)
                self.window.blit(submit_text, text_rect)
                pygame.display.update(self.submit_button)  # Update only the submit button area

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and not puzzle_solved:
                    pos = pygame.mouse.get_pos()
                    if 50 <= pos[0] <= 500 and 50 <= pos[1] <= 500:
                        x = (pos[1] - 50) // 50
                        y = (pos[0] - 50) // 50
                        selected = (x, y)
                        self.highlight_cell(selected)
                    elif self.submit_button.collidepoint(pos):  # Check if submit button is clicked
                        self.handle_submit()
                        if not any(self.board[i][j] == 0 or self.board[i][j] < 0 for i in range(9) for j in range(9)):
                            puzzle_solved = True
                if event.type == pygame.KEYDOWN and selected and not puzzle_solved:
                    if self.original_board[selected[0]][selected[1]] == 0:  # Only allow input in non-static cells
                        if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                            num = int(event.unicode)
                            if self.is_valid(num, selected):
                                self.board[selected[0]][selected[1]] = num
                                self.highlight_cell(selected)
                                # Display inputted number in black
                                value = self.font.render(str(num), True, (0, 0, 0))
                                self.window.blit(value, ((selected[1]+1)*50 + 15, (selected[0]+1)*50))
                                pygame.display.update()
                            else:
                                self.board[selected[0]][selected[1]] = num
                                self.highlight_cell(selected)
                                # Display wrong number in red and keep it on screen
                                value = self.font.render(str(num), True, (255, 0, 0))
                                self.window.blit(value, ((selected[1]+1)*50 + 15, (selected[0]+1)*50))
                                pygame.display.update()
                                # Keep the wrong number in the board for display
                                self.board[selected[0]][selected[1]] = -num
                        elif event.key == pygame.K_BACKSPACE or event.unicode == '0':
                            # Clear the cell if backspace is pressed
                            self.board[selected[0]][selected[1]] = 0
                            self.highlight_cell(selected)
                            pygame.display.update()
            pygame.display.update()

    def display_play_time(self):
        play_time = time.time() - self.start_time
        hours, rem = divmod(play_time, 3600)
        minutes, seconds = divmod(rem, 60)
        time_str = f"Completed in: {int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        # Display completed time on the screen
        font = pygame.font.SysFont('Comic Sans MS', 35)
        text_surface = font.render(time_str, True, (52, 31, 151))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 25))  # Center the text with padding
        self.window.fill(BACKGROUND_COLOR, (0, 0, WIDTH, 50))  # Clear previous time display
        self.window.blit(text_surface, text_rect)
        pygame.display.update()

def generate_random_board(difficulty=MEDIUM):
    import random
    # Create empty board
    board = [[0 for _ in range(9)] for _ in range(9)]
    # Fill diagonal 3x3 boxes (which are independent)
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for row in range(3):
            for col in range(3):
                board[i + row][i + col] = nums.pop()
    
    # Create a Sudoku instance to use its solve method
    temp_sudoku = Sudoku(board)
    temp_sudoku.solve()  # Fill the rest of the board
    
    # Remove numbers based on difficulty
    filled_board = temp_sudoku.board.copy()
    cells = [(i, j) for i in range(9) for j in range(9)]
    for _ in range(difficulty):
        if not cells:
            break
        row, col = random.choice(cells)
        cells.remove((row, col))
        filled_board[row][col] = 0
    
    return filled_board.tolist()

def select_difficulty():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Select Difficulty")
    font = pygame.font.SysFont('Comic Sans MS', 35)
    
    buttons = {
        'EASY': (WIDTH//2 - 100, 150, 200, 50),
        'MEDIUM': (WIDTH//2 - 100, 250, 200, 50),
        'HARD': (WIDTH//2 - 100, 350, 200, 50)
    }
    
    while True:
        window.fill(BACKGROUND_COLOR)
        mouse_pos = pygame.mouse.get_pos()
        for text, rect in buttons.items():
            # Check if mouse is over the button
            if pygame.Rect(rect).collidepoint(mouse_pos):
                color = (100, 100, 255)  # Hover color
            else:
                color = HIGHLIGHT_COLOR  # Normal color
            
            pygame.draw.rect(window, color, rect)
            pygame.draw.rect(window, (0, 0, 0), rect, 2)  # Border
            text_surface = font.render(text, True, (52, 31, 151))
            text_rect = text_surface.get_rect(center=(rect[0] + rect[2]//2, rect[1] + rect[3]//2))
            window.blit(text_surface, text_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Return None to indicate the game should close
            if event.type == pygame.MOUSEBUTTONDOWN:
                for text, rect in buttons.items():
                    if pygame.Rect(rect).collidepoint(mouse_pos):
                        if text == 'EASY':
                            return EASY
                        elif text == 'MEDIUM':
                            return MEDIUM
                        elif text == 'HARD':
                            return HARD

# Restore original stdout
sys.stdout = original_stdout

if __name__ == "__main__":
    difficulty = select_difficulty()
    if difficulty is not None:
        board = generate_random_board(difficulty)
        sudoku = Sudoku(board)
        sudoku.play()
