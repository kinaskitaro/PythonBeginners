import os
import sys
import re
import subprocess

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
    """Run game file using exec() (for direct python main.py <game.py> calls)"""
    import sys
    import os
    import tkinter
    from tkinter import messagebox
    
    try:
        # Get full path to game file
        if getattr(sys, 'frozen', False):
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
            # filepath is absolute, just use it
            game_path = filepath
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            game_path = os.path.join(script_dir, filepath)
        
        # Set current directory to directory containing the game file
        # This ensures relative paths work (like Assets folder)
        game_dir = os.path.dirname(os.path.abspath(game_path))
        os.chdir(game_dir)
        
        print(f"Running game: {game_path}")
        print(f"Working directory: {game_dir}")
        
        # Read and execute game file
        with open(game_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Don't pre-import tkinter modules in exec_globals
        # Let the game import what it needs normally
        exec_globals = {"__name__": "__main__"}
        exec(code, exec_globals)
    except Exception as e:
        error_msg = f"Error running {os.path.basename(filepath)}:\n{str(e)}\n\nThis game may not be fully compatible with the launcher."
        print(error_msg)
        import traceback
        traceback.print_exc()
        # Show error in popup if tkinter is available
        try:
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showerror("Game Error", error_msg)
        except:
            pass

def launch_game_subprocess(filepath):
    """Launch game in subprocess while keeping launcher open"""
    import subprocess
    import sys
    import os
    
    try:
        if getattr(sys, 'frozen', False):
            # Frozen executable - launch new exe instance
            exe_path = sys.executable
            exe_dir = os.path.dirname(exe_path)
            internal_dir = os.path.join(exe_dir, '_internal')
            
            # Get absolute game path
            if not os.path.isabs(filepath):
                # filepath is just filename, find it in Source/
                game_file = os.path.basename(filepath)
                source_dir = os.path.join(internal_dir, 'Source')
                game_path = os.path.join(source_dir, game_file)
            else:
                game_path = filepath
            
            # Launch new exe instance with game file argument
            # Use CREATE_NEW_CONSOLE so game shows errors
            subprocess.Popen([exe_path, game_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # Development mode - try to use venv Python if available
            script_dir = os.path.dirname(os.path.abspath(__file__))
            venv_python = os.path.join(script_dir, ".venv", "Scripts", "python.exe")
            if os.path.exists(venv_python):
                python = venv_python
            else:
                python = sys.executable
            # Get absolute path to game file
            if not os.path.isabs(filepath):
                filepath = os.path.join(script_dir, filepath)
            game_dir = os.path.dirname(filepath)
            # Pass the current environment to subprocess
            subprocess.Popen([python, filepath], cwd=game_dir, env=os.environ.copy())
        return True
    except Exception as e:
        print(f"Error launching game subprocess: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Check if we should run a game directly (from command line)
    if len(sys.argv) > 1 and sys.argv[1].endswith('.py'):
        filepath = sys.argv[1]
        # Resolve filepath relative to current directory
        if not os.path.isabs(filepath):
            filepath = os.path.abspath(filepath)
        # Execute game directly (not via subprocess to avoid infinite loop)
        run_game_file(filepath)
        sys.exit(0)
    else:
        import tkinter as tk
        from tkinter import ttk, messagebox, font as tkfont

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
                    self.source_dir = os.path.join(self.base_dir, "Source")
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
                    
                    # Outer frame for styling
                    card_frame = tk.Frame(grid_container, bg=COLORS["card"], 
                                        relief="raised", bd=4, width=240, height=155,
                                        cursor="hand2")
                    card_frame.pack_propagate(False)
                    card_frame.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
                    
                    # Content frame
                    content_frame = tk.Frame(card_frame, bg=COLORS["card"])
                    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
                    
                    # Icon
                    icon_label = tk.Label(content_frame, text=icon,
                            font=tkfont.Font(family="Segoe UI Emoji", size=36),
                            bg=COLORS["card"], fg="#f39c12")
                    icon_label.pack(pady=(8, 5))
                    
                    # Title
                    title_label = tk.Label(content_frame, text=game_title,
                            font=title_font, bg=COLORS["card"],
                            fg=COLORS["text"], wraplength=220)
                    title_label.pack(pady=5)
                    
                    # Filename
                    file_label = tk.Label(content_frame, text=f"📁 {filename}",
                            font=desc_font, bg=COLORS["card"],
                            fg=COLORS["secondary"])
                    file_label.pack(pady=(5, 8))
                    
                    # Create event handlers with proper closure to capture widget references
                    def create_handlers(cf, icf, ico, ttl, fl, fn):
                        def on_enter(e):
                            cf.config(bg=COLORS["card_hover"], bd=5, relief="raised")
                            icf.config(bg=COLORS["card_hover"])
                            ico.config(bg=COLORS["card_hover"])
                            ttl.config(bg=COLORS["card_hover"])
                            fl.config(bg=COLORS["card_hover"])
                        
                        def on_leave(e):
                            cf.config(bg=COLORS["card"], bd=4, relief="raised")
                            icf.config(bg=COLORS["card"])
                            ico.config(bg=COLORS["card"])
                            ttl.config(bg=COLORS["card"])
                            fl.config(bg=COLORS["card"])
                        
                        def on_click(e):
                            cf.config(bd=3, relief="sunken")
                            self.root.after(100, lambda: cf.config(bd=5, relief="raised"))
                            self.root.after(150, lambda: self.run_python_file(fn))
                        
                        return on_enter, on_leave, on_click
                    
                    # Create handlers with captured widget references
                    on_enter, on_leave, on_click = create_handlers(
                        card_frame, content_frame, icon_label, title_label, file_label, filename
                    )
                    
                    # Bind to all widgets
                    for widget in [card_frame, content_frame, icon_label, title_label, file_label]:
                        widget.bind("<Enter>", on_enter)
                        widget.bind("<Leave>", on_leave)
                        widget.bind("<Button-1>", on_click)
                
                for col in range(cols):
                    grid_container.grid_columnconfigure(col, weight=1)
            
            def run_python_file(self, filename):
                filepath = os.path.join(self.source_dir, filename)
                game_name = filename.replace(".py", "")
                game_title = get_game_title(filepath) or game_name.title()
                
                try:
                    result = messagebox.askyesno(
                        "🎮 Launch Game",
                        f"Ready to play: {game_title}?\n\n📁 File: {filename}\n\nGame will open in new window.",
                        icon="question"
                    )
                    if result:
                        # Launch game in subprocess (keeps launcher open)
                        success = launch_game_subprocess(filepath)
                        if not success:
                            messagebox.showerror(
                                "❌ Error",
                                f"Failed to launch {filename}"
                            )
                except Exception as e:
                    messagebox.showerror(
                        "❌ Error",
                        f"Failed to run {filename}:\n{str(e)}"
                    )
            
            def run(self):
                self.root.mainloop()

        app = PythonLauncher()
        app.run()
