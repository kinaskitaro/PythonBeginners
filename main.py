import os
import sys
import re

GAME_ICONS = {
    "2048": "🎯",
    "AnalogClock": "🕐",
    "Calculator": "🧮",
    "Converter": "🔄",
    "DigitalClock": "⏰",
    "Dinosaur": "🦖",
    "LanguageTrans": "🌐",
    "MemGame": "🧠",
    "Snake": "🐍",
    "Sudoku": "🔢",
    "Tetris": "🧩",
    "TicTacToe": "⭕",
    "Triangle": "📐",
    "Weather": "🌤️",
    "WordGuess": "❓"
}

def get_game_title(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title_match = re.search(r'title\s*\(\s*[\'"]([^\'"]+)[\'"]', content)
        if title_match:
            title = title_match.group(1)
            title = re.sub(r'[^\x00-\x7F]+', '', title)
            return title.strip()
    except:
        pass
    return None

def run_game_file(filepath):
    try:
        if getattr(sys, 'frozen', False):
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
            os.chdir(base_dir)
        
        exec_globals = {'__name__': '__main__', '__file__': filepath}
        with open(filepath, 'r', encoding='utf-8') as f:
            exec(f.read(), exec_globals)
    except Exception as e:
        print(f"Error running {filepath}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].endswith('.py'):
        run_game_file(sys.argv[1])
    else:
        import tkinter as tk
        from tkinter import ttk, messagebox, font as tkfont
        import subprocess

        COLORS = {
            "background": "#1a1a2e",
            "card": "#16213e",
            "card_hover": "#1f3a5e",
            "accent": "#e94560",
            "text": "#ecf0f1",
            "secondary": "#bdc3c7",
            "success": "#2ecc71"
        }

        class PythonLauncher:
            def __init__(self):
                self.root = tk.Tk()
                self.root.title("Python Game Launcher")
                self.root.geometry("900x650")
                self.root.configure(bg=COLORS["background"])
                self.root.resizable(False, False)
                
                if getattr(sys, 'frozen', False):
                    self.base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
                else:
                    self.base_dir = os.path.dirname(os.path.abspath(__file__))
                
                self.source_dir = os.path.join(self.base_dir, "Source")
                self.python_files = self.get_python_files()
                
                self.setup_ui()
            
            def get_python_files(self):
                files = []
                if os.path.exists(self.source_dir):
                    files = [f for f in os.listdir(self.source_dir) if f.endswith(".py") and f != "main.py"]
                return sorted(files)
            
            def setup_ui(self):
                title_font = tkfont.Font(family="Arial", size=32, weight="bold")
                subtitle_font = tkfont.Font(family="Arial", size=14)
                card_title_font = tkfont.Font(family="Arial", size=14, weight="bold")
                card_desc_font = tkfont.Font(family="Arial", size=10)
                
                header_frame = tk.Frame(self.root, bg=COLORS["background"])
                header_frame.pack(fill="x", pady=25)
                
                tk.Label(header_frame, text="🎮 Python Game Launcher 🎮", 
                        font=title_font, bg=COLORS["background"], fg="#f39c12").pack(pady=(0, 10))
                
                tk.Label(header_frame, text=f"Discover {len(self.python_files)} amazing Python projects", 
                        font=subtitle_font, bg=COLORS["background"], fg=COLORS["secondary"]).pack()
                
                main_frame = tk.Frame(self.root, bg=COLORS["background"])
                main_frame.pack(fill="both", expand=True, padx=40, pady=10)
                
                canvas = tk.Canvas(main_frame, bg=COLORS["background"], highlightthickness=0)
                scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg=COLORS["background"])
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                
                def on_mousewheel(event):
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                
                canvas.bind("<MouseWheel>", on_mousewheel)
                canvas.bind_all("<MouseWheel>", on_mousewheel)
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill=tk.Y)
                
                if not self.python_files:
                    no_files_label = tk.Label(
                        scrollable_frame,
                        text="🔍 No Python files found in Source directory",
                        font=tkfont.Font(family="Arial", size=16),
                        bg=COLORS["background"],
                        fg=COLORS["accent"]
                    )
                    no_files_label.pack(pady=80)
                else:
                    self.create_game_cards(scrollable_frame, card_title_font, card_desc_font)
                
                footer_frame = tk.Frame(self.root, bg=COLORS["card"], height=60)
                footer_frame.pack(side="bottom", fill="x")
                footer_frame.pack_propagate(False)
                
                tk.Label(footer_frame, text="✨ Click on any game card to launch it ✨", 
                        font=tkfont.Font(family="Arial", size=11), 
                        bg=COLORS["card"], fg=COLORS["secondary"]).pack(pady=18)
            
            def create_game_cards(self, parent, title_font, desc_font):
                grid_container = tk.Frame(parent, bg=COLORS["background"])
                grid_container.pack(pady=10)
                
                cols = 3
                for idx, filename in enumerate(self.python_files):
                    row = idx // cols
                    col = idx % cols
                    
                    filepath = os.path.join(self.source_dir, filename)
                    game_name = filename.replace(".py", "")
                    game_title = get_game_title(filepath) or game_name.title()
                    icon = GAME_ICONS.get(game_name, "🎮")
                    
                    card_frame = tk.Frame(grid_container, bg=COLORS["card"], 
                                        relief="raised", bd=3, width=230, height=145,
                                        cursor="hand2")
                    card_frame.pack_propagate(False)
                    card_frame.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
                    
                    header = tk.Frame(card_frame, bg=COLORS["card"])
                    header.pack(fill="x", pady=(12, 5))
                    
                    tk.Label(header, text=icon, 
                            font=tkfont.Font(family="Segoe UI Emoji", size=28),
                            bg=COLORS["card"], fg="#f39c12").pack()
                    
                    tk.Label(card_frame, text=game_title, 
                            font=title_font, bg=COLORS["card"], 
                            fg=COLORS["text"], wraplength=210).pack(pady=(6, 4))
                    
                    tk.Label(card_frame, text=f"📁 {filename}", 
                            font=desc_font, bg=COLORS["card"], 
                            fg=COLORS["secondary"]).pack(pady=(0, 8))
                    
                    card_frame.bind("<Button-1>", lambda e, fn=filename: self.run_python_file(fn))
                
                for col in range(cols):
                    grid_container.grid_columnconfigure(col, weight=1)
            
            def run_python_file(self, filename):
                filepath = os.path.join(self.source_dir, filename)
                game_name = filename.replace(".py", "")
                game_title = get_game_title(filepath) or game_name.title()
                
                try:
                    result = messagebox.askyesno(
                        "🎮 Launch Game",
                        f"Ready to play: {game_title}?\n\n📁 File: {filename}",
                        icon="question"
                    )
                    if result:
                        subprocess.Popen(f'"{sys.executable}" "{filepath}"', shell=True)
                except Exception as e:
                    messagebox.showerror(
                        "❌ Error",
                        f"Failed to run {filename}:\n{str(e)}"
                    )
            
            def run(self):
                self.root.mainloop()

        app = PythonLauncher()
        app.run()
