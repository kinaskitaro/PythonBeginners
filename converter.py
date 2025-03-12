from typing import Dict
import requests
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading

# Cache for currency rates
CURRENCY_CACHE = {
    'rates': {},
    'last_update': None
}

def get_live_rates() -> Dict[str, float]:
    """Fetch live currency rates from API"""
    if CURRENCY_CACHE['last_update'] and \
       datetime.now() - CURRENCY_CACHE['last_update'] < timedelta(hours=1):
        return CURRENCY_CACHE['rates']

    try:
        # Using exchangerate-api.com (free tier)
        response = requests.get('https://open.er-api.com/v6/latest/USD')
        if response.status_code == 200:
            data = response.json()
            CURRENCY_CACHE['rates'] = data['rates']
            CURRENCY_CACHE['last_update'] = datetime.now()
            return CURRENCY_CACHE['rates']
        else:
            raise ConnectionError("Failed to fetch current rates")
    except Exception as e:
        # Fallback to default rates if API fails
        return {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.73,
            'JPY': 110.0,
            'CAD': 1.25
        }

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert between currencies using live rates"""
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    rates = get_live_rates()
    
    if from_currency not in rates or to_currency not in rates:
        raise ValueError("Unsupported currency")
        
    # Convert to USD first
    usd_amount = amount / rates[from_currency]
    # Convert from USD to target currency
    return usd_amount * rates[to_currency]

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between Celsius, Fahrenheit, and Kelvin"""
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    
    # Convert to Celsius first
    if from_unit == 'F':
        celsius = (value - 32) * 5/9
    elif from_unit == 'K':
        celsius = value - 273.15
    elif from_unit == 'C':
        celsius = value
    else:
        raise ValueError("Unsupported temperature unit")
    
    # Convert from Celsius to target unit
    if to_unit == 'F':
        return (celsius * 9/5) + 32
    elif to_unit == 'K':
        return celsius + 273.15
    elif to_unit == 'C':
        return celsius
    else:
        raise ValueError("Unsupported temperature unit")

