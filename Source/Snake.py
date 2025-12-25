import turtle
import time
import random
import json
import os

HIGHSCORE_FILE = "snake_highscore.json"

class SnakeGame:
    def __init__(self):
        self.cell_size = 20
        self.grid_width = 28
        self.grid_height = 28
        self.game_width = self.grid_width * self.cell_size
        self.game_height = self.grid_height * self.cell_size
        
        self.delay = 0.1
        self.score = 0
        self.level = 1
        self.high_score = self.load_highscore()
        self.game_started = False
        self.game_paused = False
        self.game_over = False
        self.effects = []
        
        self.setup_screen()
        self.draw_game_grid()
        self.setup_game_objects()
        self.setup_bindings()
        self.show_start_screen()
        
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

    def setup_screen(self):
        self.wn = turtle.Screen()
        self.wn.title('🐍 Snake Game - Ultimate Edition 🐍')
        self.wn.bgcolor('#0d1117')
        self.wn.setup(width=700, height=700)
        self.wn.tracer(0)

    def draw_game_grid(self):
        grid = turtle.Turtle()
        grid.speed(0)
        grid.hideturtle()
        grid.penup()
        
        half_width = self.game_width / 2
        half_height = self.game_height / 2
        
        grid.goto(-half_width, half_height)
        grid.color('#4ecdc4')
        grid.pensize(3)
        grid.pendown()
        for _ in range(2):
            grid.forward(self.game_width)
            grid.right(90)
            grid.forward(self.game_height)
            grid.right(90)

    def setup_game_objects(self):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape('square')
        self.head.color('#00ff88')
        self.head.shapesize(0.9, 0.9)
        self.head.penup()
        self.head.goto(self.cell_size/2, self.cell_size/2)
        self.head_direction = "stop"

        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("#ff6b6b")
        self.food.shapesize(0.9)
        self.food.penup()
        self.food.goto(self.cell_size * 10.5, self.cell_size * 10.5)

        self.segments = []
        self.segment_colors = ['#00ff88', '#00cc6a', '#00994d', '#006633', '#003319']

        self.sc = turtle.Turtle()
        self.sc.speed(0)
        self.sc.color("white")
        self.sc.penup()
        self.sc.hideturtle()
        self.sc.goto(0, 310)

        self.start_text = turtle.Turtle()
        self.start_text.speed(0)
        self.start_text.color("#ffeb3b")
        self.start_text.penup()
        self.start_text.hideturtle()

        self.game_over_text = turtle.Turtle()
        self.game_over_text.speed(0)
        self.game_over_text.color("#ff4444")
        self.game_over_text.penup()
        self.game_over_text.hideturtle()

        self.update_score_display()

    def setup_bindings(self):
        self.wn.listen()
        self.wn.onkeypress(self.go_up, "Up")
        self.wn.onkeypress(self.go_down, "Down")
        self.wn.onkeypress(self.go_left, "Left")
        self.wn.onkeypress(self.go_right, "Right")
        self.wn.onkeypress(self.start_game, "space")
        self.wn.onkeypress(self.toggle_pause, "p")
        self.wn.onkeypress(self.restart_game, "r")

    def start_game(self):
        if not self.game_started:
            self.game_started = True
            self.start_text.clear()
            self.start_text.hideturtle()
            self.move_food()

    def toggle_pause(self):
        if self.game_started and not self.game_over:
            self.game_paused = not self.game_paused

    def restart_game(self):
        if self.game_over:
            self.game_over = False
            self.game_started = True
            self.game_over_text.clear()
            self.game_over_text.hideturtle()
            self.reset_game()

    def go_up(self):
        if self.head_direction != "down":
            self.head_direction = "up"

    def go_down(self):
        if self.head_direction != "up":
            self.head_direction = "down"

    def go_left(self):
        if self.head_direction != "right":
            self.head_direction = "left"

    def go_right(self):
        if self.head_direction != "left":
            self.head_direction = "right"

    def move(self):
        if self.head_direction == "up":
            y = self.head.ycor()
            self.head.sety(y + self.cell_size)
        elif self.head_direction == "down":
            y = self.head.ycor()
            self.head.sety(y - self.cell_size)
        elif self.head_direction == "left":
            x = self.head.xcor()
            self.head.setx(x - self.cell_size)
        elif self.head_direction == "right":
            x = self.head.xcor()
            self.head.setx(x + self.cell_size)

    def check_border_collision(self):
        x = self.head.xcor()
        y = self.head.ycor()
        half_width = self.game_width / 2 - self.cell_size
        half_height = self.game_height / 2 - self.cell_size
        return x >= half_width or x <= -half_width or y >= half_height or y <= -half_height

    def check_food_collision(self):
        return self.head.distance(self.food) < 15

    def check_body_collision(self):
        for segment in self.segments:
            if segment.distance(self.head) < 15:
                return True
        return False

    def move_segments(self):
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)

        if len(self.segments) > 0:
            x = self.head.xcor()
            y = self.head.ycor()
            self.segments[0].goto(x, y)

    def add_segment(self):
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        color_index = len(self.segments) % len(self.segment_colors)
        new_segment.color(self.segment_colors[color_index])
        new_segment.shapesize(0.9, 0.9)
        new_segment.penup()
        self.segments.append(new_segment)

    def create_food_particle(self):
        particle = turtle.Turtle()
        particle.speed(0)
        particle.shape("circle")
        particle.color("#ffd700")
        particle.shapesize(0.3)
        particle.penup()
        particle.goto(self.food.xcor(), self.food.ycor())
        self.effects.append({'turtle': particle, 'life': 10, 'dy': random.uniform(1, 3), 'dx': random.uniform(-1, 1)})

    def move_food(self):
        half_width = self.game_width / 2
        half_height = self.game_height / 2
        max_x = int((half_width - self.cell_size) / self.cell_size)
        max_y = int((half_height - self.cell_size) / self.cell_size)
        
        x = random.randint(-max_x + 1, max_x - 1) * self.cell_size + self.cell_size / 2
        y = random.randint(-max_y + 1, max_y - 1) * self.cell_size + self.cell_size / 2
        self.food.goto(x, y)
        for i in range(3):
            self.create_food_particle()

    def update_effects(self):
        for effect in self.effects[:]:
            effect['life'] -= 1
            effect['turtle'].setx(effect['turtle'].xcor() + effect['dx'])
            effect['turtle'].sety(effect['turtle'].ycor() + effect['dy'])
            if effect['life'] <= 0:
                effect['turtle'].hideturtle()
                self.effects.remove(effect)



    def update_score_display(self):
        self.sc.clear()
        score_text = f"Score: {self.score}  |  High Score: {self.high_score}  |  Level: {self.level}"
        self.sc.write(score_text, align="center", font=("Consolas", 14, "bold"))
        
        if self.game_paused:
            self.sc.goto(0, 0)
            self.sc.write("PAUSED", align="center", font=("Arial", 48, "bold"))
            self.sc.goto(0, 310)

    def show_start_screen(self):
        self.start_text.goto(0, -20)
        self.start_text.write("🐍 SNAKE GAME 🐍", align="center", font=("Arial", 40, "bold"))
        self.start_text.goto(0, -80)
        self.start_text.write("Press SPACE to Start", align="center", font=("Arial", 20, "normal"))
        self.start_text.goto(0, -120)
        self.start_text.write("Use Arrow Keys to Move", align="center", font=("Arial", 16, "normal"))
        self.start_text.goto(0, -150)
        self.start_text.write("Press P to Pause", align="center", font=("Arial", 16, "normal"))

    def show_game_over(self):
        self.game_over_text.goto(0, 50)
        self.game_over_text.write("GAME OVER", align="center", font=("Arial", 50, "bold"))
        self.game_over_text.goto(0, -20)
        self.game_over_text.write(f"Final Score: {self.score}", align="center", font=("Arial", 28, "normal"))
        if self.score >= self.high_score:
            self.game_over_text.goto(0, -60)
            self.game_over_text.write("🏆 NEW HIGH SCORE! 🏆", align="center", font=("Arial", 24, "bold"))
        self.game_over_text.goto(0, -100)
        self.game_over_text.write("Press R to Restart", align="center", font=("Arial", 18, "normal"))

    def reset_game(self):
        for segment in self.segments:
            segment.goto(1000, 1000)
            segment.hideturtle()
        self.segments.clear()
        self.score = 0
        self.level = 1
        self.delay = 0.1
        self.head_direction = "stop"
        self.head.goto(self.cell_size/2, self.cell_size/2)
        self.move_food()
        self.update_score_display()

    def update_highscore(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_highscore()

    def update_level(self):
        new_level = self.score // 50 + 1
        if new_level > self.level:
            self.level = new_level
            self.delay = max(0.05, 0.1 - (self.level * 0.01))
            return True
        return False

    def run(self):
        try:
            while True:
                self.wn.update()
                
                self.update_effects()

                if self.game_over:
                    time.sleep(0.1)
                    continue

                if not self.game_started:
                    time.sleep(0.1)
                    continue

                if self.game_paused:
                    self.update_score_display()
                    time.sleep(0.1)
                    continue

                if self.check_border_collision():
                    self.head_direction = "stop"
                    time.sleep(1)
                    self.game_over = True
                    self.show_game_over()

                if self.check_food_collision():
                    self.move_food()
                    self.add_segment()
                    self.score += 10
                    self.update_highscore()
                    self.update_score_display()
                    self.update_level()

                self.move_segments()
                self.move()

                if self.check_body_collision():
                    self.head_direction = "stop"
                    time.sleep(1)
                    self.game_over = True
                    self.show_game_over()

                time.sleep(self.delay)
        except turtle.Terminator:
            pass


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
