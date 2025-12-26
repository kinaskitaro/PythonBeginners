import os
import sys

def run_game_file(filepath):
    try:
        # Change to correct directory so games find assets
        if getattr(sys, 'frozen', False):
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
            os.chdir(base_dir)
        
        # Execute the game file
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
        # Run the launcher
        import tkinter as tk
        from tkinter import ttk, messagebox, font as tkfont
        import subprocess

        class PythonLauncher:
            def __init__(self):
                self.root = tk.Tk()
                self.root.title("Python Game Launcher")
                self.root.geometry("700x500")
                
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
                return files
            
            def setup_ui(self):
                self.root.configure(bg="#2C3E50")
                
                title_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
                label_font = tkfont.Font(family="Helvetica", size=12)
                button_font = tkfont.Font(family="Helvetica", size=11)
                
                title_label = tk.Label(
                    self.root,
                    text="Python Game Launcher",
                    font=title_font,
                    bg="#2C3E50",
                    fg="#ECF0F1"
                )
                title_label.pack(pady=(30, 20))
                
                subtitle_label = tk.Label(
                    self.root,
                    text=f"Found {len(self.python_files)} Python files in Source directory",
                    font=label_font,
                    bg="#2C3E50",
                    fg="#BDC3C7"
                )
                subtitle_label.pack(pady=(0, 20))
                
                main_frame = tk.Frame(self.root, bg="#34495E", padx=20, pady=20)
                main_frame.pack(pady=10, padx=50, fill=tk.BOTH, expand=True)
                
                canvas = tk.Canvas(main_frame, bg="#34495E", highlightthickness=0)
                scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg="#34495E")
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                
                def on_mousewheel(event):
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                
                canvas.bind("<MouseWheel>", on_mousewheel)
                canvas.bind_all("<MouseWheel>", on_mousewheel)
                
                canvas.pack(side="left", fill=tk.BOTH, expand=True)
                scrollbar.pack(side="right", fill=tk.Y)
                
                if not self.python_files:
                    no_files_label = tk.Label(
                        scrollable_frame,
                        text="No Python files found in the Source directory.",
                        font=label_font,
                        bg="#34495E",
                        fg="#E74C3C"
                    )
                    no_files_label.pack(pady=50)
                else:
                    self.create_file_buttons(scrollable_frame, button_font)
                
                bottom_frame = tk.Frame(self.root, bg="#2C3E50")
                bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
                
                info_label = tk.Label(
                    bottom_frame,
                    text="Select a project above to run it",
                    font=label_font,
                    bg="#2C3E50",
                    fg="#95A5A6"
                )
                info_label.pack()
            
            def create_file_buttons(self, parent, font):
                for idx, filename in enumerate(self.python_files):
                    display_name = filename.replace(".py", "")
                    
                    button_frame = tk.Frame(parent, bg="#34495E", pady=8)
                    button_frame.pack(fill=tk.X, padx=10)
                    
                    num_label = tk.Label(
                        button_frame,
                        text=f"{idx + 1}.",
                        font=font,
                        bg="#34495E",
                        fg="#3498DB",
                        width=3,
                        anchor="w"
                    )
                    num_label.pack(side=tk.LEFT)
                    
                    run_button = tk.Button(
                        button_frame,
                        text=display_name,
                        font=font,
                        bg="#3498DB",
                        fg="white",
                        activebackground="#2980B9",
                        activeforeground="white",
                        relief="flat",
                        cursor="hand2",
                        command=lambda fn=filename: self.run_python_file(fn),
                        pady=8,
                        padx=20
                    )
                    run_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            def run_python_file(self, filename):
                filepath = os.path.join(self.source_dir, filename)
                display_name = filename.replace(".py", "")
                
                try:
                    result = messagebox.askyesno(
                        "Run Project",
                        f"Do you want to run '{display_name}'?\n\nFile: {filename}",
                        icon="question"
                    )
                    if result:
                        # Launch game in new process
                        subprocess.Popen(f'"{sys.executable}" "{filepath}"', shell=True)
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"Failed to run {filename}:\n{str(e)}"
                    )
            
            def run(self):
                self.root.mainloop()

        app = PythonLauncher()
        app.run()
