import pygame
import os
import random
import sys
import json
import math

# Initialize the game
pygame.init()

# Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
FPS = 60
HIGHSCORE_FILE = "dinosaur_highscore.json"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 149, 237)
YELLOW = (255, 215, 0)
PURPLE = (147, 112, 219)

# Screen setup
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🦖 Dinosaur Runner 🦖")

# Load assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")

def load_image(path):
    return pygame.image.load(os.path.join(ASSETS_DIR, path))

RUNNING = [load_image(os.path.join("Dino", "DinoRun1.png")), load_image(os.path.join("Dino", "DinoRun2.png"))]
JUMPING = load_image(os.path.join("Dino", "DinoJump.png"))
DUCKING = [load_image(os.path.join("Dino", "DinoDuck1.png")), load_image(os.path.join("Dino", "DinoDuck2.png"))]
SMALL_CACTUS = [load_image(os.path.join("Cactus", "SmallCactus1.png")), load_image(os.path.join("Cactus", "SmallCactus2.png")), load_image(os.path.join("Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [load_image(os.path.join("Cactus", "LargeCactus1.png")), load_image(os.path.join("Cactus", "LargeCactus2.png")), load_image(os.path.join("Cactus", "LargeCactus3.png"))]
BIRD = [load_image(os.path.join("Bird", "Bird1.png")), load_image(os.path.join("Bird", "Bird2.png"))]
CLOUD = load_image(os.path.join("Other", "Cloud.png"))
BG = load_image(os.path.join("Other", "Track.png"))


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 6)
        self.life = 30
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-5, -1)
        self.gravity = 0.2

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity
        self.life -= 1
        self.size = max(0, self.size - 0.1)

    def draw(self, screen):
        if self.life > 0:
            alpha = int((self.life / 30) * 255)
            surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, alpha), (int(self.size), int(self.size)), int(self.size))
            screen.blit(surface, (self.x - self.size, self.y - self.size))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 10

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
        self.dino_rect.y = int(self.Y_POS)

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
        elif not user_input[pygame.K_DOWN] and self.dino_duck:
            self.dino_duck = False
            self.dino_run = True
        elif not self.dino_jump and not self.dino_duck:
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False
    
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = int(self.Y_POS_DUCK)
        self.step_index += 1
    
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = int(self.Y_POS)
        self.step_index += 1
    
    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= int(self.jump_vel * 4)
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL
    
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
        self.opacity = random.randint(150, 200)
        self.speed_factor = random.uniform(0.5, 0.8)

    def update(self, game_speed):
        self.x -= game_speed * self.speed_factor
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
            self.opacity = random.randint(150, 200)

    def draw(self, screen):
        cloud_surface = self.image.copy()
        cloud_surface.set_alpha(self.opacity)
        screen.blit(cloud_surface, (self.x, self.y))


