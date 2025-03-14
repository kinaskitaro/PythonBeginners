import tkinter as tk
import time
import math

class AnalogClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Analog Clock")
        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()
        self.center_x = 200
        self.center_y = 200
        self.radius = 100
        self.canvas.configure(bg='lightblue')
        self.draw_gradient_background()
        self.draw_clock_face()
        self.update_clock()

    def draw_gradient_background(self):
        for i in range(200):
            color = "#%02x%02x%02x" % (255 - i, 255 - i // 2, 255)
            self.canvas.create_line(0, i, 400, i, fill=color)
        for i in range(200, 400):
            color = "#%02x%02x%02x" % (255 - i // 2, 255 - i // 4, 255 - i // 2)
            self.canvas.create_line(0, i, 400, i, fill=color)

    def draw_hand(self, angle, length, width, color):
        angle_rad = math.radians(angle)
        end_x = self.center_x + length * math.sin(angle_rad)
        end_y = self.center_y - length * math.cos(angle_rad)
        self.canvas.create_line(self.center_x, self.center_y, end_x, end_y, width=width, fill=color)

    def draw_clock_face(self):
        for i in range(12):
            angle = math.radians(i * 30)
            x = self.center_x + self.radius * 0.78 * math.sin(angle)  # Adjusted from 0.85 to 0.80
            y = self.center_y - self.radius * 0.78 * math.cos(angle)  # Adjusted from 0.85 to 0.80
            self.canvas.create_text(x, y, text=str(i if i != 0 else 12), font=("Arial", 12, "bold"))
        for i in range(60):
            angle = math.radians(i * 6)
            x = self.center_x + self.radius * 0.95 * math.sin(angle)
            y = self.center_y - self.radius * 0.95 * math.cos(angle)
            if i % 5 == 0:
                self.canvas.create_line(x, y, x - 10 * math.sin(angle), y + 10 * math.cos(angle), width=2)
            else:
                self.canvas.create_line(x, y, x - 5 * math.sin(angle), y + 5 * math.cos(angle), width=1)

    def update_clock(self):
        self.canvas.delete("all")
        self.draw_gradient_background()
        self.canvas.create_oval(self.center_x - self.radius - 10, self.center_y - self.radius - 10, 
                                self.center_x + self.radius + 10, self.center_y + self.radius + 10, width=2)
        self.canvas.create_oval(self.center_x - self.radius, self.center_y - self.radius, 
                                self.center_x + self.radius, self.center_y + self.radius, fill='white')
        self.draw_clock_face()
        
        current_time = time.localtime()
        hours = current_time.tm_hour % 12
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        hour_angle = (hours + minutes / 60) * 30
        minute_angle = (minutes + seconds / 60) * 6
        second_angle = seconds * 6

        self.draw_hand(hour_angle, self.radius * 0.5, 6, 'darkgreen')
        self.draw_hand(minute_angle, self.radius * 0.8, 4, 'darkblue')
        self.draw_hand(second_angle, self.radius * 0.9, 2, 'darkred')

        self.canvas.create_oval(self.center_x - 5, self.center_y - 5, self.center_x + 5, self.center_y + 5, fill='black')

        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    clock = AnalogClock(root)
    root.mainloop()
