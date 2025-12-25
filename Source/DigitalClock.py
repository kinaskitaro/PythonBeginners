import tkinter as tk
from tkinter import ttk, colorchooser
from datetime import datetime
import pytz

class DigitalClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Digital Clock")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        self.is_24hour = True
        self.show_date = True
        self.show_day = True
        self.show_seconds = True
        self.is_fullscreen = False
        
        self.themes = {
            "Neon": {
                "bg": "#000000",
                "time": "#00ffea",
                "day": "#ff4d4d",
                "date": "#e0e0e0",
                "gradient": [(5, 10, 25), (15, 30, 75)]
            },
            "Sunset": {
                "bg": "#1a0a0a",
                "time": "#ff6b6b",
                "day": "#ffd93d",
                "date": "#ffb347",
                "gradient": [(26, 10, 10), (80, 40, 30)]
            },
            "Ocean": {
                "bg": "#000a1a",
                "time": "#00d4ff",
                "day": "#00ff88",
                "date": "#0099cc",
                "gradient": [(0, 10, 26), (0, 60, 100)]
            },
            "Forest": {
                "bg": "#0a1a0a",
                "time": "#00ff00",
                "day": "#90ee90",
                "date": "#32cd32",
                "gradient": [(10, 26, 10), (50, 100, 50)]
            }
        }
        self.current_theme = "Neon"
        
        self.timezones = [
            "UTC",
            "Asia/Ho_Chi_Minh",
            "America/New_York",
            "America/Los_Angeles",
            "Europe/London",
            "Europe/Paris",
            "Asia/Tokyo",
            "Australia/Sydney"
        ]
        self.current_tz = "Asia/Ho_Chi_Minh"
        
        self.setup_ui()
        self.update_time()
        self.root.mainloop()
    
    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.draw_gradient()
        
        self.settings_button = tk.Button(
            self.canvas,
            text="⚙ Settings",
            command=self.open_settings,
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["time"],
            font=("Arial", 10),
            relief="flat",
            padx=10
        )
        self.settings_button_window = self.canvas.create_window(20, 20, anchor="nw", window=self.settings_button)
        
        self.fullscreen_button = tk.Button(
            self.canvas,
            text="⛶ Fullscreen",
            command=self.toggle_fullscreen,
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["time"],
            font=("Arial", 10),
            relief="flat",
            padx=10
        )
        self.fullscreen_button_window = self.canvas.create_window(120, 20, anchor="nw", window=self.fullscreen_button)
        
        self.clock_frame = tk.Frame(self.canvas, bg=self.themes[self.current_theme]["bg"])
        self.clock_frame_window = self.canvas.create_window(300, 200, window=self.clock_frame)
        
        self.time_label = tk.Label(
            self.clock_frame,
            text="00:00:00",
            font=("Arial", 72, "bold"),
            fg=self.themes[self.current_theme]["time"],
            bg=self.themes[self.current_theme]["bg"],
            pady=10
        )
        self.time_label.pack(anchor="center")
        
        self.day_label = tk.Label(
            self.clock_frame,
            text="Day",
            font=("Arial", 24, "bold"),
            fg=self.themes[self.current_theme]["day"],
            bg=self.themes[self.current_theme]["bg"]
        )
        self.day_label.pack(anchor="center")
        
        self.date_label = tk.Label(
            self.clock_frame,
            text="Date",
            font=("Arial", 16, "italic"),
            fg=self.themes[self.current_theme]["date"],
            bg=self.themes[self.current_theme]["bg"],
            pady=5
        )
        self.date_label.pack(anchor="center")
        
        self.canvas.bind("<Configure>", self.on_resize)
    
    def draw_gradient(self):
        theme = self.themes[self.current_theme]
        start, end = theme["gradient"]
        height = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 400
        width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 600
        
        for i in range(height):
            r = int(start[0] + (end[0] - start[0]) * i / height)
            g = int(start[1] + (end[1] - start[1]) * i / height)
            b = int(start[2] + (end[2] - start[2]) * i / height)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_rectangle(0, i, width, i+1, fill=color, outline="", tags="gradient")
    
    def on_resize(self, event):
        self.canvas.delete("gradient")
        self.draw_gradient()
        self.canvas.coords(self.clock_frame_window, event.width/2, event.height/2)
    
    def update_time(self):
        try:
            tz = pytz.timezone(self.current_tz)
            current_time = datetime.now(tz)
            
            if self.is_24hour:
                if self.show_seconds:
                    time_string = current_time.strftime("%H:%M:%S")
                else:
                    time_string = current_time.strftime("%H:%M")
            else:
                period = current_time.strftime("%p")
                if self.show_seconds:
                    time_string = current_time.strftime("%I:%M:%S")
                else:
                    time_string = current_time.strftime("%I:%M")
                time_string += f" {period}"
            
            day_string = current_time.strftime("%A")
            date_string = current_time.strftime("%B %d, %Y")
            tz_display = self.current_tz.split("/")[-1].replace("_", " ")
            
            self.time_label.config(text=time_string)
            
            if self.show_day:
                self.day_label.config(text=day_string)
                self.day_label.pack(anchor="center")
            else:
                self.day_label.pack_forget()
            
            if self.show_date:
                self.date_label.config(text=f"{date_string} • {tz_display}")
                self.date_label.pack(anchor="center")
            else:
                self.date_label.pack_forget()
            
            self.root.after(1000, self.update_time)
        except Exception as e:
            print(f"Error in update_time: {e}")
    
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x450")
        settings_window.resizable(False, False)
        settings_window.configure(bg=self.themes[self.current_theme]["bg"])
        
        theme_frame = tk.LabelFrame(settings_window, text="Theme", bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["time"])
        theme_frame.pack(fill="x", padx=10, pady=10)
        
        theme_var = tk.StringVar(value=self.current_theme)
        for theme in self.themes.keys():
            rb = tk.Radiobutton(
                theme_frame,
                text=theme,
                variable=theme_var,
                value=theme,
                command=lambda: self.change_theme(theme_var.get()),
                bg=self.themes[self.current_theme]["bg"],
                fg=self.themes[self.current_theme]["time"],
                selectcolor=self.themes[self.current_theme]["bg"],
                activebackground=self.themes[self.current_theme]["bg"],
                activeforeground=self.themes[self.current_theme]["time"]
            )
            rb.pack(anchor="w", padx=10)
        
        tz_frame = tk.LabelFrame(settings_window, text="Timezone", bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["time"])
        tz_frame.pack(fill="x", padx=10, pady=10)
        
        tz_combo = ttk.Combobox(tz_frame, values=self.timezones, state="readonly")
        tz_combo.set(self.current_tz)
        tz_combo.pack(fill="x", padx=10, pady=5)
        tz_combo.bind("<<ComboboxSelected>>", lambda e: self.change_timezone(tz_combo.get()))
        
        options_frame = tk.LabelFrame(settings_window, text="Display Options", bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["time"])
        options_frame.pack(fill="x", padx=10, pady=10)
        
        hour_var = tk.BooleanVar(value=self.is_24hour)
        hour_check = tk.Checkbutton(
            options_frame,
            text="24-Hour Format",
            variable=hour_var,
            command=lambda: self.toggle_24hour(hour_var.get()),
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["time"],
            selectcolor=self.themes[self.current_theme]["bg"],
            activebackground=self.themes[self.current_theme]["bg"],
            activeforeground=self.themes[self.current_theme]["time"]
        )
        hour_check.pack(anchor="w", padx=10)
        
        seconds_var = tk.BooleanVar(value=self.show_seconds)
        seconds_check = tk.Checkbutton(
            options_frame,
            text="Show Seconds",
            variable=seconds_var,
            command=lambda: self.toggle_seconds(seconds_var.get()),
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["time"],
            selectcolor=self.themes[self.current_theme]["bg"],
            activebackground=self.themes[self.current_theme]["bg"],
            activeforeground=self.themes[self.current_theme]["time"]
        )
        seconds_check.pack(anchor="w", padx=10)
        
        date_var = tk.BooleanVar(value=self.show_date)
        date_check = tk.Checkbutton(
            options_frame,
            text="Show Date",
            variable=date_var,
            command=lambda: self.toggle_date(date_var.get()),
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["time"],
            selectcolor=self.themes[self.current_theme]["bg"],
            activebackground=self.themes[self.current_theme]["bg"],
            activeforeground=self.themes[self.current_theme]["time"]
        )
        date_check.pack(anchor="w", padx=10)
        
        day_var = tk.BooleanVar(value=self.show_day)
        day_check = tk.Checkbutton(
            options_frame,
            text="Show Day",
            variable=day_var,
            command=lambda: self.toggle_day(day_var.get()),
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["time"],
            selectcolor=self.themes[self.current_theme]["bg"],
            activebackground=self.themes[self.current_theme]["bg"],
            activeforeground=self.themes[self.current_theme]["time"]
        )
        day_check.pack(anchor="w", padx=10)
    
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
        self.canvas.delete("gradient")
        self.draw_gradient()
        
        self.clock_frame.config(bg=theme["bg"])
        self.time_label.config(fg=theme["time"], bg=theme["bg"])
        self.day_label.config(fg=theme["day"], bg=theme["bg"])
        self.date_label.config(fg=theme["date"], bg=theme["bg"])
        
        self.settings_button.config(bg=theme["bg"], fg=theme["time"])
        self.fullscreen_button.config(bg=theme["bg"], fg=theme["time"])
    
    def change_timezone(self, tz_name):
        self.current_tz = tz_name
    
    def toggle_24hour(self, value):
        self.is_24hour = value
    
    def toggle_seconds(self, value):
        self.show_seconds = value
    
    def toggle_date(self, value):
        self.show_date = value
    
    def toggle_day(self, value):
        self.show_day = value
    
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        self.fullscreen_button.config(text="⛶ Exit" if self.is_fullscreen else "⛶ Fullscreen")
        
        if self.is_fullscreen:
            self.root.bind("<Escape>", lambda e: self.toggle_fullscreen())

if __name__ == "__main__":
    DigitalClock()