class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Converter")
        self.root.geometry("600x500")
        
        # Color scheme
        self.colors = {
            'bg': '#2C3E50',
            'fg': '#ECF0F1',
            'accent': '#3498DB',
            'button': '#2980B9',
            'button_hover': '#3498DB',
            'error': '#E74C3C',
            'success': '#2ECC71'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure common styles
        style.configure('Main.TFrame', background=self.colors['bg'])
        style.configure('Tab.TFrame', background=self.colors['bg'])
        style.configure('Main.TLabel', 
                       background=self.colors['bg'], 
                       foreground=self.colors['fg'],
                       font=('Helvetica', 10))
        style.configure('Result.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['success'],
                       font=('Helvetica', 12, 'bold'))
        style.configure('Main.TButton',
                       background=self.colors['button'],
                       foreground=self.colors['fg'],
                       padding=10,
                       font=('Helvetica', 10, 'bold'))
        style.configure('Main.TEntry',
                       fieldbackground=self.colors['fg'],
                       foreground=self.colors['bg'])
        
        # Configure notebook style
        style.configure('Main.TNotebook',
                       background=self.colors['bg'],
                       foreground=self.colors['fg'])
        style.configure('Main.TNotebook.Tab',
                       background=self.colors['button'],
                       foreground=self.colors['fg'],
                       padding=[10, 5])
        style.map('Main.TNotebook.Tab',
                 background=[('selected', self.colors['accent'])])
        
        # Create notebook with custom style
        self.notebook = ttk.Notebook(root, style='Main.TNotebook')
        self.notebook.pack(pady=10, expand=True, fill="both")
        
        # Create frames for tabs
        self.currency_frame = ttk.Frame(self.notebook, style='Tab.TFrame')
        self.temp_frame = ttk.Frame(self.notebook, style='Tab.TFrame')
        
        # Add frames to notebook
        self.notebook.add(self.currency_frame, text="Currency Converter")
        self.notebook.add(self.temp_frame, text="Temperature Converter")
        
        # Setup tabs
        self.setup_currency_tab()
        self.setup_temperature_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initial rate fetch
        self.update_rates()

    def setup_currency_tab(self):
        # Title label
        title_label = ttk.Label(self.currency_frame, 
                               text="Currency Converter",
                               style='Main.TLabel',
                               font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Amount entry with custom style
        amount_frame = ttk.Frame(self.currency_frame, style='Tab.TFrame')
        amount_frame.pack(pady=20)
        ttk.Label(amount_frame, text="Amount:", style='Main.TLabel').pack(side=tk.LEFT)
        self.amount_entry = ttk.Entry(amount_frame, width=20, style='Main.TEntry')
        self.amount_entry.pack(side=tk.LEFT, padx=10)
        
        # Currency selection
        selections_frame = ttk.Frame(self.currency_frame, style='Tab.TFrame')
        selections_frame.pack(pady=10)
        
        # From currency
        from_frame = ttk.Frame(selections_frame, style='Tab.TFrame')
        from_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(from_frame, text="From:", style='Main.TLabel').pack()
        self.from_currency = ttk.Combobox(from_frame, width=10, style='Main.TCombobox')
        self.from_currency.pack()
        
        # To currency
        to_frame = ttk.Frame(selections_frame, style='Tab.TFrame')
        to_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(to_frame, text="To:", style='Main.TLabel').pack()
        self.to_currency = ttk.Combobox(to_frame, width=10, style='Main.TCombobox')
        self.to_currency.pack()
        
        # Convert button
        ttk.Button(self.currency_frame, text="Convert", command=self.convert_currency_gui, style='Main.TButton').pack(pady=20)
        
        # Result label with custom style
        self.currency_result = ttk.Label(self.currency_frame, 
                                       style='Result.TLabel',
                                       font=('Helvetica', 14, 'bold'))
        self.currency_result.pack(pady=10)

    def setup_temperature_tab(self):
        # Title label
        title_label = ttk.Label(self.temp_frame, 
                               text="Temperature Converter",
                               style='Main.TLabel',
                               font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Temperature entry with custom style
        temp_frame = ttk.Frame(self.temp_frame, style='Tab.TFrame')
        temp_frame.pack(pady=20)
        ttk.Label(temp_frame, text="Temperature:", style='Main.TLabel').pack(side=tk.LEFT)
        self.temp_entry = ttk.Entry(temp_frame, width=20, style='Main.TEntry')
        self.temp_entry.pack(side=tk.LEFT, padx=10)
        
        # Unit selection
        units_frame = ttk.Frame(self.temp_frame, style='Tab.TFrame')
        units_frame.pack(pady=10)
        
        # From unit
        self.from_unit = ttk.Combobox(units_frame, values=['Celsius', 'Fahrenheit', 'Kelvin'], width=10, style='Main.TCombobox')
        self.from_unit.set('Celsius')
        self.from_unit.pack(side=tk.LEFT, padx=10)
        
        # To unit
        self.to_unit = ttk.Combobox(units_frame, values=['Celsius', 'Fahrenheit', 'Kelvin'], width=10, style='Main.TCombobox')
        self.to_unit.set('Fahrenheit')
        self.to_unit.pack(side=tk.LEFT, padx=10)
        
        # Convert button
        ttk.Button(self.temp_frame, text="Convert", command=self.convert_temperature_gui, style='Main.TButton').pack(pady=20)
        
        # Result label with custom style
        self.temp_result = ttk.Label(self.temp_frame, 
                                    style='Result.TLabel',
                                    font=('Helvetica', 14, 'bold'))
        self.temp_result.pack(pady=10)

    def update_rates(self):
        def fetch():
            try:
                rates = get_live_rates()
                currencies = sorted(rates.keys())
                self.from_currency['values'] = currencies
                self.to_currency['values'] = currencies
                self.from_currency.set('USD')
                self.to_currency.set('EUR')
                self.status_var.set(f"Rates updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            except Exception as e:
                self.status_var.set("Error updating rates. Using fallback values.")
        
        thread = threading.Thread(target=fetch)
        thread.start()

    def convert_currency_gui(self):
        try:
            amount = float(self.amount_entry.get())
            result = convert_currency(amount, self.from_currency.get(), self.to_currency.get())
            self.currency_result.config(text=f"{amount:.2f} {self.from_currency.get()} = {result:.2f} {self.to_currency.get()}", foreground=self.colors['success'])
        except Exception as e:
            self.currency_result.config(foreground=self.colors['error'])
            messagebox.showerror("Error", str(e))

    def convert_temperature_gui(self):
        try:
            value = float(self.temp_entry.get())
            from_unit = self.from_unit.get()[0]  # Get first letter (C/F/K)
            to_unit = self.to_unit.get()[0]
            result = convert_temperature(value, from_unit, to_unit)
            self.temp_result.config(text=f"{value}°{from_unit} = {result:.2f}°{to_unit}", foreground=self.colors['success'])
        except Exception as e:
            self.temp_result.config(foreground=self.colors['error'])
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
