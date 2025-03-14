import tkinter as tk
from datetime import datetime
import pytz

# Constants
WINDOW_TITLE = "Digital Clock"
WINDOW_SIZE = "500x300"
BACKGROUND_COLOR = "#000000"
TIME_FONT = ("Arial", 80, "bold")
DAY_FONT = ("Arial", 28, "bold")
DATE_FONT = ("Arial", 18, "italic")
TIME_COLOR = "#00ffea"
DAY_COLOR = "#ff4d4d"
DATE_COLOR = "#e0e0e0"
SHADOW_COLOR = "#1a1a1a"
BANGKOK_TZ = pytz.timezone('Asia/Bangkok')

def update_time():
    try:
        current_time = datetime.now(BANGKOK_TZ)
        time_string = current_time.strftime("%H:%M:%S")  # 24-hour format with AM/PM
        day_string = current_time.strftime("%A")
        date_string = current_time.strftime("%Y-%m-%d")
        tz_string = "Ho Chi Minh city"
        
        clock_label.config(text=time_string)
        
        day_label.config(text=day_string)
        date_label.config(text=f"{date_string} ({tz_string})")
        
        root.after(1000, update_time)
    except Exception as e:
        print(f"Error in update_time: {e}")

root = tk.Tk()
root.title(WINDOW_TITLE)
root.geometry(WINDOW_SIZE)
root.resizable(False, False)

canvas = tk.Canvas(root, width=500, height=300, highlightthickness=0)
canvas.pack(fill="both", expand=True)

for i in range(300):
    color = f"#{int(10 + i/2):02x}{int(20 + i/2):02x}{int(50 + i/1.5):02x}"
    canvas.create_rectangle(0, i, 500, i+1, fill=color, outline="")

frame = tk.Frame(canvas, bg=BACKGROUND_COLOR, bd=0, relief="flat")
frame_window = canvas.create_window(250, 150, window=frame)

shadow = canvas.create_rectangle(235, 135, 265, 165, fill=SHADOW_COLOR, outline="")

clock_label = tk.Label(frame, text="00:00:00", font=TIME_FONT, fg=TIME_COLOR, bg=BACKGROUND_COLOR, pady=10, padx=20)
clock_label.pack(anchor="center")

day_label = tk.Label(frame, text="Day", font=DAY_FONT, fg=DAY_COLOR, bg=BACKGROUND_COLOR)
day_label.pack(anchor="center")

date_label = tk.Label(frame, text="Date (TZ)", font=DATE_FONT, fg=DATE_COLOR, bg=BACKGROUND_COLOR, pady=10)
date_label.pack(anchor="center")

update_time()
root.mainloop()