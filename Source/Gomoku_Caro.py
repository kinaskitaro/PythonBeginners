import pygame
import os
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
HEIGHT = SIZE * CELL_SIZE + 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)

FONT_SIZE = 40
GAME_MESSAGES = {
    'win': '{} Wins!',
    'draw': 'Draw!',
    'turn': "{}'s Turn"
}

class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class QLearningAgent:
    def __init__(self, state_size, action_size, lr=0.0005, gamma=0.99, epsilon=1.0, epsilon_decay=0.99999, epsilon_min=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.model = DQN(state_size, action_size).to('cuda' if torch.cuda.is_available() else 'cpu')
        self.target_model = DQN(state_size, action_size).to('cuda' if torch.cuda.is_available() else 'cpu')
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.memory = ReplayMemory(100000)
        self.update_target_model()
        self.decay_schedule = {  # Example decay schedule
            1000: 0.5,
            5000: 0.1,
            10000: 0.01
        }

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def act(self, state, training=False):
        state = torch.FloatTensor(state).unsqueeze(0).to('cuda' if torch.cuda.is_available() else 'cpu')
        if np.random.rand() <= self.epsilon and training:
            possible_moves = self.get_possible_moves(state)  # Get valid moves
            if possible_moves:
                return random.choice(possible_moves)  # Explore only valid moves
            else:
                return random.randint(0, self.action_size - 1)  # Fallback if no valid moves
        with torch.no_grad():
            q_values = self.model(state)
        return torch.argmax(q_values).item()

    def get_possible_moves(self, state):
        #state = torch.FloatTensor(state).unsqueeze(0).to('cuda' if torch.cuda.is_available() else 'cpu') #No need to unsqueeze or move to device here
        board = np.reshape(state.cpu().numpy(), (SIZE, SIZE))  # Reshape to board
        possible_moves = []
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == ' ':  # Assuming ' ' is empty cell
                    possible_moves.append(i * SIZE + j)
        return possible_moves

    def train(self, batch_size, episode): # Add episode number
        if len(self.memory) < batch_size:
            return

        batch = self.memory.sample(batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        # Convert lists of numpy arrays to numpy arrays before creating tensors
        states = np.array(states)
        next_states = np.array(next_states)

        states = torch.FloatTensor(states).to('cuda' if torch.cuda.is_available() else 'cpu')
        actions = torch.LongTensor(actions).to('cuda' if torch.cuda.is_available() else 'cpu')
        rewards = torch.FloatTensor(rewards).to('cuda' if torch.cuda.is_available() else 'cpu')
        next_states = torch.FloatTensor(next_states).to('cuda' if torch.cuda.is_available() else 'cpu')
        dones = torch.FloatTensor(dones).to('cuda' if torch.cuda.is_available() else 'cpu')

        q_values = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        next_q_values = self.target_model(next_states).max(1)[0]
        target_q_values = rewards + (1 - dones) * self.gamma * next_q_values

        loss = self.criterion(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        self.optimizer.step()

        # Apply scheduled epsilon decay
        for milestone, epsilon_value in self.decay_schedule.items():
            if episode >= milestone and self.epsilon > epsilon_value:
                self.epsilon = epsilon_value
                print(f"Epsilon set to {self.epsilon} at episode {episode}")

        # Adaptive Epsilon Decay (Example, uncomment to use)
        #if loss.item() < 0.01 and self.epsilon > self.epsilon_min:
        #    self.epsilon = max(self.epsilon * 0.999, self.epsilon_min)
        #elif self.epsilon < 1.0:
        #     self.epsilon = min(self.epsilon / 0.999, 1.0)
    def get_epsilon(self):
        return self.epsilon


class CaroGame:
    def __init__(self, size=15):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.last_move = None
        self.score = {'X': 0, 'O': 0}
        self.game_state = GAME_MESSAGES['turn'].format('X')

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

def draw_board(game):
    screen.fill(WHITE)
    for i in range(SIZE):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SIZE * CELL_SIZE))
    for i in range(SIZE):
        for j in range(SIZE):
            if game.board[i][j] == 'X':
                pygame.draw.line(screen, RED, (j * CELL_SIZE + 5, i * CELL_SIZE + 5),
                                 ((j + 1) * CELL_SIZE - 5, (i + 1) * CELL_SIZE - 5), 3)
                pygame.draw.line(screen, RED, ((j + 1) * CELL_SIZE - 5, i * CELL_SIZE + 5),
                                 (j * CELL_SIZE + 5, (i + 1) * CELL_SIZE - 5), 3)
            elif game.board[i][j] == 'O':
                pygame.draw.circle(screen, BLUE, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5, 3)
    pygame.draw.line(screen, BLACK, (0, SIZE * CELL_SIZE), (WIDTH, SIZE * CELL_SIZE), 2)
    font = pygame.font.SysFont(None, FONT_SIZE)
    score_text = font.render(game.get_score(), True, BLACK)
    score_background_rect = pygame.Rect(0, SIZE * CELL_SIZE, WIDTH, 60)
    pygame.draw.rect(screen, GRAY, score_background_rect)
    score_rect = score_text.get_rect(center=(WIDTH // 2, SIZE * CELL_SIZE + 30))
    screen.blit(score_text, score_rect)

    #game_state_text = font.render(game.game_state, True, BLACK)
    #game_state_rect = game_state_text.get_rect(center = (WIDTH//2, 30))
    #screen.blit(game_state_text, game_state_rect)

def board_to_numeric(board):
    return [[1 if cell == 'X' else -1 if cell == 'O' else 0 for cell in row] for row in board]

def training_mode():
    try:
        agent = QLearningAgent(state_size=SIZE * SIZE, action_size=SIZE * SIZE,
                               lr=0.0005, gamma=0.99, epsilon=1.0, epsilon_decay=0.99999, epsilon_min=0.01)
        num_games = 10000 #Reduce number of games to test
        batch_size = 128
        model_path = "Trained_bot.pth"

        for i in range(num_games):
            game = CaroGame(SIZE)
            state = np.array(board_to_numeric(game.board)).flatten()
            total_reward = 0

            while not game.game_over():
                action = agent.act(state, training=True)
                x, y = divmod(action, SIZE)
                if game.make_move(x, y):
                    if game.is_winner('O'):
                        reward = 10
                    elif game.is_winner('X'):
                        reward = -10
                    else:
                        reward = -0.1
                        if game.is_winner('X'):
                            reward += 5

                    next_state = np.array(board_to_numeric(game.board)).flatten()
                    done = game.game_over()
                    agent.memory.push(state, action, reward, next_state, done)
                    state = next_state
                    agent.train(batch_size, i) # Pass the episode number here
                    total_reward += reward

            agent.update_target_model()
            print(f"Training game {i+1}/{num_games} completed, Total Reward: {total_reward}, Epsilon: {agent.get_epsilon()}")

        torch.save(agent.model.state_dict(), model_path)
        print(f"Model saved to {model_path}")
        return True
    except Exception as e:
        print(f"Error during training: {e}")
        import traceback
        traceback.print_exc()
        return False

def play_with_bot_mode():
    agent = QLearningAgent(state_size=SIZE * SIZE, action_size=SIZE * SIZE)
    model_path = "Trained_bot.pth"
    if os.path.exists(model_path):
        try:
            # Load the model state dictionary using the 'rb' (read binary) mode
            agent.model.load_state_dict(torch.load(model_path, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu')))
            agent.update_target_model()
            print(f"Model loaded from {model_path}")
        except Exception as e:
             print(f"Error loading model: {e}")
             import traceback
             traceback.print_exc() #Print full traceback
             return False # Exit if model loading fails
    else:
        print("Trained model not found. Please select 'Training' from the main menu to train the bot first.")
        return False

    game = CaroGame(SIZE)
    running = True
    scores = {'X': 0, 'O': 0}
    max_attempts = 100

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and game.current_player == 'X':
                x, y = event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE
                if game.make_move(x, y):
                    #game.game_state = GAME_MESSAGES['turn'].format('Player O')
                    break

        if game.current_player == 'O' and not game.game_over():
            state = np.array(board_to_numeric(game.board)).flatten()
            attempts = 0
            while attempts < max_attempts:
                action = agent.act(state)
                x, y = divmod(action, SIZE)

                if 0 <= x < SIZE and 0 <= y < SIZE and game.board[x][y] == ' ':
                    if game.make_move(x, y):
                        break
                attempts += 1
            else:
                print("AI could not find a valid move after several attempts. Game may be unwinnable.")
                possible_moves = [(i, j) for i in range(SIZE) for j in range(SIZE) if game.board[i][j] == ' ']
                if possible_moves:
                    x, y = random.choice(possible_moves)
                    game.make_move(x, y)
                else:
                    print("No possible moves left. It's a draw!")
                    game.game_state = GAME_MESSAGES['draw']
                    pygame.time.wait(2000)
                    game = CaroGame(SIZE)
                    game.score = scores
                    continue
        draw_board(game)
        pygame.display.flip()

        if game.game_over():
            if game.is_winner('X'):
                scores['X'] += 1
                game.game_state = GAME_MESSAGES['win'].format('Player X')
            elif game.is_winner('O'):
                scores['O'] += 1
                game.game_state = GAME_MESSAGES['win'].format('Player O')
            else:
                game.game_state = GAME_MESSAGES['draw']

            pygame.time.wait(2000)
            game = CaroGame(SIZE)
            game.score = scores


    return True

def play_with_another_player_mode():
    game = CaroGame(SIZE)
    running = True
    scores = {'X': 0, 'O': 0}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE
                if game.make_move(x, y):
                    if game.is_winner('X'):
                        scores['X'] += 1
                        game.game_state = GAME_MESSAGES['win'].format('Player X')
                    elif game.is_winner('O'):
                        scores['O'] += 1
                        game.game_state = GAME_MESSAGES['win'].format('Player O')
                    elif game.is_full():
                        game.game_state = GAME_MESSAGES['draw']


        draw_board(game)
        pygame.display.flip()
        if game.game_over():
            pygame.time.wait(2000)
            game = CaroGame(SIZE)
            game.score = scores
    return True

def main_menu():
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
    max_button_width = max(button_font.size(text)[0] + 40 for text, _ in options)
    button_x = (WIDTH - max_button_width) // 2
    button_y_start = (HEIGHT - (len(options) * (button_height + button_spacing) - button_spacing)) // 2

    while True:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        for i, (text, action) in enumerate(options):
            button_y = button_y_start + i * (button_height + button_spacing)
            is_hovered = button_x <= mouse_pos[0] <= button_x + max_button_width and button_y <= mouse_pos[1] <= button_y + button_height
            pygame.draw.rect(screen, hover_color if is_hovered else button_color, (button_x, button_y, max_button_width, button_height), border_radius=10)
            text_surface = button_font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(button_x + max_button_width // 2, button_y + button_height // 2))
            screen.blit(text_surface, text_rect)
            if is_hovered and mouse_click[0]:
                pygame.time.wait(200)
                if action():
                    return True
                return False
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

if __name__ == "__main__":
    try:
        if main_menu():
            pygame.quit()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()