from typing import Dict
import requests
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import threading

CURRENCY_CACHE = {
    'rates': {},
    'last_update': None
}

def get_live_rates() -> Dict[str, float]:
    if CURRENCY_CACHE['last_update'] and \
       datetime.now() - CURRENCY_CACHE['last_update'] < timedelta(hours=1):
        return CURRENCY_CACHE['rates']

    try:
        response = requests.get('https://open.er-api.com/v6/latest/USD', timeout=5)
        if response.status_code == 200:
            data = response.json()
            CURRENCY_CACHE['rates'] = data['rates']
            CURRENCY_CACHE['last_update'] = datetime.now()
            return CURRENCY_CACHE['rates']
        else:
            raise ConnectionError("Failed to fetch current rates")
    except Exception:
        return {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.73,
            'JPY': 110.0,
            'CAD': 1.25,
            'AUD': 1.35,
            'CHF': 0.92,
            'CNY': 6.45,
            'INR': 74.5,
            'VND': 23000.0
        }

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    rates = get_live_rates()
    
    if from_currency not in rates or to_currency not in rates:
        raise ValueError("Unsupported currency")
        
    usd_amount = amount / rates[from_currency]
    return usd_amount * rates[to_currency]

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    
    if from_unit == 'F':
        celsius = (value - 32) * 5/9
    elif from_unit == 'K':
        celsius = value - 273.15
    elif from_unit == 'C':
        celsius = value
    else:
        raise ValueError("Unsupported temperature unit")
    
    if to_unit == 'F':
        return (celsius * 9/5) + 32
    elif to_unit == 'K':
        return celsius + 273.15
    elif to_unit == 'C':
        return celsius
    else:
        raise ValueError("Unsupported temperature unit")

def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    conversions = {
        'kg': 1.0,
        'pounds': 0.453592,
        'ounces': 0.0283495,
        'grams': 0.001,
        'stones': 6.35029,
        'milligrams': 0.000001,
        'metric tons': 1000.0
    }
    
    if from_unit not in conversions or to_unit not in conversions:
        raise ValueError("Unsupported weight unit")
    
    kg = value * conversions[from_unit]
    return kg / conversions[to_unit]

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    conversions = {
        'meters': 1.0,
        'kilometers': 1000.0,
        'centimeters': 0.01,
        'millimeters': 0.001,
        'miles': 1609.34,
        'yards': 0.9144,
        'feet': 0.3048,
        'inches': 0.0254
    }
    
    if from_unit not in conversions or to_unit not in conversions:
        raise ValueError("Unsupported length unit")
    
    meters = value * conversions[from_unit]
    return meters / conversions[to_unit]