class Obstacle:
    def __init__(self, image, obstacle_type):
        self.image = image
        self.type = obstacle_type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed):
        self.rect.x -= game_speed

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = int(325)
        self.rect.width = self.rect.width // 2
        self.rect.height = self.rect.height // 2
    

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = int(300)
        self.rect.width = self.rect.width // 2
        self.rect.height = self.rect.height // 2
    

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = int(250)
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index//5], self.rect)
        self.index += 1


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.player = Dinosaur()
        self.cloud = Cloud()
        self.clouds = [self.cloud]
        self.game_speed = 8
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.high_score = self.load_highscore()
        self.obstacles = []
        self.death_count = 0
        self.paused = False
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.running = True
        self.particles = []
        self.screen_shake = 0
        self.day_night_cycle = 0
        self.score_animation = 0
        self.combo = 0
        self.last_obstacle_pass_time = 0

    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('highscore', 0)
            except:
                return 0
        return 0

    def save_highscore(self):
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump({'highscore': self.high_score}, f)

    def update_score(self):
        if self.points % 100 == 0 and self.points != 0:
            self.game_speed += 0.5
        if self.points > self.high_score:
            self.high_score = self.points
            self.save_highscore()

    def create_particles(self, x, y, color, count=10):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def draw_score(self):
        score_offset = min(self.score_animation, 10)
        text_color = ORANGE if self.score_animation > 0 else BLACK
        text = self.font.render(f"Points: {self.points}  High Score: {self.high_score}", True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (500, 40 - score_offset)
        SCREEN.blit(text, text_rect)
        
        if self.combo > 1:
            combo_text = self.font.render(f"Combo x{self.combo}!", True, PURPLE)
            combo_rect = combo_text.get_rect()
            combo_rect.center = (500, 70)
            SCREEN.blit(combo_text, combo_rect)
        
        if self.score_animation > 0:
            self.score_animation -= 1

    def draw_background(self):
        self.day_night_cycle = (self.points % 500) / 500
        
        if self.day_night_cycle < 0.5:
            day_progress = self.day_night_cycle * 2
            r = int(255 - day_progress * 100)
            g = int(255 - day_progress * 100)
            b = int(255)
            bg_color = (r, g, b)
        else:
            night_progress = (self.day_night_cycle - 0.5) * 2
            r = int(155 + night_progress * 100)
            g = int(155 + night_progress * 100)
            b = int(155 + night_progress * 100)
            bg_color = (r, g, b)
        
        SCREEN.fill(bg_color)
        
        image_width = BG.get_width()
        SCREEN.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        SCREEN.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def handle_collisions(self):
        for obstacle in self.obstacles:
            player_hitbox = self.player.dino_rect.inflate(-20, -20)
            obstacle_hitbox = obstacle.rect.inflate(-15, -15)
            if player_hitbox.colliderect(obstacle_hitbox):
                self.screen_shake = 10
                self.create_particles(self.player.dino_rect.centerx, self.player.dino_rect.centery, RED, 20)
                pygame.time.delay(2000)
                self.death_count += 1
                self.menu()
                self.points = 0
                self.game_speed = 8
                self.obstacles.clear()
                self.combo = 0
                return
            elif obstacle.rect.right < self.player.dino_rect.left:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_obstacle_pass_time < 3000:
                    self.combo += 1
                else:
                    self.combo = 1
                self.last_obstacle_pass_time = current_time
                
                score_gain = 1 * self.combo
                self.points += score_gain
                self.score_animation = 10
                self.create_particles(obstacle.rect.right, obstacle.rect.centery, GREEN, 5)
                self.obstacles.remove(obstacle)

    def spawn_obstacles(self):
        if len(self.obstacles) == 0:
            if random.randint(0, 100) < 2:
                rand = random.randint(0, 2)
                if rand == 0:
                    self.obstacles.append(SmallCactus(SMALL_CACTUS))
                elif rand == 1:
                    self.obstacles.append(LargeCactus(LARGE_CACTUS))
                elif rand == 2:
                    self.obstacles.append(Bird(BIRD))

    def update_game(self):
        user_input = pygame.key.get_pressed()
        self.draw_background()
        self.player.draw(SCREEN)
        self.player.update(user_input)
        self.spawn_obstacles()

        for obstacle in self.obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(self.game_speed)

        self.handle_collisions()
        
        if random.randint(0, 200) < 1 and len(self.clouds) < 5:
            self.clouds.append(Cloud())
        
        for cloud in self.clouds:
            cloud.update(self.game_speed)
            cloud.draw(SCREEN)
        
        for particle in self.particles[:]:
            particle.update()
            particle.draw(SCREEN)
            if particle.life <= 0:
                self.particles.remove(particle)
        
        if self.screen_shake > 0:
            shake_offset_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_offset_y = random.randint(-self.screen_shake, self.screen_shake)
            SCREEN.blit(SCREEN, (shake_offset_x, shake_offset_y))
            self.screen_shake -= 1
        
        self.update_score()
        self.draw_score()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused

            if not self.paused:
                self.update_game()
            else:
                self.draw_pause_screen()

            self.clock.tick(FPS)
            pygame.display.update()

    def draw_pause_screen(self):
        self.draw_background()
        self.player.draw(SCREEN)
        for obstacle in self.obstacles:
            obstacle.draw(SCREEN)
        for cloud in self.clouds:
            cloud.draw(SCREEN)
        self.draw_score()
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        SCREEN.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont("Arial", 60, bold=True)
        text = font.render("PAUSED", True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        SCREEN.blit(text, text_rect)
        
        resume_text = self.font.render("Press P to Resume", True, WHITE)
        resume_rect = resume_text.get_rect()
        resume_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        SCREEN.blit(resume_text, resume_rect)

    def draw_gradient_background(self):
        for y in range(SCREEN_HEIGHT):
            color_factor = y / SCREEN_HEIGHT
            r = int(135 + color_factor * 120)
            g = int(206 + color_factor * 49)
            b = int(235)
            pygame.draw.line(SCREEN, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def menu(self):
        menu_running = True
        dino_anim = 0
        while menu_running:
            self.draw_gradient_background()
            
            title = self.title_font.render("🦖 DINOSAUR RUNNER 🦖", True, DARK_GRAY)
            title_rect = title.get_rect()
            title_rect.center = (SCREEN_WIDTH // 2, 100)
            
            title_shadow = self.title_font.render("🦖 DINOSAUR RUNNER 🦖", True, GRAY)
            title_shadow_rect = title_shadow.get_rect()
            title_shadow_rect.center = (SCREEN_WIDTH // 2 + 3, 103)
            
            SCREEN.blit(title_shadow, title_shadow_rect)
            SCREEN.blit(title, title_rect)

            if self.death_count == 0:
                text = self.font.render("Press any Key to Start", True, ORANGE)
                text_rect = text.get_rect()
                text_rect.center = (SCREEN_WIDTH // 2, 200)
                SCREEN.blit(text, text_rect)
                
                dino_image = RUNNING[dino_anim // 5 % 2]
                dino_rect = dino_image.get_rect()
                dino_rect.center = (SCREEN_WIDTH // 2, 350)
                SCREEN.blit(dino_image, dino_rect)
                
                controls_text1 = self.font.render("Controls:", True, DARK_GRAY)
                controls_text2 = self.font.render("↑ JUMP | ↓ DUCK | P PAUSE", True, DARK_GRAY)
                controls_rect1 = controls_text1.get_rect()
                controls_rect2 = controls_text2.get_rect()
                controls_rect1.center = (SCREEN_WIDTH // 2, 450)
                controls_rect2.center = (SCREEN_WIDTH // 2, 490)
                SCREEN.blit(controls_text1, controls_rect1)
                SCREEN.blit(controls_text2, controls_rect2)
            else:
                game_over_text = self.title_font.render("GAME OVER", True, RED)
                game_over_rect = game_over_text.get_rect()
                game_over_rect.center = (SCREEN_WIDTH // 2, 150)
                SCREEN.blit(game_over_text, game_over_rect)
                
                text = self.font.render("Press any Key to Restart", True, ORANGE)
                score_text = self.font.render(f"Your Score: {self.points}", True, BLUE)
                highscore_text = self.font.render(f"High Score: {self.high_score}", True, PURPLE)
                
                text_rect = text.get_rect()
                text_rect.center = (SCREEN_WIDTH // 2, 200)
                score_rect = score_text.get_rect()
                score_rect.center = (SCREEN_WIDTH // 2, 280)
                highscore_rect = highscore_text.get_rect()
                highscore_rect.center = (SCREEN_WIDTH // 2, 330)
                
                SCREEN.blit(score_text, score_rect)
                SCREEN.blit(highscore_text, highscore_rect)
                SCREEN.blit(text, text_rect)
                
                dino_image = load_image(os.path.join("Dino", "DinoDead.png"))
                dino_rect = dino_image.get_rect()
                dino_rect.center = (SCREEN_WIDTH // 2, 420)
                SCREEN.blit(dino_image, dino_rect)

            dino_anim += 1
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    menu_running = False


if __name__ == "__main__":
    game = Game()
    game.menu()
    game.run()
