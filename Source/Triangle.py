import tkinter as tk
from tkinter import ttk, font as tkfont

class TriangleGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Triangle Pattern Generator")
        self.root.geometry("800x700")
        self.root.configure(bg="#1E1E2E")
        
        self.setup_ui()
    
    def triangle_left(self, height, symbol):
        result = []
        for i in range(height):
            row = symbol * (i + 1)
            result.append(row)
        return "\n".join(result)
    
    def triangle_center(self, height, symbol):
        result = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            stars = symbol * (2 * i + 1)
            row = spaces + stars
            result.append(row)
        return "\n".join(result)
    
    def triangle_right(self, height, symbol):
        result = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            stars = symbol * (i + 1)
            row = spaces + stars
            result.append(row)
        return "\n".join(result)
    
    def inverted_triangle(self, height, symbol):
        result = []
        for i in range(height, 0, -1):
            spaces = " " * (height - i)
            stars = symbol * (2 * i - 1)
            row = spaces + stars
            result.append(row)
        return "\n".join(result)
    
    def pyramid(self, height, symbol):
        result = []
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = (symbol + " ") * i
            row = spaces + symbols
            result.append(row)
        return "\n".join(result)
    
    def diamond(self, height, symbol):
        result = []
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            stars = symbol * (2 * i - 1)
            row = spaces + stars
            result.append(row)
        for i in range(height, 0, -1):
            spaces = " " * (height - i)
            stars = symbol * (2 * i - 1)
            row = spaces + stars
            result.append(row)
        return "\n".join(result)
    
    def generate_pattern(self):
        pattern_type = self.pattern_var.get()
        height = self.height_scale.get()
        symbol = self.symbol_entry.get().strip()
        
        if not symbol:
            symbol = "*"
        elif len(symbol) > 1:
            symbol = symbol[0]
        
        if pattern_type == "Left-aligned Triangle":
            pattern = self.triangle_left(height, symbol)
        elif pattern_type == "Center-aligned Triangle":
            pattern = self.triangle_center(height, symbol)
        elif pattern_type == "Right-aligned Triangle":
            pattern = self.triangle_right(height, symbol)
        elif pattern_type == "Inverted Triangle":
            pattern = self.inverted_triangle(height, symbol)
        elif pattern_type == "Pyramid":
            pattern = self.pyramid(height, symbol)
        elif pattern_type == "Diamond":
            pattern = self.diamond(height, symbol)
        else:
            pattern = "Select a pattern type"
        
        self.display_pattern(pattern)
    
    def display_pattern(self, pattern):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, pattern)
    
    def copy_to_clipboard(self):
        pattern = self.output_text.get(1.0, tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(pattern)
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
    
    def setup_ui(self):
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        label_font = tkfont.Font(family="Helvetica", size=12)
        button_font = tkfont.Font(family="Helvetica", size=11)
        output_font = tkfont.Font(family="Courier New", size=14)
        
        header_frame = tk.Frame(self.root, bg="#2C3E50", padx=20, pady=20)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="Triangle Pattern Generator",
            font=title_font,
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Select a pattern and height to generate",
            font=label_font,
            bg="#2C3E50",
            fg="#BDC3C7"
        )
        subtitle_label.pack(pady=(10, 20))
        
        main_frame = tk.Frame(self.root, bg="#1E1E2E")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        left_frame = tk.Frame(main_frame, bg="#34495E", padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        section_label = tk.Label(
            left_frame,
            text="Pattern Type",
            font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
            bg="#34495E",
            fg="#ECF0F1"
        )
        section_label.pack(pady=(0, 15), anchor="w")
        
        canvas = tk.Canvas(left_frame, bg="#34495E", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        patterns_frame = tk.Frame(canvas, bg="#34495E")
        
        canvas.create_window((0, 0), window=patterns_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        patterns_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        patterns = [
            "Left-aligned Triangle",
            "Center-aligned Triangle",
            "Right-aligned Triangle",
            "Inverted Triangle",
            "Pyramid",
            "Diamond"
        ]
        
        self.pattern_var = tk.StringVar(value="Left-aligned Triangle")
        
        for pattern in patterns:
            rb = tk.Radiobutton(
                patterns_frame,
                text=pattern,
                variable=self.pattern_var,
                value=pattern,
                font=label_font,
                bg="#34495E",
                fg="white",
                selectcolor="#3498DB",
                activebackground="#2980B9",
                activeforeground="white",
                pady=8,
                anchor="w"
            )
            rb.pack(fill=tk.X, pady=5)
        
        symbol_label = tk.Label(
            patterns_frame,
            text="Display Symbol:",
            font=label_font,
            bg="#34495E",
            fg="#ECF0F1"
        )
        symbol_label.pack(pady=(20, 5), anchor="w")
        
        self.symbol_entry = tk.Entry(
            patterns_frame,
            font=label_font,
            bg="#2980B9",
            fg="white",
            insertbackground="#2980B9",
            relief="flat",
            width=15
        )
        self.symbol_entry.insert(0, "*")
        self.symbol_entry.pack(pady=5, fill=tk.X)
        
        height_label = tk.Label(
            patterns_frame,
            text="Pattern Height: 8",
            font=label_font,
            bg="#34495E",
            fg="#ECF0F1"
        )
        height_label.pack(pady=(20, 5), anchor="w")
        
        self.height_scale = tk.Scale(
            patterns_frame,
            from_=3,
            to=20,
            orient=tk.HORIZONTAL,
            length=200,
            font=label_font,
            bg="#34495E",
            fg="white",
            activebackground="#3498DB",
            highlightbackground="#34495E",
            troughcolor="#2980B9",
            command=lambda v: height_label.config(text=f"Pattern Height: {v}")
        )
        self.height_scale.set(8)
        self.height_scale.pack(pady=5, fill=tk.X)
        
        generate_button = tk.Button(
            patterns_frame,
            text="Generate Pattern",
            font=tkfont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#27AE60",
            fg="white",
            activebackground="#219653",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.generate_pattern,
            pady=12,
            padx=20
        )
        generate_button.pack(pady=(25, 10), fill=tk.X)
        
        right_frame = tk.Frame(main_frame, bg="#2D3748", padx=15, pady=15)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        output_header = tk.Frame(right_frame, bg="#1E1E2E")
        output_header.pack(fill=tk.X, pady=(0, 10))
        
        output_title_label = tk.Label(
            output_header,
            text="Output",
            font=tkfont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#1E1E2E",
            fg="#3498DB"
        )
        output_title_label.pack(side=tk.LEFT)
        
        button_frame = tk.Frame(output_header, bg="#1E1E2E")
        button_frame.pack(side=tk.RIGHT)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            font=button_font,
            bg="#E74C3C",
            fg="white",
            activebackground="#C0392B",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.clear_output,
            padx=10,
            pady=5
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        copy_btn = tk.Button(
            button_frame,
            text="Copy",
            font=button_font,
            bg="#3498DB",
            fg="white",
            activebackground="#2980B9",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.copy_to_clipboard,
            padx=10,
            pady=5
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        self.output_text = tk.Text(
            right_frame,
            font=output_font,
            bg="#1E1E2E",
            fg="#ECF0F1",
            wrap=tk.NONE,
            padx=15,
            pady=15,
            highlightthickness=0,
            width=40,
            height=15
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        initial_pattern = self.triangle_center(8, "*")
        self.display_pattern(initial_pattern)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TriangleGenerator()
    app.run()
