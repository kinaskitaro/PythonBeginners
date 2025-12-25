import tkinter as tk
from tkinter import ttk
import math
import operator

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("500x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        self.current = "0"
        self.previous = ""
        self.operation = None
        self.new_num = True
        self.memory = 0
        self.history = []
        self.angle_mode = "DEG"
        
        self.create_display()
        self.create_buttons()
        self.create_history_panel()
        
        root.bind("<Key>", self.key_press)
    
    def create_display(self):
        display_frame = tk.Frame(self.root, bg="#2c3e50")
        display_frame.pack(pady=10, padx=10, fill="x")
        
        self.mode_label = tk.Label(
            display_frame, text=f"Mode: {self.angle_mode}",
            font=("Arial", 10), bg="#2c3e50", fg="#3498db"
        )
        self.mode_label.pack(anchor="w")
        
        self.history_label = tk.Label(
            display_frame, text="",
            font=("Arial", 12), bg="#2c3e50", fg="#95a5a6", anchor="e"
        )
        self.history_label.pack(fill="x")
        
        self.display = tk.Label(
            display_frame, text="0",
            font=("Arial", 28, "bold"), bg="#34495e", fg="#ecf0f1",
            relief="flat", anchor="e", padx=15, pady=20
        )
        self.display.pack(fill="x", ipady=10)
    
    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        buttons = [
            ("deg", 0, 0), ("rad", 0, 1), ("xʸ", 0, 2), ("n√", 0, 3),
            ("sin⁻¹", 1, 0), ("cos⁻¹", 1, 1), ("tan⁻¹", 1, 2), ("ln", 1, 3),
            ("sinh", 2, 0), ("cosh", 2, 1), ("tanh", 2, 2), ("log₂", 2, 3),
            ("n!", 3, 0), ("1/x", 3, 1), ("|x|", 3, 2), ("⌊x⌋", 3, 3),
            ("C", 4, 0), ("±", 4, 1), ("%", 4, 2), ("÷", 4, 3),
            ("7", 5, 0), ("8", 5, 1), ("9", 5, 2), ("×", 5, 3),
            ("4", 6, 0), ("5", 6, 1), ("6", 6, 2), ("−", 6, 3),
            ("1", 7, 0), ("2", 7, 1), ("3", 7, 2), ("+", 7, 3),
            ("0", 8, 0), (".", 8, 1), ("⌫", 8, 2), ("=", 8, 3),
        ]
        
        for text, row, col in buttons:
            color = self.get_button_color(text)
            btn = tk.Button(
                button_frame, text=text, font=("Arial", 12, "bold"),
                bg=color, fg="white" if text in ["÷", "×", "−", "+", "="] else "#2c3e50",
                relief="flat", padx=5, pady=8,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        
        for i in range(9):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        
        constants_frame = tk.Frame(self.root, bg="#2c3e50")
        constants_frame.pack(pady=5, padx=10, fill="x")
        
        constant_buttons = ["π", "e", "φ", "eˣ", "10ˣ"]
        for text in constant_buttons:
            btn = tk.Button(
                constants_frame, text=text, font=("Arial", 11, "bold"),
                bg="#95a5a6", fg="#2c3e50", relief="flat",
                command=lambda t=text: self.on_constant_click(t)
            )
            btn.pack(side="left", expand=True, fill="x", padx=1)
        
        memory_frame = tk.Frame(self.root, bg="#2c3e50")
        memory_frame.pack(pady=5, padx=10, fill="x")
        
        memory_buttons = ["MC", "MR", "M+", "M−"]
        for text in memory_buttons:
            btn = tk.Button(
                memory_frame, text=text, font=("Arial", 10, "bold"),
                bg="#7f8c8d", fg="white", relief="flat",
                command=lambda t=text: self.on_memory_click(t)
            )
            btn.pack(side="left", expand=True, fill="x", padx=1)
    
    def create_history_panel(self):
        self.history_window = tk.Toplevel(self.root)
        self.history_window.title("History")
        self.history_window.geometry("300x400")
        self.history_window.configure(bg="#ecf0f1")
        
        tk.Label(
            self.history_window, text="Calculation History",
            font=("Arial", 14, "bold"), bg="#ecf0f1"
        ).pack(pady=10)
        
        self.history_list = tk.Listbox(
            self.history_window, font=("Arial", 11), bg="white",
            height=20, width=40
        )
        self.history_list.pack(pady=10, padx=10, fill="both", expand=True)
        
        clear_btn = tk.Button(
            self.history_window, text="Clear History",
            font=("Arial", 10), bg="#e74c3c", fg="white",
            command=self.clear_history
        )
        clear_btn.pack(pady=5)
        
        self.history_window.withdraw()
        
        history_toggle = tk.Button(
            self.root, text="📋 History", font=("Arial", 10),
            bg="#3498db", fg="white", relief="flat",
            command=self.toggle_history
        )
        history_toggle.place(x=5, y=5)
    
    def get_button_color(self, text):
        if text in ["÷", "×", "−", "+", "xʸ"]:
            return "#e67e22"
        elif text == "=":
            return "#27ae60"
        elif text == "C":
            return "#c0392b"
        elif text in ["deg", "rad"]:
            return "#8e44ad"
        elif text in ["π", "e", "φ"]:
            return "#16a085"
        else:
            return "#ecf0f1"
    
    def get_angle_factor(self):
        return 1 if self.angle_mode == "RAD" else math.pi / 180
    
    def to_degrees(self, value):
        return value if self.angle_mode == "RAD" else math.degrees(value)
    
    def to_radians(self, value):
        return value if self.angle_mode == "RAD" else math.radians(value)
    
    def on_button_click(self, text):
        if text.isdigit():
            self.append_number(text)
        elif text == ".":
            self.append_decimal()
        elif text in ["÷", "×", "−", "+", "xʸ"]:
            self.set_operation(text)
        elif text == "=":
            self.calculate()
        elif text == "C":
            self.clear_all()
        elif text == "±":
            self.toggle_sign()
        elif text == "%":
            self.percentage()
        elif text == "⌫":
            self.backspace()
        elif text == "deg":
            self.angle_mode = "DEG"
            self.mode_label.config(text="Mode: DEG")
        elif text == "rad":
            self.angle_mode = "RAD"
            self.mode_label.config(text="Mode: RAD")
        elif text == "n√":
            self.nth_root()
        else:
            self.on_scientific_click(text)
    
    def on_scientific_click(self, text):
        try:
            num = float(self.current)
            result = num
            
            if text == "n!":
                if num < 0 or num != int(num):
                    self.show_error("Invalid input")
                    return
                result = math.factorial(int(num))
            elif text == "sin⁻¹":
                if abs(num) > 1:
                    self.show_error("Domain error")
                    return
                result = self.to_degrees(math.asin(num))
            elif text == "cos⁻¹":
                if abs(num) > 1:
                    self.show_error("Domain error")
                    return
                result = self.to_degrees(math.acos(num))
            elif text == "tan⁻¹":
                result = self.to_degrees(math.atan(num))
            elif text == "sinh":
                result = math.sinh(num)
            elif text == "cosh":
                result = math.cosh(num)
            elif text == "tanh":
                result = math.tanh(num)
            elif text == "ln":
                if num <= 0:
                    self.show_error("Invalid input")
                    return
                result = math.log(num)
            elif text == "log₂":
                if num <= 0:
                    self.show_error("Invalid input")
                    return
                result = math.log2(num)
            elif text == "1/x":
                if num == 0:
                    self.show_error("Cannot divide by zero")
                    return
                result = 1 / num
            elif text == "|x|":
                result = abs(num)
            elif text == "⌊x⌋":
                result = math.floor(num)
            
            expression = f"{text}({num})"
            self.history_label.config(text=expression)
            self.current = str(round(result, 10))
            self.update_display()
            self.new_num = True
        except:
            self.show_error("Error")
    
    def on_constant_click(self, text):
        try:
            num = float(self.current) if self.current != "0" else 0
            result = num
            
            if text == "π":
                result = math.pi
            elif text == "e":
                result = math.e
            elif text == "φ":
                result = (1 + math.sqrt(5)) / 2
            elif text == "eˣ":
                result = math.e ** num
            elif text == "10ˣ":
                result = 10 ** num
            
            expression = f"{text}" if text in ["π", "e", "φ"] else f"{text}({num})"
            self.history_label.config(text=expression)
            self.current = str(round(result, 10))
            self.update_display()
            self.new_num = True
        except:
            self.show_error("Error")
    
    def nth_root(self):
        self.set_operation("n√")
    
    def calculate(self):
        if not self.operation:
            return
        
        try:
            num1 = float(self.previous)
            num2 = float(self.current)
            
            if self.operation == "xʸ":
                result = num1 ** num2
            elif self.operation == "n√":
                if num1 == 0:
                    self.show_error("Invalid input")
                    return
                if num2 == 0:
                    self.show_error("Cannot take 0th root")
                    return
                if num1 < 0 and abs(num2 % 2) < 1e-10:
                    self.show_error("Invalid input")
                    return
                result = num1 ** (1 / num2)
            else:
                ops = {
                    "÷": operator.truediv,
                    "×": operator.mul,
                    "−": operator.sub,
                    "+": operator.add,
                }
                
                if self.operation == "÷" and num2 == 0:
                    self.show_error("Cannot divide by zero")
                    return
                
                result = ops[self.operation](num1, num2)
            
            expression = f"{num1} {self.operation} {num2} = {result}"
            self.history.append(expression)
            self.history_list.insert(0, expression)
            
            self.history_label.config(text=f"{self.previous} {self.operation} {self.current} =")
            self.current = str(round(result, 10))
            self.operation = None
            self.new_num = True
            self.update_display()
        except:
            self.show_error("Error")
    
    def on_memory_click(self, text):
        try:
            num = float(self.current)
            
            if text == "MC":
                self.memory = 0
            elif text == "MR":
                self.current = str(self.memory)
                self.update_display()
            elif text == "M+":
                self.memory += num
            elif text == "M−":
                self.memory -= num
        except:
            pass
    
    def append_number(self, num):
        if self.new_num:
            self.current = num
            self.new_num = False
        else:
            self.current += num
        self.update_display()
    
    def append_decimal(self):
        if self.new_num:
            self.current = "0."
            self.new_num = False
        elif "." not in self.current:
            self.current += "."
        self.update_display()
    
    def set_operation(self, op):
        if self.operation and not self.new_num:
            self.calculate()
        self.previous = self.current
        self.operation = op
        self.new_num = True
        self.history_label.config(text=f"{self.previous} {op}")
    
    def clear_all(self):
        self.current = "0"
        self.previous = ""
        self.operation = None
        self.new_num = True
        self.update_display()
        self.history_label.config(text="")
    
    def toggle_sign(self):
        try:
            num = float(self.current)
            self.current = str(-num)
            self.update_display()
        except:
            pass
    
    def percentage(self):
        try:
            num = float(self.current)
            self.current = str(num / 100)
            self.update_display()
        except:
            pass
    
    def backspace(self):
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.update_display()
    
    def update_display(self):
        try:
            if float(self.current) == int(float(self.current)):
                self.display.config(text=str(int(float(self.current))))
            else:
                self.display.config(text=self.current)
        except:
            self.display.config(text=self.current)
    
    def show_error(self, message):
        self.display.config(text=message)
        self.current = "0"
        self.new_num = True
    
    def toggle_history(self):
        if self.history_window.state() == "withdrawn":
            self.history_window.deiconify()
        else:
            self.history_window.withdraw()
    
    def clear_history(self):
        self.history.clear()
        self.history_list.delete(0, tk.END)
    
    def key_press(self, event):
        key = event.char
        if key.isdigit():
            self.append_number(key)
        elif key == ".":
            self.append_decimal()
        elif key == "+":
            self.set_operation("+")
        elif key == "-":
            self.set_operation("−")
        elif key == "*":
            self.set_operation("×")
        elif key == "/":
            self.set_operation("÷")
        elif key == "^":
            self.set_operation("xʸ")
        elif key == "\r":
            self.calculate()
        elif event.keysym == "Escape":
            self.clear_all()
        elif event.keysym == "BackSpace":
            self.backspace()

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
