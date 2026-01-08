import tkinter as tk
from tkinter import font as tkfont
import random
import time
import json
import os

CATEGORIES = {
    "Animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🦁", "🐮", "🐷"],
    "Fruits": ["🍎", "🍌", "🍇", "🍊", "🍓", "🍑", "🍒", "🍍", "🥝", "🍉", "🍋", "🥭"],
    "Sports": ["⚽", "🏀", "🏈", "⚾", "🎾", "🏐", "🏉", "🎱", "🏓", "🏸", "🥊", "⛳"],
    "Weather": ["☀️", "🌙", "⭐", "☁️", "🌧️", "⛈️", "❄️", "🌈", "🌊", "🌪️", "🌡️", "💨"],
    "Vehicles": ["🚗", "🚕", "🚙", "🚌", "🚎", "🏍️", "🚂", "✈️", "🚁", "🚢", "🚲", "🚜"],
    "Foods": ["🍕", "🍔", "🍟", "🌭", "🍿", "🧁", "🍩", "🍪", "🍰", "🍫", "🍦", "🧊"],
    "Nature": ["🌸", "🌺", "🌻", "🌹", "🍀", "🌲", "🌴", "🌵", "🍄", "🌾", "🪨", "💐"],
    "Emojis": ["😀", "😍", "🥰", "😎", "🤩", "😇", "🥳", "🤗", "😂", "🤣", "😜", "😋"]
}

COLORS = {
    "card_back": "#34495e",
    "card_front": "#ecf0f1",
    "matched": "#27ae60",
    "selected": "#FF9800",
    "background": "#2c3e50",
    "panel": "#34495e",
    "button": "#3498db",
    "button_hover": "#2980b9",
    "text": "#ecf0f1",
    "accent": "#e74c3c"
}

class MemoryGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Memory Game")
        self.root.geometry("1050x900")
        self.root.configure(bg=COLORS["background"])
        self.root.resizable(False, False)
        
        self.cards = []
        self.flipped_cards = []
        self.matched_pairs = 0
        self.total_pairs = 0
        self.moves = 0
        self.start_time = None
        self.game_active = False
        self.current_difficulty = "Easy"
        self.current_category = "Animals"
        self.grid_size = (4, 4)
        self.flip_animation_ids = []
        
        self.custom_font = tkfont.Font(family="Arial", size=12)
        self.header_font = tkfont.Font(family="Arial", size=20, weight="bold")
        self.card_font = tkfont.Font(family="Segoe UI Emoji", size=40)
        
        self.create_widgets()
        self.show_category_selection()
        
    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg=COLORS["background"])
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
    def show_category_selection(self):
        self.clear_frame()
        
        header_container = tk.Frame(self.main_frame, bg=COLORS["background"])
        header_container.pack(fill="x", pady=20)
        
        title = tk.Label(header_container, text="🧠 MEMORY GAME 🧠", 
                        font=tkfont.Font(family="Arial", size=28, weight="bold"), 
                        bg=COLORS["background"], fg="#f39c12")
        title.pack(pady=10)
        
        subtitle = tk.Label(header_container, text="✨ Choose Your Challenge Category ✨", 
                           font=tkfont.Font(family="Arial", size=14), 
                           bg=COLORS["background"], fg=COLORS["text"])
        subtitle.pack(pady=5)
        
        main_container = tk.Frame(self.main_frame, bg=COLORS["background"])
        main_container.pack(expand=True, fill="both", padx=40)
        
        categories_frame = tk.Frame(main_container, bg=COLORS["background"])
        categories_frame.pack(expand=True)
        
        category_colors = {
            "Animals": "#e74c3c",
            "Fruits": "#e91e63",
            "Sports": "#9c27b0",
            "Weather": "#673ab7",
            "Vehicles": "#3f51b5",
            "Foods": "#2196f3",
            "Nature": "#4caf50",
            "Emojis": "#ff9800"
        }
        
        category_icons = {
            "Animals": "🦁",
            "Fruits": "🍎",
            "Sports": "⚽",
            "Weather": "⛈️",
            "Vehicles": "🚗",
            "Foods": "🍕",
            "Nature": "🌺",
            "Emojis": "😀"
        }
        
        card_frame = tk.Frame(categories_frame, bg=COLORS["background"])
        card_frame.pack()
        
        for i, category in enumerate(CATEGORIES.keys()):
            cat_color = category_colors.get(category, COLORS["button"])
            cat_icon = category_icons.get(category, "🎮")
            
            btn_container = tk.Frame(card_frame, bg=COLORS["background"])
            btn_container.grid(row=i//2, column=i%2, padx=15, pady=15)
            
            icon_label = tk.Label(btn_container, text=cat_icon, 
                                 font=tkfont.Font(family="Segoe UI Emoji", size=48),
                                 bg=COLORS["background"], fg=cat_color)
            icon_label.pack(pady=(0, 5))
            
            btn = tk.Button(btn_container, text=category, 
                          font=tkfont.Font(family="Arial", size=13, weight="bold"),
                          bg=cat_color, fg="white", width=14, height=2,
                          relief="flat", cursor="hand2",
                          activebackground=cat_color,
                          activeforeground="white",
                          command=lambda c=category: self.select_category(c))
            btn.pack()
        
        footer_frame = tk.Frame(self.main_frame, bg=COLORS["panel"], height=60)
        footer_frame.pack(side="bottom", fill="x")
        footer_frame.pack_propagate(False)
        
        info_label = tk.Label(footer_frame, text="🎮 Select a category to start playing! | 🎯 Multiple difficulty levels available", 
                            font=tkfont.Font(family="Arial", size=10), 
                            bg=COLORS["panel"], fg=COLORS["text"])
        info_label.pack(pady=18)
        
    def select_category(self, category):
        self.current_category = category
        self.show_difficulty_selection()
        
    def show_difficulty_selection(self):
        self.clear_frame()
        
        header_container = tk.Frame(self.main_frame, bg=COLORS["background"])
        header_container.pack(fill="x", pady=20)
        
        title = tk.Label(header_container, text=f"🎯 {self.current_category} 🎯", 
                        font=tkfont.Font(family="Arial", size=24, weight="bold"), 
                        bg=COLORS["background"], fg="#f39c12")
        title.pack(pady=10)
        
        subtitle = tk.Label(header_container, text="🎮 Choose Your Difficulty Level 🎮", 
                           font=tkfont.Font(family="Arial", size=14), 
                           bg=COLORS["background"], fg=COLORS["text"])
        subtitle.pack(pady=5)
        
        main_container = tk.Frame(self.main_frame, bg=COLORS["background"])
        main_container.pack(expand=True, fill="both", padx=40, pady=10)
        
        difficulties_frame = tk.Frame(main_container, bg=COLORS["background"])
        difficulties_frame.pack(expand=True)
        
        difficulty_data = [
            ("Easy", "🌟", (4, 3), "#2ecc71", "Perfect for beginners!"),
            ("Medium", "⭐", (4, 4), "#3498db", "A balanced challenge!"),
            ("Hard", "💪", (6, 5), "#e67e22", "Test your skills!"),
            ("Expert", "🏆", (6, 6), "#e74c3c", "For memory masters!")
        ]
        
        for idx, (difficulty, icon, size, color, desc) in enumerate(difficulty_data):
            row = idx // 2
            col = idx % 2
            
            btn_text = f"{icon}\n\n{difficulty}\n{size[0]} × {size[1]} Grid\n\n{desc}"
            btn = tk.Button(difficulties_frame, text=btn_text, 
                           bg=color, fg="white", 
                           font=tkfont.Font(family="Segoe UI Emoji", size=10),
                           width=20, height=8,
                           relief="raised", bd=4, cursor="hand2",
                           command=lambda d=difficulty, s=size: self.select_difficulty(d, s))
            btn.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        
        difficulties_frame.grid_columnconfigure(0, weight=1)
        difficulties_frame.grid_columnconfigure(1, weight=1)
        difficulties_frame.grid_rowconfigure(0, weight=1)
        difficulties_frame.grid_rowconfigure(1, weight=1)
        
        footer_frame = tk.Frame(self.main_frame, bg=COLORS["panel"], height=60)
        footer_frame.pack(side="bottom", fill="x")
        footer_frame.pack_propagate(False)
        
        back_btn = tk.Button(footer_frame, text="← Back to Categories", 
                            font=tkfont.Font(family="Arial", size=12), 
                            bg=COLORS["button"], fg=COLORS["text"], width=20,
                            cursor="hand2",
                            command=self.show_category_selection)
        back_btn.pack(pady=15)
        
    def select_difficulty(self, difficulty, size):
        self.current_difficulty = difficulty
        self.grid_size = size
        self.start_game()
        
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        for animation_id in self.flip_animation_ids:
            self.root.after_cancel(animation_id)
        self.flip_animation_ids.clear()
        
    def start_game(self):
        self.clear_frame()
        
        self.cards = []
        self.flipped_cards = []
        self.matched_pairs = 0
        self.moves = 0
        self.game_active = True
        self.start_time = time.time()
        
        total_cells = self.grid_size[0] * self.grid_size[1]
        if total_cells % 2 != 0:
            total_cells -= self.grid_size[1]
        self.total_pairs = total_cells // 2
        
        self.create_header()
        self.create_game_board()
        
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg=COLORS["panel"], height=100)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        category_label = tk.Label(header_frame, 
                                 text=f"🎯 {self.current_category}", 
                                 font=tkfont.Font(family="Arial", size=18, weight="bold"), 
                                 bg=COLORS["panel"], fg="#f39c12")
        category_label.pack(pady=(5, 10))
        
        info_frame = tk.Frame(header_frame, bg=COLORS["panel"])
        info_frame.pack()
        
        moves_container = tk.Frame(info_frame, bg=COLORS["panel"])
        moves_container.pack(side="left", padx=20)
        tk.Label(moves_container, text="Moves", 
                font=tkfont.Font(family="Arial", size=9), 
                bg=COLORS["panel"], fg="#bdc3c7").pack()
        self.moves_label = tk.Label(moves_container, text="0", 
                                   font=tkfont.Font(family="Arial", size=20, weight="bold"),
                                   bg=COLORS["panel"], fg=COLORS["text"])
        self.moves_label.pack()
        
        time_container = tk.Frame(info_frame, bg=COLORS["panel"])
        time_container.pack(side="left", padx=20)
        tk.Label(time_container, text="Time", 
                font=tkfont.Font(family="Arial", size=9), 
                bg=COLORS["panel"], fg="#bdc3c7").pack()
        self.time_label = tk.Label(time_container, text="0:00", 
                                  font=tkfont.Font(family="Arial", size=20, weight="bold"),
                                  bg=COLORS["panel"], fg=COLORS["text"])
        self.time_label.pack()
        
        pairs_container = tk.Frame(info_frame, bg=COLORS["panel"])
        pairs_container.pack(side="left", padx=20)
        tk.Label(pairs_container, text="Pairs", 
                font=tkfont.Font(family="Arial", size=9), 
                bg=COLORS["panel"], fg="#bdc3c7").pack()
        self.pairs_label = tk.Label(pairs_container, 
                                   text=f"0/{self.total_pairs}", 
                                   font=tkfont.Font(family="Arial", size=20, weight="bold"),
                                   bg=COLORS["panel"], fg=COLORS["text"])
        self.pairs_label.pack()
        
        self.update_time()
        
    def update_time(self):
        if self.game_active and self.start_time and hasattr(self, 'time_label') and self.time_label.winfo_exists():
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.time_label.config(text=f"Time: {minutes}:{seconds:02d}")
            self.root.after(1000, self.update_time)
        
    def create_game_board(self):
        total_cells = self.grid_size[0] * self.grid_size[1]
        if total_cells % 2 != 0:
            total_cells -= self.grid_size[1]
        
        symbols = CATEGORIES[self.current_category][:total_cells//2] * 2
        random.shuffle(symbols)
        
        board_frame = tk.Frame(self.main_frame, bg=COLORS["background"])
        board_frame.pack(expand=True, fill="both")
        
        card_width = 85
        card_height = 85
        
        grid_container = tk.Frame(board_frame, bg=COLORS["background"])
        grid_container.place(relx=0.5, rely=0.5, anchor="center")
        
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                idx = row * self.grid_size[1] + col
                if idx < len(symbols):
                    card = Card(grid_container, symbols[idx], idx, 
                               card_width, card_height, self.card_font,
                               COLORS, self.on_card_click)
                    card.grid(row=row, column=col, padx=2, pady=2)
                    self.cards.append(card)
        
        buttons_frame = tk.Frame(self.main_frame, bg=COLORS["panel"], height=70)
        buttons_frame.pack(side="bottom", fill="x")
        buttons_frame.pack_propagate(False)
        
        button_container = tk.Frame(buttons_frame, bg=COLORS["panel"])
        button_container.pack(pady=12)
        
        restart_btn = tk.Button(button_container, text="🔄 Restart Game", 
                               font=tkfont.Font(family="Arial", size=12, weight="bold"),
                               bg=COLORS["button"], fg=COLORS["text"], width=15, height=2,
                               relief="flat", cursor="hand2",
                               activebackground=COLORS["button_hover"],
                               command=self.start_game)
        restart_btn.pack(side="left", padx=15)
        
        back_btn = tk.Button(button_container, text="← Back to Menu", 
                           font=tkfont.Font(family="Arial", size=12, weight="bold"),
                           bg=COLORS["accent"], fg="white", width=15, height=2,
                           relief="flat", cursor="hand2",
                           activebackground="#c0392b",
                           command=self.show_category_selection)
        back_btn.pack(side="left", padx=15)
        
    def on_card_click(self, card):
        if not self.game_active or card.flipped or card.matched:
            return
        
        if len(self.flipped_cards) >= 2:
            return
        
        card.flip()
        self.flipped_cards.append(card)
        
        if len(self.flipped_cards) == 2:
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            self.root.after(800, self.check_match)
            
    def check_match(self):
        if len(self.flipped_cards) != 2:
            return
        
        card1, card2 = self.flipped_cards
        
        if card1.symbol == card2.symbol:
            card1.set_matched()
            card2.set_matched()
            self.matched_pairs += 1
            self.pairs_label.config(text=f"Pairs: {self.matched_pairs}/{self.total_pairs}")
            
            if self.matched_pairs == self.total_pairs:
                self.game_active = False
                self.show_victory()
        else:
            card1.flip()
            card2.flip()
        
        self.flipped_cards.clear()
        
    def show_victory(self):
        elapsed = int(time.time() - (self.start_time or time.time()))
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        victory_window = tk.Toplevel(self.root)
        victory_window.title("🎉 Victory! 🎉")
        victory_window.geometry("500x550")
        victory_window.configure(bg=COLORS["background"])
        victory_window.resizable(False, False)
        victory_window.transient(self.root)
        victory_window.grab_set()
        
        header_frame = tk.Frame(victory_window, bg="#1abc9c", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🏆 VICTORY! 🏆", 
                font=tkfont.Font(family="Arial", size=32, weight="bold"), 
                bg="#1abc9c", fg="white").pack(pady=(25, 5))
        
        tk.Label(header_frame, text="Congratulations, Champion!", 
                font=tkfont.Font(family="Arial", size=11), 
                bg="#1abc9c", fg="#ecf0f1").pack()
        
        content_frame = tk.Frame(victory_window, bg=COLORS["background"])
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        stats_container = tk.Frame(content_frame, bg=COLORS["background"])
        stats_container.pack(fill="both", expand=True)
        
        stat_items = [
            ("🎯", "Category", self.current_category),
            ("⚡", "Difficulty", self.current_difficulty),
            ("🎮", "Moves", str(self.moves)),
            ("⏱️", "Time", f"{minutes}:{seconds:02d}")
        ]
        
        for idx, (icon, label, value) in enumerate(stat_items):
            stat_frame = tk.Frame(stats_container, bg=COLORS["panel"], relief="raised", bd=2, height=60)
            stat_frame.pack_propagate(False)
            stat_frame.pack(fill="x", pady=6, padx=5)
            
            icon_label = tk.Label(stat_frame, text=icon, 
                                 font=tkfont.Font(family="Segoe UI Emoji", size=28),
                                 bg=COLORS["panel"], fg="#f39c12", width=3)
            icon_label.pack(side="left", padx=(15, 10), pady=0)
            
            info_frame = tk.Frame(stat_frame, bg=COLORS["panel"])
            info_frame.pack(side="left", padx=5, fill="both", expand=True)
            
            text_frame = tk.Frame(info_frame, bg=COLORS["panel"])
            text_frame.pack(fill="both", expand=True)
            
            tk.Label(text_frame, text=label, 
                    font=tkfont.Font(family="Arial", size=10, weight="bold"),
                    bg=COLORS["panel"], fg="#bdc3c7").pack(side="left", padx=0)
            tk.Label(text_frame, text=value, 
                    font=tkfont.Font(family="Arial", size=15, weight="bold"),
                    bg=COLORS["panel"], fg=COLORS["text"]).pack(side="left", padx=(10, 0))
        
        def play_again():
            victory_window.destroy()
            self.start_game()
            
        def back_to_menu():
            victory_window.destroy()
            self.show_category_selection()
            
        buttons_frame = tk.Frame(content_frame, bg=COLORS["background"])
        buttons_frame.pack(pady=(20, 10))
        
        tk.Button(buttons_frame, text="🔄 Play Again", 
                 font=tkfont.Font(family="Arial", size=12, weight="bold"),
                 bg=COLORS["matched"], fg="white", width=18, height=2,
                 relief="flat", cursor="hand2",
                 command=play_again).pack(side="left", padx=8)
        tk.Button(buttons_frame, text="📋 Main Menu", 
                 font=tkfont.Font(family="Arial", size=12, weight="bold"),
                 bg=COLORS["button"], fg=COLORS["text"], width=18, height=2,
                 relief="flat", cursor="hand2",
                 command=back_to_menu).pack(side="left", padx=8)
        
    def run(self):
        self.root.mainloop()

class Card:
    def __init__(self, parent, symbol, index, width, height, font, colors, on_click):
        self.symbol = symbol
        self.index = index
        self.font = font
        self.colors = colors
        self.on_click = on_click
        self.flipped = False
        self.matched = False
        
        self.canvas = tk.Canvas(parent, width=width, height=height, 
                               bg=colors["card_back"], highlightthickness=0)
        self.canvas.config(cursor="hand2")
        self.canvas.bind("<Button-1>", self.on_click_event)
        
        padding = 6
        inner_width = width - padding * 2
        inner_height = height - padding * 2
        
        self.border_id = self.canvas.create_rectangle(padding, padding, 
                                                     width-padding, height-padding, 
                                                     fill=colors["card_back"], 
                                                     outline="white", width=3)
        
        self.inner_rect_id = self.canvas.create_rectangle(padding+3, padding+3, 
                                                         width-padding-3, height-padding-3, 
                                                         fill=colors["card_back"], 
                                                         outline="", width=0)
        
        self.decor_id = self.canvas.create_text(width//2, height//2 - 10, 
                                               text="?", font=font, 
                                               fill="#ecf0f1")
        
        self.content_id = self.canvas.create_text(width//2, height//2, 
                                                  text="", font=font, 
                                                  fill="#2c3e50", state="hidden")
        
        self.shadow_id = self.canvas.create_rectangle(padding+8, padding+8, 
                                                     width-padding+4, height-padding+4, 
                                                     fill="#2c3e50", outline="", state="hidden")
    
    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)
    
    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)
        
    def on_click_event(self, event):
        if not self.flipped and not self.matched:
            self.on_click(self)
            
    def flip(self):
        if self.flipped:
            self.canvas.itemconfigure(self.border_id, fill=self.colors["card_back"])
            self.canvas.itemconfigure(self.inner_rect_id, fill=self.colors["card_back"])
            self.canvas.itemconfigure(self.content_id, state="hidden")
            self.canvas.itemconfigure(self.decor_id, state="normal", text="?")
            self.canvas.itemconfigure(self.shadow_id, state="hidden")
        else:
            self.canvas.itemconfigure(self.border_id, fill=self.colors["card_front"])
            self.canvas.itemconfigure(self.inner_rect_id, fill=self.colors["card_front"])
            self.canvas.itemconfigure(self.content_id, state="normal", text=self.symbol)
            self.canvas.itemconfigure(self.decor_id, state="hidden")
            self.canvas.itemconfigure(self.shadow_id, state="hidden")
        self.flipped = not self.flipped
        
    def set_matched(self):
        self.matched = True
        self.canvas.itemconfigure(self.border_id, fill=self.colors["matched"], 
                                outline="white", width=4)
        self.canvas.itemconfigure(self.inner_rect_id, fill=self.colors["matched"])
        self.canvas.itemconfigure(self.shadow_id, state="normal")
        self.canvas.tag_lower(self.shadow_id)
        self.canvas.config(cursor="")

if __name__ == "__main__":
    game = MemoryGame()
    game.run()
