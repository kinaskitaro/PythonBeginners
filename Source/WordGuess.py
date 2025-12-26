import tkinter as tk
from tkinter import messagebox
import random
import json
import os
from tkinter import font as tkfont

class WordGuessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Word Guess Game")
        self.master.geometry("950x700")
        self.master.resizable(False, False)
        self.master.configure(bg="#1a1a2e")
        
        self.HIGHSCORE_FILE = "wordguess_highscore.json"
        
        self.categories = {
            "Animals": {
                "COLOR": "#e74c3c",
                "WORDS": ["TIGER", "EAGLE", "SHARK", "PANDA", "KOALA", "OTTER", "SNAKE", "MOOSE", "GOOSE", "ZEBRA",
                          "HAWKS", "CAMEL", "PANDA", "LEOPARD", "CAMEL", "WHALE", "TURKEY", "GEESE", "SHEEP", "HORSE",
                          "MOUSE", "SHEEP", "SHARK", "SQUID", "SLOTH", "LEMUR", "HYENA", "JAGUAR", "CRAZY", "COBRA",
                          "PIGEO", "SHREW", "OCEAN", "RODENT", "BEAVER", "BOBCAT", "COUGAR", "FERRET", "GAZEL", "LLAMA",
                          "MAMBA", "OTTER", "QUAIL", "RAVEN", "SABER", "SKUNK", "TAPIR", "WALRU", "WOMBAT", "YAK", "ZORRO"]
            },
            "Technology": {
                "COLOR": "#3498db",
                "WORDS": ["LAPTOP", "PHONE", "ROBOT", "DRONE", "CHIP", "SERVER", "PIXEL", "BINARY", "CODEX", "PYTHON",
                          "CYBER", "HACKER", "VIRUS", "ROUTER", "MEMORY", "SYSTEM", "DATABASE", "NETWORK", "LASER", "RADAR",
                          "METER", "LOGIC", "CIRCUIT", "ROUTER", "SERVER", "BINARY", "PIXEL", "LASER", "RADAR", "LOGIC",
                          "MOUSE", "CABLE", "WIFI", "APPLE", "NEXUS", "SAMSU", "SONY", "DELL", "ACER", "ASUS",
                          "INTEL", "AMD", "NVIDIA", "QUANTUM", "VIRUS", "MALWARE", "FIREWALL", "CLOUD", "DATA", "INPUT"]
            },
            "Nature": {
                "COLOR": "#27ae60",
                "WORDS": ["RIVER", "OCEAN", "PLANT", "FLOWER", "STORM", "CLOUD", "FOREST", "DESERT", "VALLEY", "BEACH",
                          "REEFS", "MEADOW", "GARDEN", "GRASS", "LEAVES", "ROCKS", "SANDS", "WATER", "SOLAR", "LUNAR",
                          "BASIN", "BAYOU", "BERRY", "BLOOM", "BUSH", "CANE", "CANYON", "CEDAR", "CLIFF", "CREEK",
                          "DAISY", "DAWN", "DUST", "EARTH", "FEN", "FIELD", "FOG", "FROST", "GUST", "HAIL",
                          "HEAT", "HILL", "LAKE", "LOAM", "LUNAR", "MARSH", "MOSS", "MOUNT", "MUD", "NIGHT"]
            },
            "Sports": {
                "COLOR": "#f39c12",
                "WORDS": ["SOCCER", "TENNIS", "BOXING", "SKIING", "DIVING", "SWING", "JOGGING", "KAYAK", "LACROS", "RUGBY",
                          "CRICK", "DANCE", "ROWIN", "SURF", "WATER", "YOGA", "ZUMBA", "CYCLE", "DRIVE", "FIGHT",
                          "GAME", "GOLF", "GYMN", "HURL", "JUDO", "KICK", "LUGE", "MARTIAL", "NET", "ORIENTEER",
                          "PADDLE", "POLO", "POWER", "RALLY", "SAIL", "SHOOT", "SKATE", "SKII", "SNOW", "SOFT",
                          "SQUASH", "SUMO", "SWIM", "TAEKWONDO", "TRAMPOLINE", "TRIATHLON", "ULTIMATE", "VOLLEY", "WALK", "WATER"]
            },
            "Food": {
                "COLOR": "#9b59b6",
                "WORDS": ["PIZZA", "BURGER", "STEAK", "FRUIT", "SUSHI", "CURRY", "PASTA", "RICE", "FISH", "BACON",
                          "BREAD", "BUN", "CAKE", "CANDY", "CIDER", "CREAM", "DISH", "DUMPS", "EGG", "FRIES",
                          "GRAPE", "GRAIN", "HONEY", "JUICE", "KEBAB", "LEMON", "LUNCH", "MEAL", "MENU", "MELON",
                          "MILK", "MUFFIN", "NUT", "ONION", "PANCAKE", "PEAR", "PEPPER", "PIE", "PLUM", "PRUNE",
                          "PUDDING", "QUINCE", "RADISH", "RAISIN", "RICE", "ROLL", "SAUCE", "SODA", "SOUP", "SPICE"]
            },
            "Countries": {
                "COLOR": "#1abc9c",
                "WORDS": ["INDIA", "CHINA", "SPAIN", "FRANCE", "ITALY", "JAPAN", "KENYA", "EGYPT", "PERU", "CHILE",
                          "SWEDEN", "GREECE", "CUBA", "FIJI", "YEMEN", "OMAN", "NEPAL", "QATAR", "MEXICO", "BRAZIL",
                          "CANADA", "RUSSIA", "GERMANY", "TURKEY", "POLAND", "IRAN", "VIETNAM", "SUDAN", "LIBYA", "MALTA",
                          "NORWAY", "SUDAN", "SYRIA", "TOGO", "UGANDA", "WALES", "YUGOSLAVIA", "ZIMBABWE", "ALGERIA", "ANGOLA",
                          "ARGENTINA", "BAHRAIN", "BANGLA", "BELGIUM", "BHUTAN", "BOLIVIA", "BOSTWANA", "BRUNEI", "CAMBODIA", "CAMEROON"]
            },
            "Colors": {
                "COLOR": "#e91e63",
                "WORDS": ["WHITE", "BLACK", "BROWN", "GREEN", "CREAM", "GRAY", "PINK", "BLUE", "TEAL", "GOLD",
                          "PURPLE", "ORANGE", "YELLOW", "RED", "VIOLET", "BEIGE", "CYAN", "LIME", "NAVY", "MAGENTA",
                          "OLIVE", "MAROON", "CRIMSON", "SILVER", "BRONZE", "INDIGO", "CORAL", "AQUA", "AZURE", "IVORY",
                          "JADE", "KHAKI", "LAVENDER", "MAUVE", "MUSTARD", "OCHER", "PEACH", "PLUM", "RUBY", "SAFFRON",
                          "SAPPHIRE", "SCARLET", "TAN", "TURQUOISE", "UMBER", "VANILLA", "VERMILION", "WHEAT", "ALABASTER", "APRICOT"]
            },
            "Music": {
                "COLOR": "#673ab7",
                "WORDS": ["PIANO", "GUITAR", "VIOLIN", "FLUTE", "HARP", "BAND", "SONG", "SING", "BEAT", "OPERA",
                          "MELODY", "CHORUS", "JAZZ", "SOUL", "BLUES", "CONCERT", "ORCHESTRA", "CELLO", "BASS", "DRUMS",
                          "FIDDLE", "FLUTE", "GOSPEL", "HARP", "LYRICS", "MAESTRO", "MUSIC", "NOTES", "OBOE", "OPERA",
                          "PIANIST", "POP", "PSALM", "QUARTET", "QUINTET", "RADIO", "RAP", "RHYTHM", "ROCK", "SONGWRITER",
                          "SOUND", "SOUL", "SYMPHONY", "TEMPO", "TIMBRE", "TONE", "TRUMPET", "TUNE", "VERSE", "VIOLA"]
            }
        }
        
        self.current_category = "Animals"
        self.target_word = ""
        self.guesses = []
        self.current_guess = ""
        self.max_attempts = 6
        self.score = 0
        self.streak = 0
        self.high_score = self.load_highscore()
        self.game_over = False
        
        for category in self.categories:
            self.categories[category]["WORDS"] = [word for word in self.categories[category]["WORDS"] if len(word) == 5]
        
        self.create_widgets()
        self.start_new_round()

    def load_highscore(self):
        if os.path.exists(self.HIGHSCORE_FILE):
            try:
                with open(self.HIGHSCORE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('highscore', 0)
            except (json.JSONDecodeError, IOError):
                pass
        return 0

    def save_highscore(self):
        try:
            with open(self.HIGHSCORE_FILE, 'w') as f:
                json.dump({'highscore': self.high_score}, f)
        except IOError:
            pass

    def create_widgets(self):
        title_font = tkfont.Font(family="Segoe UI", size=32, weight="bold")
        label_font = tkfont.Font(family="Segoe UI", size=11)
        letter_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        
        header_frame = tk.Frame(self.master, bg="#1a1a2e")
        header_frame.pack(pady=10)
        
        title_label = tk.Label(header_frame, text="WORD GUESS", font=title_font, 
                              bg="#1a1a2e", fg="#00d4ff")
        title_label.pack()
        
        score_frame = tk.Frame(self.master, bg="#16213e", padx=20, pady=8)
        score_frame.pack(pady=5)
        
        self.score_label = tk.Label(score_frame, text=f"Score: {self.score}", 
                                    font=tkfont.Font(family="Segoe UI", size=14, weight="bold"),
                                    bg="#16213e", fg="#00ff88")
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.streak_label = tk.Label(score_frame, text=f"Streak: {self.streak}", 
                                     font=tkfont.Font(family="Segoe UI", size=14, weight="bold"),
                                     bg="#16213e", fg="#ffd700")
        self.streak_label.pack(side=tk.LEFT, padx=10)
        
        self.high_score_label = tk.Label(score_frame, text=f"Best: {self.high_score}", 
                                         font=tkfont.Font(family="Segoe UI", size=14, weight="bold"),
                                         bg="#16213e", fg="#ff6b6b")
        self.high_score_label.pack(side=tk.LEFT, padx=10)
        
        category_frame = tk.Frame(self.master, bg="#1a1a2e")
        category_frame.pack(pady=10)
        
        tk.Label(category_frame, text="Category:", font=label_font, 
                bg="#1a1a2e", fg="#888").pack(side=tk.LEFT)
        
        self.category_var = tk.StringVar(value=self.current_category)
        self.category_menu = tk.OptionMenu(category_frame, self.category_var, *self.categories.keys(),
                                          command=self.change_category)
        self.category_menu.config(font=tkfont.Font(family="Segoe UI", size=11, weight="bold"),
                                  bg="#16213e", fg="white", activebackground="#0f3460",
                                  activeforeground="white", relief="flat", padx=10)
        self.category_menu["menu"].config(bg="#16213e", fg="white", activebackground="#0f3460")
        self.category_menu.pack(side=tk.LEFT, padx=8)
        
        self.category_label = tk.Label(category_frame, text=self.current_category,
                                      font=tkfont.Font(family="Segoe UI", size=11, weight="bold"),
                                      bg="#1a1a2e", fg=self.categories[self.current_category]["COLOR"])
        self.category_label.pack(side=tk.LEFT, padx=5)
        
        main_container = tk.Frame(self.master, bg="#1a1a2e")
        main_container.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        left_panel = tk.Frame(main_container, bg="#1a1a2e")
        left_panel.pack(side=tk.LEFT, padx=10)
        
        hint_frame = tk.Frame(left_panel, bg="#1a1a2e")
        hint_frame.pack(pady=5)
        
        self.hint_label = tk.Label(hint_frame, text=f"Hints: {self.max_attempts}", 
                                   font=label_font, bg="#1a1a2e", fg="#ffd700")
        self.hint_label.pack()
        
        game_board_frame = tk.Frame(left_panel, bg="#1a1a2e")
        game_board_frame.pack(pady=10)
        
        self.cells = []
        for i in range(self.max_attempts):
            row = []
            row_frame = tk.Frame(game_board_frame, bg="#1a1a2e")
            row_frame.pack(pady=3)
            
            for j in range(5):
                cell = tk.Label(row_frame, text="", width=5, height=2, 
                               font=letter_font, bg="#16213e", fg="white",
                               relief="solid", borderwidth=1)
                cell.pack(side=tk.LEFT, padx=3)
                row.append(cell)
            self.cells.append(row)
        
        message_frame = tk.Frame(left_panel, bg="#1a1a2e")
        message_frame.pack(pady=10)
        
        self.message_label = tk.Label(message_frame, text="Guess the word!", font=label_font,
                                      bg="#1a1a2e", fg="#888")
        self.message_label.pack()
        
        right_panel = tk.Frame(main_container, bg="#1a1a2e")
        right_panel.pack(side=tk.RIGHT, padx=10)
        
        keyboard_frame = tk.Frame(right_panel, bg="#1a1a2e")
        keyboard_frame.pack(pady=10)
        
        self.keyboard = {}
        rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        for row_idx, row in enumerate(rows):
            row_frame = tk.Frame(keyboard_frame, bg="#1a1a2e")
            row_frame.pack(pady=2)
            
            if row_idx == 1:
                tk.Label(row_frame, text="", width=2, bg="#1a1a2e").pack(side=tk.LEFT)
            elif row_idx == 2:
                tk.Label(row_frame, text="", width=5, bg="#1a1a2e").pack(side=tk.LEFT)
            
            for letter in row:
                key = tk.Button(row_frame, text=letter, width=4, height=2,
                               font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
                               bg="#2d2d44", fg="white", activebackground="#3d3d54",
                               relief="flat", cursor="hand2",
                               command=lambda l=letter: self.on_key_press(l))
                key.pack(side=tk.LEFT, padx=1)
                self.keyboard[letter] = key
        
        buttons_frame = tk.Frame(right_panel, bg="#1a1a2e")
        buttons_frame.pack(pady=10)
        
        restart_round_btn = tk.Button(buttons_frame, text="RESTART", font=tkfont.Font(family="Segoe UI", size=11, weight="bold"),
                                    bg="#ffd700", fg="#1a1a2e", activebackground="#e6c200",
                                    relief="flat", cursor="hand2", padx=20, pady=8, command=self.restart_round)
        restart_round_btn.pack(side=tk.LEFT, padx=10)
        
        new_word_btn = tk.Button(buttons_frame, text="NEW WORD", font=tkfont.Font(family="Segoe UI", size=11, weight="bold"),
                              bg="#00d4ff", fg="#1a1a2e", activebackground="#00a8cc",
                              relief="flat", cursor="hand2", padx=20, pady=8, command=self.start_new_round)
        new_word_btn.pack(side=tk.LEFT, padx=10)
        
        new_game_btn = tk.Button(buttons_frame, text="NEW GAME", font=tkfont.Font(family="Segoe UI", size=11, weight="bold"),
                               bg="#ff6b6b", fg="white", activebackground="#e85555",
                               relief="flat", cursor="hand2", padx=20, pady=8, command=self.restart_game)
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        self.master.bind("<Key>", self.on_keypress_event)

    def change_category(self, value):
        self.current_category = value
        self.category_label.config(text=value,
                                   fg=self.categories[value]["COLOR"])
        self.start_new_round()
        self.message_label.config(text=f"New word from {value}!", fg=self.categories[value]["COLOR"])

    def start_new_round(self):
        words = self.categories[self.current_category]["WORDS"]
        self.target_word = random.choice(words)
        self.guesses = []
        self.current_guess = ""
        self.game_over = False
        
        for row in self.cells:
            for cell in row:
                cell.config(text="", bg="#16213e", fg="white")
        
        for letter in self.keyboard:
            self.keyboard[letter].config(bg="#2d2d44")
        
        self.message_label.config(text="Guess the word!", fg="#888")
        self.hint_label.config(text=f"Hints: {self.max_attempts}")

    def restart_round(self):
        self.guesses = []
        self.current_guess = ""
        self.game_over = False
        
        for row in self.cells:
            for cell in row:
                cell.config(text="", bg="#16213e", fg="white")
        
        for letter in self.keyboard:
            self.keyboard[letter].config(bg="#2d2d44")
        
        self.message_label.config(text="Guess the word!", fg="#888")
        self.hint_label.config(text=f"Hints: {self.max_attempts}")

    def restart_game(self):
        self.score = 0
        self.streak = 0
        self.update_score_display()
        self.start_new_round()

    def on_keypress_event(self, event):
        key = event.keysym.upper()
        if len(key) == 1 and key.isalpha():
            self.on_key_press(key)
        elif key == "BACKSPACE":
            self.backspace()
        elif key == "RETURN":
            self.submit_guess()

    def on_key_press(self, letter):
        if self.game_over:
            return
        
        if len(self.current_guess) < 5:
            self.current_guess += letter
            self.update_display()

    def backspace(self):
        if self.game_over:
            return
        
        if self.current_guess:
            self.current_guess = self.current_guess[:-1]
            self.update_display()

    def submit_guess(self):
        if self.game_over:
            return
        
        if len(self.current_guess) != 5:
            self.message_label.config(text="Not enough letters!", fg="#ff6b6b")
            return
        
        row = len(self.guesses)
        result = self.check_guess(self.current_guess)
        self.guesses.append((self.current_guess, result))
        
        self.animate_guess(row, self.current_guess, result)
        
        self.update_keyboard_colors(self.current_guess, result)
        
        if self.current_guess == self.target_word:
            # Delay win handling until animation finishes
            self.master.after(1000, lambda: self.handle_win(row))
        elif len(self.guesses) >= self.max_attempts:
            # Delay loss handling until animation finishes
            self.master.after(1000, self.handle_loss)
        else:
            self.current_guess = ""
            self.message_label.config(text="Keep going!", fg="#888")
            self.hint_label.config(text=f"Hints: {self.max_attempts - len(self.guesses)}")

    def check_guess(self, guess):
        if len(guess) != 5 or len(self.target_word) != 5:
            return ['absent'] * 5
        
        result = [''] * 5
        target_list = list(self.target_word)
        guess_list = list(guess)
        
        for i in range(5):
            if i >= len(target_list) or i >= len(guess_list):
                result[i] = 'absent'
                continue
                
            if guess_list[i] == target_list[i]:
                result[i] = 'correct'
                target_list[i] = '#'
                guess_list[i] = '#'
        
        for i in range(5):
            if i >= len(guess_list):
                result[i] = 'absent'
                continue
                
            if guess_list[i] != '#':
                if guess_list[i] in target_list:
                    result[i] = 'present'
                    idx = target_list.index(guess_list[i])
                    target_list[idx] = '#'
                else:
                    result[i] = 'absent'
        
        return result

    def animate_guess(self, row, guess, result):
        for i in range(5):
            status = result[i]
            if status == 'correct':
                color = "#00ff88"
                fg = "#1a1a2e"
            elif status == 'present':
                color = "#ffd700"
                fg = "#1a1a2e"
            else:
                color = "#3d3d54"
                fg = "#888"
            self.master.after(i * 150, self.update_cell_anim, self.cells[row][i], guess[i], color, fg)
    
    def update_cell_anim(self, cell, letter, color, fg):
        cell.config(text=letter, bg=color, fg=fg)

    def update_keyboard_colors(self, guess, result):
        for i in range(5):
            letter = guess[i]
            status = result[i]
            key = self.keyboard[letter]
            
            current_bg = key.cget("bg")
            
            if status == 'correct':
                key.config(bg="#00ff88", fg="#1a1a2e")
            elif status == 'present':
                if current_bg != "#00ff88":
                    key.config(bg="#ffd700", fg="#1a1a2e")
            elif status == 'absent':
                if current_bg not in ["#00ff88", "#ffd700"]:
                    key.config(bg="#3d3d54", fg="#888")

    def update_display(self):
        for i in range(5):
            if i < len(self.current_guess):
                self.cells[len(self.guesses)][i].config(text=self.current_guess[i])
            else:
                self.cells[len(self.guesses)][i].config(text="")

    def handle_win(self, attempts):
        self.game_over = True
        self.streak += 1
        
        points = (7 - attempts) * 10
        streak_bonus = self.streak * 5
        total_points = points + streak_bonus
        
        self.score += total_points
        
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_highscore()
        
        self.update_score_display()
        
        if self.streak >= 3:
            bonus_text = f" (including +{streak_bonus} streak bonus!)"
        else:
            bonus_text = ""
        
        self.message_label.config(text=f"You win! +{total_points} pts{bonus_text}", fg="#00ff88")
        
        if self.streak >= 5:
            self.message_label.config(text=f"Amazing! {self.streak} streak! (+{total_points} pts)", fg="#00ff88")

    def handle_loss(self):
        self.game_over = True
        self.streak = 0
        self.update_score_display()
        
        self.message_label.config(text=f"Word was: {self.target_word}", fg="#ff6b6b")

    def update_score_display(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.streak_label.config(text=f"Streak: {self.streak}")
        self.high_score_label.config(text=f"Best: {self.high_score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGuessGame(root)
    root.mainloop()
