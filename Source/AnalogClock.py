import tkinter as tk
import time
import math
from datetime import datetime

class AnalogClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Analog Clock")
        self.root.resizable(False, False)
        self.root.geometry("500x550")
        self.canvas = tk.Canvas(root, width=500, height=500, bg='#1a1a2e')
        self.canvas.pack()
        self.center_x = 250
        self.center_y = 230
        self.radius = 150
        self.background_drawn = False
        self.init_clock_face()
        self.update_clock()

    def draw_gradient_background(self):
        if self.background_drawn:
            return
        gradient = ['#0f0f1a', '#1a1a2e', '#252540', '#303055', '#1a1a2e', '#0f0f1a']
        segment_height = 500 // len(gradient)
        for i, color in enumerate(gradient):
            self.canvas.create_rectangle(0, i * segment_height, 500, (i + 1) * segment_height, fill=color, outline='', tags='background')
        self.background_drawn = True

    def draw_decorative_circle(self, x, y, r, color, width, tags='clock'):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, outline=color, width=width, tags=tags)

    def draw_hand(self, angle, length, width, color, tags='hand'):
        angle_rad = math.radians(angle)
        end_x = self.center_x + length * math.cos(angle_rad)
        end_y = self.center_y + length * math.sin(angle_rad)
        
        back_x = self.center_x - length * 0.15 * math.cos(angle_rad)
        back_y = self.center_y - length * 0.15 * math.sin(angle_rad)
        
        self.canvas.create_line(back_x, back_y, end_x, end_y, width=width, fill=color, capstyle=tk.ROUND, tags=tags)

    def draw_clock_face(self):
        shadow_offset = 5
        self.draw_decorative_circle(self.center_x + shadow_offset, self.center_y + shadow_offset, self.radius + 15, '#0a0a15', 0)
        
        self.draw_decorative_circle(self.center_x, self.center_y, self.radius + 20, '#5c5c80', 5)
        self.draw_decorative_circle(self.center_x, self.center_y, self.radius + 12, '#4a4a6a', 2)
        self.draw_decorative_circle(self.center_x, self.center_y, self.radius + 5, '#3a3a5a', 3)
        self.draw_decorative_circle(self.center_x, self.center_y, self.radius, '#2a2a4a', 4)
        self.draw_decorative_circle(self.center_x, self.center_y, self.radius - 3, '#4a4a7a', 1)
        
        inner_radius = self.radius - 25
        self.canvas.create_oval(self.center_x - inner_radius, self.center_y - inner_radius,
                                self.center_x + inner_radius, self.center_y + inner_radius,
                                fill='#e8e8f8', outline='#b8b8d8', width=3, tags='clock')
        
        self.canvas.create_oval(self.center_x - inner_radius + 15, self.center_y - inner_radius + 15,
                                self.center_x + inner_radius - 15, self.center_y + inner_radius - 15,
                                outline='#d8d8f8', width=1, dash=(5, 5), tags='clock')
        
        self.draw_decorative_circle(self.center_x, self.center_y, 40, '#c8c8e8', 2, 'clock')

        quadrant_colors = ['#ff6b6b', '#4ecdc4', '#ffe66d', '#95e1d3']
        for i in range(4):
            angle_start = math.radians(i * 90)
            angle_end = math.radians((i + 1) * 90)
            for r in range(10, 30, 8):
                x = self.center_x + r * math.cos(angle_start + math.pi/4)
                y = self.center_y + r * math.sin(angle_start + math.pi/4)
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=quadrant_colors[i], outline='', tags='clock')

        for i in range(12):
            angle = math.radians(i * 30 - 90)
            text_radius = self.radius * 0.72
            x = self.center_x + text_radius * math.cos(angle)
            y = self.center_y + text_radius * math.sin(angle)
            number = 12 if i == 0 else i
            
            bg_x = self.center_x + (self.radius * 0.78) * math.cos(angle)
            bg_y = self.center_y + (self.radius * 0.78) * math.sin(angle)
            self.canvas.create_oval(bg_x - 18, bg_y - 18, bg_x + 18, bg_y + 18, fill='#f0f0f5', outline='#c0c0d0', width=1, tags='clock')
            
            self.canvas.create_text(x, y, text=str(number), font=("Times New Roman", 20, "bold"), fill='#2c3e50', tags='clock')
            
            tick_x = self.center_x + self.radius * 0.86 * math.cos(angle)
            tick_y = self.center_y + self.radius * 0.86 * math.sin(angle)
            tick_end_x = self.center_x + self.radius * 0.94 * math.cos(angle)
            tick_end_y = self.center_y + self.radius * 0.94 * math.sin(angle)
            self.canvas.create_line(tick_x, tick_y, tick_end_x, tick_end_y, width=5, fill='#1a1a2e', capstyle=tk.ROUND, tags='clock')

        for i in range(60):
            if i % 5 != 0:
                angle = math.radians(i * 6 - 90)
                tick_x = self.center_x + self.radius * 0.90 * math.cos(angle)
                tick_y = self.center_y + self.radius * 0.90 * math.sin(angle)
                tick_end_x = self.center_x + self.radius * 0.96 * math.cos(angle)
                tick_end_y = self.center_y + self.radius * 0.96 * math.sin(angle)
                self.canvas.create_line(tick_x, tick_y, tick_end_x, tick_end_y, width=2, fill='#8888aa', capstyle=tk.ROUND, tags='clock')
        
        self.canvas.create_text(self.center_x, self.center_y + 80, text="QUARTZ", font=("Arial", 8, "bold"), fill='#8888aa', tags='clock')
        self.canvas.create_text(self.center_x, self.center_y - 80, text="SWISS", font=("Arial", 8, "bold"), fill='#8888aa', tags='clock')

    def init_clock_face(self):
        self.draw_gradient_background()
        self.draw_clock_face()

    def update_clock(self):
        self.canvas.delete('hand', 'digital', 'center')
        
        now = time.localtime()
        hours = now.tm_hour % 12
        minutes = now.tm_min
        seconds = now.tm_sec
        milliseconds = int(time.time() * 1000) % 1000

        hour_angle = (hours + minutes / 60) * 30 - 90
        minute_angle = (minutes + seconds / 60) * 6 - 90
        second_angle = (seconds + milliseconds / 1000) * 6 - 90

        self.draw_hand(hour_angle, self.radius * 0.5, 7, '#2c3e50', 'hand')
        self.draw_hand(minute_angle, self.radius * 0.75, 5, '#34495e', 'hand')
        self.draw_hand(second_angle, self.radius * 0.85, 2, '#e74c3c', 'hand')

        self.canvas.create_oval(self.center_x - 8, self.center_y - 8, self.center_x + 8, self.center_y + 8, fill='#c0392b', outline='#e74c3c', width=2, tags='center')
        self.canvas.create_oval(self.center_x - 4, self.center_y - 4, self.center_x + 4, self.center_y + 4, fill='#2c3e50', tags='center')

        time_str = time.strftime("%H:%M:%S", now)
        date_str = time.strftime("%A, %B %d, %Y", now)
        
        self.canvas.create_text(self.center_x, 420, text=time_str, font=("Consolas", 28, "bold"), fill='#ecf0f1', tags='digital')
        self.canvas.create_text(self.center_x, 460, text=date_str, font=("Arial", 12), fill='#95a5a6', tags='digital')

        self.root.after(50, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    clock = AnalogClock(root)
    root.mainloop()
