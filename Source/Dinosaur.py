import pygame
import os
import random
import sys  # Import sys to handle program termination

# Initialize the game
pygame.init()

#Global Variables
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Game")
FPS = 60

RUNNING = [pygame.image.load(os.path.join("./Source/Assets/Dino", "DinoRun1.png")), pygame.image.load(os.path.join("./Source/Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("./Source/Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("./Source/Assets/Dino", "DinoDuck1.png")), pygame.image.load(os.path.join("./Source/Assets/Dino", "DinoDuck2.png"))]
SMALL_CACTUS = [pygame.image.load(os.path.join("./Source/Assets/Cactus", "SmallCactus1.png")), pygame.image.load(os.path.join("./Source/Assets/Cactus", "SmallCactus2.png")), pygame.image.load(os.path.join("./Source/Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("./Source/Assets/Cactus", "LargeCactus1.png")), pygame.image.load(os.path.join("./Source/Assets/Cactus", "LargeCactus2.png")), pygame.image.load(os.path.join("./Source/Assets/Cactus", "LargeCactus3.png"))]
BIRD = [pygame.image.load(os.path.join("./Source/Assets/Bird", "Bird1.png")), pygame.image.load(os.path.join("./Source/Assets/Bird", "Bird2.png"))]
CLOUD = pygame.image.load(os.path.join("./Source/Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("./Source/Assets/Other", "Track.png"))

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_jump = False
        self.dino_run = True

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.tilt = 0
        self.gravity = 0

        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, user_input):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()

        if self.step_index >= 10:
            self.step_index = 0

        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_jump = True
            self.dino_duck = False
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        elif not self.dino_jump and not self.dino_duck:
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False
    
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1
    
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1
    
    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:

    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        self.rect.width = self.rect.width // 2  # Reduce the width of the small cactus
        self.rect.height = self.rect.height // 2  # Reduce the height of the small cactus
    
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
        self.rect.width = self.rect.width // 2  # Reduce the width of the large cactus
        self.rect.height = self.rect.height // 2  # Reduce the height of the large cactus
    
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, high_score
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 12  # Reduced the initial game speed
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    high_score = 0  # Track the high score
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0
    paused = False

    def score():
        global points, game_speed, high_score
        if points % 50 == 0 and points != 0:
            game_speed += 1  # Increase game speed every 50 points
        if points > high_score:
            high_score = points  # Update high score
        text = font.render(f"Points: {points}  High Score: {high_score}", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (500, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        # Set the background color first
        if points % 100 < 50:
            SCREEN.fill((255, 255, 255))  # Daytime (white)
        else:
            SCREEN.fill((169, 169, 169))  # Nighttime (gray)

        # Draw the ground
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()  # Ensure the program exits cleanly
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        if not run:  # Check if the game should exit
            break

        if not paused:
            user_input = pygame.key.get_pressed()

            # Draw background first
            background()

            player.draw(SCREEN)
            player.update(user_input)

            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))

            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(2000)
                    death_count += 1
                    menu(death_count)
                    points = 0
                    game_speed = 10  # Reset game speed
                    obstacles.clear()
                elif obstacle.rect.right < player.dino_rect.left:
                    points += 1  # Increase points by 1 when the player has completely passed an obstacle
                    obstacles.remove(obstacle)

            cloud.draw(SCREEN)
            cloud.update()
            score()

        else:
            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render("Paused", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)

        clock.tick(FPS)
        pygame.display.update()

def menu(death_count):
    global points, high_score
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render(f"Your Score: {points}  High Score: {high_score}", True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (500, 100)
            SCREEN.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (500, 200)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (500, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()  # Ensure the program exits cleanly
            if event.type == pygame.KEYDOWN:
                main()
                return  # Ensure the loop exits after restarting the game

    pygame.quit()
    sys.exit()  # Ensure the program exits cleanly

menu(death_count=0)