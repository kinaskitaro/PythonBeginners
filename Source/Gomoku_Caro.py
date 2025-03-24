import pygame
import time
import json
import os
from random import randint, choice
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

pygame.init()

SIZE = 15 
CELL_SIZE = 40
WIDTH = SIZE * CELL_SIZE
HEIGHT = SIZE * CELL_SIZE + 60  # Add extra space for the score display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro Game")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)

# Additional constants
DIFFICULTY_LEVELS = {
    'Easy': 2,
    'Medium': 3,
    'Hard': 4
}
FONT_SIZE = 40
TRAINING_MAX = 100
GAME_MESSAGES = {
    'win': '{} Wins!',
    'draw': 'Draw!',
    'turn': "{}'s Turn"
}

# Neural Network for Q-Learning
class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Replay Memory
class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

# Q-Learning Agent
class QLearningAgent:
    def __init__(self, state_size, action_size, lr=0.001, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.1):
        """Initialize the Q-Learning agent."""
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.model = DQN(state_size, action_size)
        self.target_model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.memory = ReplayMemory(10000)
        self.update_target_model()

    def update_target_model(self):
        """Update the target model to match the current model."""
        self.target_model.load_state_dict(self.model.state_dict())

    def act(self, state, training=False):
        """Choose an action based on the current state."""
        state = torch.FloatTensor(state).unsqueeze(0)
        if np.random.rand() <= self.epsilon:
            action = random.randint(0, self.action_size - 1)
        else:
            with torch.no_grad():
                q_values = self.model(state)
            action = torch.argmax(q_values).item()
        return action

    def train(self, batch_size):
        """Train the model using a batch of experiences."""
        if len(self.memory) < batch_size:
            return
        batch = self.memory.sample(batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)

        q_values = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        next_q_values = self.target_model(next_states).max(1)[0]
        target_q_values = rewards + (1 - dones) * self.gamma * next_q_values

        loss = self.criterion(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Lớp trò chơi
class CaroGame:
    def __init__(self, size=15):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.last_move = None
        self.score = {'X': 0, 'O': 0}
        self.game_state = ''
    
    def make_move(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == ' ':
            self.board[x][y] = self.current_player
            self.last_move = (x, y)
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def is_winner(self, player):
        for i in range(self.size):
            for j in range(self.size):
                if j <= self.size - 5 and all(self.board[i][j + k] == player for k in range(5)):
                    return True
                if i <= self.size - 5 and all(self.board[i + k][j] == player for k in range(5)):
                    return True
                if i <= self.size - 5 and j <= self.size - 5 and all(self.board[i + k][j + k] == player for k in range(5)):
                    return True
                if i >= 4 and j <= self.size - 5 and all(self.board[i - k][j + k] == player for k in range(5)):
                    return True
        return False

    def is_full(self):
        return all(self.board[i][j] != ' ' for i in range(self.size) for j in range(self.size))

    def game_over(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_full()

    def get_score(self):
        return f"Player X: {self.score['X']}  Player O: {self.score['O']}"

# Hàm vẽ bàn cờ
def draw_board(game):
    """Draw the game board, score, and bottom line."""
    screen.fill(WHITE)
    
    # Draw the grid
    for i in range(SIZE):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SIZE * CELL_SIZE))
    
    # Draw the X and O marks
    for i in range(SIZE):
        for j in range(SIZE):
            if game.board[i][j] == 'X':
                pygame.draw.line(screen, RED, (j * CELL_SIZE + 5, i * CELL_SIZE + 5), 
                                 ((j + 1) * CELL_SIZE - 5, (i + 1) * CELL_SIZE - 5), 3)
                pygame.draw.line(screen, RED, ((j + 1) * CELL_SIZE - 5, i * CELL_SIZE + 5), 
                                 (j * CELL_SIZE + 5, (i + 1) * CELL_SIZE - 5), 3)
            elif game.board[i][j] == 'O':
                pygame.draw.circle(screen, BLUE, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5, 3)
    
    # Draw the bottom line to separate the table from the score
    pygame.draw.line(screen, BLACK, (0, SIZE * CELL_SIZE), (WIDTH, SIZE * CELL_SIZE), 2)
    
    # Draw the score with a more attractive style
    font = pygame.font.SysFont(None, FONT_SIZE)
    score_text = font.render(game.get_score(), True, BLACK)
    score_background_rect = pygame.Rect(0, SIZE * CELL_SIZE, WIDTH, 60)  # Background for the score
    pygame.draw.rect(screen, GRAY, score_background_rect)  # Draw the background
    score_rect = score_text.get_rect(center=(WIDTH // 2, SIZE * CELL_SIZE + 30))  # Center the score
    screen.blit(score_text, score_rect)

# Hàm đánh giá
def evaluate_line(line, player):
    """Evaluate a line for the given player."""
    count = line.count(player)
    empty = line.count(' ')
    if count == 5:
        return 10000
    elif count == 4 and empty == 1:
        return 1000
    elif count == 3 and empty == 2:
        return 100
    elif count == 2 and empty == 3:
        return 10
    return 0

def evaluate_board(board, size, last_move):
    """Evaluate the board state."""
    if not last_move:
        return 0
    x, y = last_move
    
    # Cache the board section we're evaluating
    min_i, max_i = max(0, x - 4), min(size, x + 5)
    min_j, max_j = max(0, y - 4), min(size, y + 5)
    section = [row[min_j:max_j] for row in board[min_i:max_i]]
    
    score = 0
    for player, factor in [('X', 1), ('O', -1)]:
        # Horizontal
        for row in section:
            score += evaluate_line(row, player) * factor
        
        # Vertical
        for j in range(len(section[0])):
            column = [row[j] for row in section]
            score += evaluate_line(column, player) * factor
        
        # Diagonals
        for i in range(len(section) - 4):
            for j in range(len(section[0]) - 4):
                diagonal = [section[i + k][j + k] for k in range(5)]
                score += evaluate_line(diagonal, player) * factor
                diagonal = [section[i + k][j + 4 - k] for k in range(5)]
                score += evaluate_line(diagonal, player) * factor
    
    return score

# Tối ưu tìm kiếm
def get_nearby_moves(game, radius=2):
    if not game.last_move:
        return [(randint(0, SIZE-1), randint(0, SIZE-1))]
    x, y = game.last_move
    moves = []
    for i in range(max(0, x - radius), min(SIZE, x + radius + 1)):
        for j in range(max(0, y - radius), min(SIZE, y + radius + 1)):
            if game.board[i][j] == ' ':
                moves.append((i, j))
    return moves if moves else [(x, y)]

# Minimax với Alpha-Beta
def minimax(game, depth, alpha, beta, maximizing_player):
    if depth == 0 or game.game_over():
        return evaluate_board(game.board, game.size, game.last_move)

    moves = get_nearby_moves(game)
    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            game.make_move(*move)
            eval = minimax(game, depth - 1, alpha, beta, False)
            game.board[move[0]][move[1]] = ' '
            game.current_player = 'X'
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            game.make_move(*move)
            eval = minimax(game, depth - 1, alpha, beta, True)
            game.board[move[0]][move[1]] = ' '
            game.current_player = 'O'
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(game, depth=3):
    best_move = None
    best_value = float('inf')
    alpha = float('-inf')
    beta = float('inf')
    moves = get_nearby_moves(game)
    
    for move in moves:
        game.make_move(*move)
        value = minimax(game, depth - 1, alpha, beta, True)
        game.board[move[0]][move[1]] = ' '
        game.current_player = 'O'
        if value < best_value:
            best_value = value
            best_move = move
        beta = min(beta, value)
    return best_move

# Helper function to convert board to numerical state
def board_to_numeric(board):
    """Convert the board state to a numerical representation."""
    return [[1 if cell == 'X' else -1 if cell == 'O' else 0 for cell in row] for row in board]

# Training mode
def training_mode():
    """Train the bot using Deep Q-Learning."""
    agent = QLearningAgent(state_size=SIZE * SIZE, action_size=SIZE * SIZE)
    num_games = 100  # Number of training games
    batch_size = 64

    for i in range(num_games):
        game = CaroGame(SIZE)
        state = np.array(board_to_numeric(game.board)).flatten()  # Convert board to numeric
        while not game.game_over():
            action = agent.act(state, training=True)  # No logging during training
            x, y = divmod(action, SIZE)
            if game.make_move(x, y):
                reward = 1 if game.is_winner('O') else -1 if game.is_winner('X') else 0
                next_state = np.array(board_to_numeric(game.board)).flatten()  # Convert next board to numeric
                done = game.game_over()
                agent.memory.push(state, action, reward, next_state, done)
                state = next_state
                agent.train(batch_size)
        
        agent.update_target_model()
        print(f"Training game {i+1}/{num_games} completed")
    
    # Return to the main menu after training
    return True

# Play with bot mode
def play_with_bot_mode():
    """Play against the bot and log game outcomes."""
    game = CaroGame(SIZE)
    difficulty = 'Medium'  # Default difficulty
    running = True
    scores = {'X': 0, 'O': 0}  # Initialize scores outside the game instance

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = 'Easy'
                elif event.key == pygame.K_2:
                    difficulty = 'Medium'
                elif event.key == pygame.K_3:
                    difficulty = 'Hard'
            elif event.type == pygame.MOUSEBUTTONDOWN and game.current_player == 'X':
                x, y = event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE
                if game.make_move(x, y):
                    game.game_state = GAME_MESSAGES['turn'].format('Player O')
        
        if game.current_player == 'O' and not game.game_over():
            move = find_best_move(game, depth=DIFFICULTY_LEVELS[difficulty])
            if move:
                game.make_move(*move)
                game.game_state = GAME_MESSAGES['turn'].format('Player X')
        
        draw_board(game)
        pygame.display.flip()
        
        if game.game_over():
            if game.is_winner('X'):
                scores['X'] += 1  # Increment Player's score
                game.game_state = GAME_MESSAGES['win'].format('Player X')
            elif game.is_winner('O'):
                scores['O'] += 1  # Increment Bot's score
                game.game_state = GAME_MESSAGES['win'].format('Player O')
            else:
                game.game_state = GAME_MESSAGES['draw']
            
            pygame.time.wait(2000)
            game = CaroGame(SIZE)  # Reset the game board
            game.score = scores  # Preserve scores across games
    
    return True

# Play with another player mode
def play_with_another_player_mode():
    """Play against another player."""
    game = CaroGame(SIZE)
    running = True
    scores = {'X': 0, 'O': 0}  # Initialize scores outside the game instance

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE
                if game.make_move(x, y):
                    if game.is_winner('X'):
                        scores['X'] += 1  # Increment Player X's score
                        game.game_state = GAME_MESSAGES['win'].format('Player X')
                    elif game.is_winner('O'):
                        scores['O'] += 1  # Increment Player O's score
                        game.game_state = GAME_MESSAGES['win'].format('Player O')
                    elif game.is_full():
                        game.game_state = GAME_MESSAGES['draw']
        
        draw_board(game)
        pygame.display.flip()
        
        if game.game_over():
            pygame.time.wait(2000)
            game = CaroGame(SIZE)  # Reset the game board
            game.score = scores  # Preserve scores across games
    
    return True

def draw_button(text, x, y, width, height, color, hover_color, font, is_hovered):
    """Draw a button with hover effect."""
    button_color = hover_color if is_hovered else color
    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=10)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def main_menu():
    """Display the main menu with button-like options."""
    font = pygame.font.SysFont(None, 50)
    button_font = pygame.font.SysFont(None, 40)
    options = [
        ("Training", training_mode),
        ("Play with Bot", play_with_bot_mode),
        ("Play with Another Player", play_with_another_player_mode)
    ]
    button_height = 60
    button_spacing = 20
    button_color = GRAY
    hover_color = RED

    # Calculate button dimensions dynamically based on text width
    button_widths = [button_font.size(text)[0] + 40 for text, _ in options]  # Add padding to text width
    max_button_width = max(button_widths)
    button_x = (WIDTH - max_button_width) // 2
    button_y_start = (HEIGHT - (len(options) * (button_height + button_spacing) - button_spacing)) // 2

    while True:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for i, (text, action) in enumerate(options):
            button_y = button_y_start + i * (button_height + button_spacing)
            is_hovered = button_x <= mouse_pos[0] <= button_x + max_button_width and button_y <= mouse_pos[1] <= button_y + button_height
            draw_button(text, button_x, button_y, max_button_width, button_height, button_color, hover_color, button_font, is_hovered)

            if is_hovered and mouse_click[0]:  # Left mouse button clicked
                pygame.time.wait(200)  # Add a small delay for better UX
                if action():
                    return True
                return False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

# Chạy game
if __name__ == "__main__":
    try:
        if main_menu():
            pygame.quit()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()