def convert_speed(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    conversions = {
        'm/s': 1.0,
        'km/h': 0.277778,
        'mph': 0.44704,
        'knots': 0.514444,
        'ft/s': 0.3048
    }
    
    if from_unit not in conversions or to_unit not in conversions:
        raise ValueError("Unsupported speed unit")
    
    ms = value * conversions[from_unit]
    return ms / conversions[to_unit]

def convert_volume(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    conversions = {
        'liters': 1.0,
        'milliliters': 0.001,
        'gallons': 3.78541,
        'quarts': 0.946353,
        'cups': 0.236588,
        'tablespoons': 0.0147868,
        'teaspoons': 0.00492892,
        'cubic meters': 1000.0
    }
    
    if from_unit not in conversions or to_unit not in conversions:
        raise ValueError("Unsupported volume unit")
    
    liters = value * conversions[from_unit]
    return liters / conversions[to_unit]

def convert_time(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    conversions = {
        'seconds': 1.0,
        'minutes': 60.0,
        'hours': 3600.0,
        'days': 86400.0,
        'weeks': 604800.0,
        'months': 2629746.0,
        'years': 31556952.0
    }
    
    if from_unit not in conversions or to_unit not in conversions:
        raise ValueError("Unsupported time unit")
    
    seconds = value * conversions[from_unit]
    return seconds / conversions[to_unit]

def convert_data(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    conversions = {
        'bytes': 1.0,
        'kilobytes': 1024.0,
        'megabytes': 1048576.0,
        'gigabytes': 1073741824.0,
        'terabytes': 1099511627776.0
    }
    
    if from_unit not in conversions or to_unit not in conversions:
        raise ValueError("Unsupported data unit")
    
    bytes_val = value * conversions[from_unit]
    return bytes_val / conversions[to_unit]

def convert_area(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    conversions = {
        'square meters': 1.0,
        'square kilometers': 1000000.0,
        'square feet': 0.092903,
        'square yards': 0.836127,
        'acres': 4046.86,
        'hectares': 10000.0,
        'square miles': 2589988.0
    }
    
    if from_unit not in conversions or to_unit not in conversions:
        raise ValueError("Unsupported area unit")
    
    sq_meters = value * conversions[from_unit]
    return sq_meters / conversions[to_unit]

class ModernConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Converter ✨")
        self.root.geometry("800x600")
        
        self.themes = {
            "Dark Ocean": {
                "bg": "#0a1628",
                "fg": "#e8f4f8",
                "accent": "#00d4ff",
                "card": "#0f2744",
                "button": "#0a4b78",
                "button_hover": "#0066cc",
                "success": "#00ff88",
                "gradient": [(10, 22, 40), (20, 60, 90)]
            },
            "Sunset": {
                "bg": "#1a0a1a",
                "fg": "#fff5f5",
                "accent": "#ff6b6b",
                "card": "#2d1515",
                "button": "#cc4444",
                "button_hover": "#ff6666",
                "success": "#ffd700",
                "gradient": [(26, 10, 26), (80, 30, 50)]
            },
            "Forest": {
                "bg": "#0a1a0a",
                "fg": "#f0fff0",
                "accent": "#00ff66",
                "card": "#0f2d0f",
                "button": "#0a6622",
                "button_hover": "#00cc44",
                "success": "#66ff66",
                "gradient": [(10, 26, 10), (30, 80, 40)]
            },
            "Purple Haze": {
                "bg": "#120a1a",
                "fg": "#f5e6ff",
                "accent": "#b366ff",
                "card": "#1f0f33",
                "button": "#6600cc",
                "button_hover": "#9933ff",
                "success": "#ff99ff",
                "gradient": [(18, 10, 26), (50, 30, 80)]
            }
        }
        self.current_theme = "Dark Ocean"
        
        self.history = []
        
        self.setup_ui()
        self.update_rates()
        
    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.draw_gradient()
        
        header_frame = tk.Frame(self.canvas, bg=self.get_theme("bg"))
        header_window = self.canvas.create_window(400, 30, window=header_frame)
        
        title_label = tk.Label(
            header_frame,
            text="✨ Universal Converter ✨",
            font=("Segoe UI", 24, "bold"),
            bg=self.get_theme("bg"),
            fg=self.get_theme("accent")
        )
        title_label.pack(side=tk.LEFT, padx=20)
        
        theme_combo = ttk.Combobox(
            header_frame,
            values=list(self.themes.keys()),
            state="readonly",
            width=15
        )
        theme_combo.set(self.current_theme)
        theme_combo.pack(side=tk.RIGHT, padx=20)
        theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        
        main_frame = tk.Frame(self.canvas, bg=self.get_theme("bg"))
        main_window = self.canvas.create_window(400, 330, window=main_frame)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        tabs = [
            ("Currency", "💱", self.setup_currency),
            ("Temperature", "🌡️", self.setup_temperature),
            ("Weight", "⚖️", self.setup_weight),
            ("Length", "📏", self.setup_length),
            ("Speed", "🏃", self.setup_speed),
            ("Volume", "🥛", self.setup_volume),
            ("Time", "⏰", self.setup_time),
            ("Data", "💾", self.setup_data),
            ("Area", "📐", self.setup_area)
        ]
        
        for name, icon, setup_func in tabs:
            frame = tk.Frame(notebook, bg=self.get_theme("bg"))
            notebook.add(frame, text=f"{icon} {name}")
            setup_func(frame)
        
        history_button = tk.Button(
            main_frame,
            text="📜 History",
            command=self.show_history,
            bg=self.get_theme("button"),
            fg=self.get_theme("fg"),
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5,
            cursor="hand2"
        )
        history_button.pack(pady=5)
        
        self.canvas.bind("<Configure>", self.on_resize)
    
    def get_theme(self, key):
        return self.themes[self.current_theme][key]
    
    def draw_gradient(self):
        self.canvas.delete("gradient")
        theme = self.themes[self.current_theme]
        start, end = theme["gradient"]
        height = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 600
        width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 800
        
        for i in range(height):
            r = int(start[0] + (end[0] - start[0]) * i / height)
            g = int(start[1] + (end[1] - start[1]) * i / height)
            b = int(start[2] + (end[2] - start[2]) * i / height)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_rectangle(0, i, width, i+1, fill=color, outline="", tags="gradient")
    
    def on_resize(self, event):
        self.draw_gradient()
    
    def change_theme(self, event):
        theme_name = event.widget.get()
        self.current_theme = theme_name
        self.draw_gradient()
        self.update_theme_colors()
    
    def update_theme_colors(self):
        for widget in self.root.winfo_children():
            self._update_widget_theme(widget)
    
    def _update_widget_theme(self, widget):
        try:
            if isinstance(widget, tk.Canvas):
                widget.config(bg=self.get_theme("bg"))
            elif isinstance(widget, tk.Frame):
                widget.config(bg=self.get_theme("bg"))
            elif isinstance(widget, tk.Label):
                widget.config(bg=self.get_theme("bg"), fg=self.get_theme("fg"))
            elif isinstance(widget, tk.Button):
                widget.config(bg=self.get_theme("button"), fg=self.get_theme("fg"))
            elif isinstance(widget, tk.Entry):
                widget.config(bg=self.get_theme("bg"), fg=self.get_theme("fg"), insertbackground=self.get_theme("accent"))
        except:
            pass
        
        for child in widget.winfo_children():
            self._update_widget_theme(child)
    
    def create_converter_frame(self, parent, title, units, convert_func, unit_map=None):
        frame = tk.Frame(parent, bg=self.get_theme("card"), relief="ridge", bd=2)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            bg=self.get_theme("card"),
            fg=self.get_theme("accent")
        )
        title_label.pack(pady=15)
        
        entry_frame = tk.Frame(frame, bg=self.get_theme("card"))
        entry_frame.pack(pady=10)
        
        tk.Label(entry_frame, text="Value:", bg=self.get_theme("card"), fg=self.get_theme("fg")).pack(side=tk.LEFT)
        entry = tk.Entry(entry_frame, width=20, font=("Segoe UI", 12))
        entry.pack(side=tk.LEFT, padx=10)
        
        units_frame = tk.Frame(frame, bg=self.get_theme("card"))
        units_frame.pack(pady=10)
        
        from_frame = tk.Frame(units_frame, bg=self.get_theme("card"))
        from_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(from_frame, text="From:", bg=self.get_theme("card"), fg=self.get_theme("fg")).pack()
        from_unit = ttk.Combobox(from_frame, values=units, width=15, state="readonly")
        from_unit.set(units[0])
        from_unit.pack()
        
        swap_btn = tk.Button(
            units_frame,
            text="⇄",
            command=lambda: self.swap_units(from_unit, to_unit),
            bg=self.get_theme("button"),
            fg=self.get_theme("fg"),
            font=("Segoe UI", 16, "bold"),
            relief="flat",
            width=3,
            cursor="hand2"
        )
        swap_btn.pack(side=tk.LEFT, padx=5)
        
        to_frame = tk.Frame(units_frame, bg=self.get_theme("card"))
        to_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(to_frame, text="To:", bg=self.get_theme("card"), fg=self.get_theme("fg")).pack()
        to_unit = ttk.Combobox(to_frame, values=units, width=15, state="readonly")
        to_unit.set(units[1] if len(units) > 1 else units[0])
        to_unit.pack()
        
        convert_btn = tk.Button(
            frame,
            text="🔄 Convert",
            bg=self.get_theme("button"),
            fg=self.get_theme("fg"),
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        convert_btn.pack(pady=15)
        
        result_label = tk.Label(
            frame,
            text="Result will appear here",
            font=("Segoe UI", 14, "bold"),
            bg=self.get_theme("card"),
            fg=self.get_theme("success")
        )
        result_label.pack(pady=15)
        
        copy_btn = tk.Button(
            frame,
            text="📋 Copy",
            command=lambda: self.copy_result(result_label),
            bg=self.get_theme("button"),
            fg=self.get_theme("fg"),
            font=("Segoe UI", 10),
            relief="flat",
            cursor="hand2"
        )
        copy_btn.pack(pady=5)
        
        def do_convert():
            try:
                value = float(entry.get())
                from_val = from_unit.get()
                to_val = to_unit.get()
                if unit_map:
                    from_val = unit_map.get(from_val, from_val)
                    to_val = unit_map.get(to_val, to_val)
                result = convert_func(value, from_val, to_val)
                result_text = f"{value} {from_unit.get()} = {result:.4f} {to_unit.get()}"
                result_label.config(text=result_text)
                self.add_to_history(result_text)
            except Exception as e:
                result_label.config(text=f"Error: {str(e)}", fg="#ff4444")
        
        entry.bind("<Return>", lambda e: do_convert())
        convert_btn.config(command=do_convert)
        
        return entry, from_unit, to_unit, result_label
    
    def swap_units(self, from_unit, to_unit):
        from_val = from_unit.get()
        to_val = to_unit.get()
        from_unit.set(to_val)
        to_unit.set(from_val)
    
    def copy_result(self, label):
        result = label.cget("text")
        if result and not result.startswith("Error"):
            text_to_copy = result.split(" = ")[1] if " = " in result else result
            self.root.clipboard_clear()
            self.root.clipboard_append(text_to_copy)
    
    def add_to_history(self, conversion):
        self.history.insert(0, f"{datetime.now().strftime('%H:%M:%S')} - {conversion}")
        if len(self.history) > 50:
            self.history.pop()
    
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Conversion History 📜")
        history_window.geometry("600x400")
        history_window.configure(bg=self.get_theme("bg"))
        
        text_widget = tk.Text(
            history_window,
            bg=self.get_theme("card"),
            fg=self.get_theme("fg"),
            font=("Consolas", 10),
            wrap="word"
        )
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if not self.history:
            text_widget.insert("1.0", "No conversion history yet.")
        else:
            for item in self.history:
                text_widget.insert("end", item + "\n")
        
        text_widget.config(state="disabled")
        
        clear_btn = tk.Button(
            history_window,
            text="🗑️ Clear History",
            command=lambda: self.clear_history(text_widget),
            bg=self.get_theme("button"),
            fg=self.get_theme("fg"),
            cursor="hand2"
        )
        clear_btn.pack(pady=5)
    
    def clear_history(self, text_widget):
        self.history.clear()
        text_widget.config(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", "History cleared.")
        text_widget.config(state="disabled")
    
    def setup_currency(self, parent):
        default_currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "VND"]
        self.currency_entry, self.from_currency, self.to_currency, self.currency_result = \
            self.create_converter_frame(
                parent,
                "💱 Currency Converter",
                default_currencies,
                convert_currency
            )
    
    def setup_temperature(self, parent):
        self.create_converter_frame(
            parent,
            "🌡️ Temperature Converter",
            ["Celsius", "Fahrenheit", "Kelvin"],
            convert_temperature,
            {"Celsius": "C", "Fahrenheit": "F", "Kelvin": "K"}
        )
    
    def setup_weight(self, parent):
        self.create_converter_frame(
            parent,
            "⚖️ Weight Converter",
            ["Kilograms", "Pounds", "Ounces", "Grams", "Stones", "Milligrams", "Metric Tons"],
            convert_weight
        )
    
    def setup_length(self, parent):
        self.create_converter_frame(
            parent,
            "📏 Length Converter",
            ["Meters", "Kilometers", "Centimeters", "Millimeters", "Miles", "Yards", "Feet", "Inches"],
            convert_length
        )
    
    def setup_speed(self, parent):
        self.create_converter_frame(
            parent,
            "🏃 Speed Converter",
            ["m/s", "km/h", "mph", "knots", "ft/s"],
            convert_speed
        )
    
    def setup_volume(self, parent):
        self.create_converter_frame(
            parent,
            "🥛 Volume Converter",
            ["Liters", "Milliliters", "Gallons", "Quarts", "Cups", "Tablespoons", "Teaspoons"],
            convert_volume
        )
    
    def setup_time(self, parent):
        self.create_converter_frame(
            parent,
            "⏰ Time Converter",
            ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"],
            convert_time
        )
    
    def setup_data(self, parent):
        self.create_converter_frame(
            parent,
            "💾 Data Converter",
            ["Bytes", "Kilobytes", "Megabytes", "Gigabytes", "Terabytes"],
            convert_data
        )
    
    def setup_area(self, parent):
        self.create_converter_frame(
            parent,
            "📐 Area Converter",
            ["Square Meters", "Square Kilometers", "Square Feet", "Square Yards", "Acres", "Hectares"],
            convert_area
        )
    
    def update_rates(self):
        def fetch():
            try:
                rates = get_live_rates()
                currencies = sorted(rates.keys())
                self.from_currency['values'] = currencies
                self.to_currency['values'] = currencies
                self.from_currency.set('USD')
                self.to_currency.set('EUR')
            except Exception:
                pass
        
        thread = threading.Thread(target=fetch)
        thread.start()

def main():
    root = tk.Tk()
    ModernConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()