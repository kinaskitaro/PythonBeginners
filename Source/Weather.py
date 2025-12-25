import tkinter as tk
from tkinter import ttk, font as tkfont
import requests
import os
from datetime import datetime

class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Application")
        self.root.geometry("600x650")
        self.root.configure(bg="#1a1a2e")
        self.api_key = "c5b6d867d25225d52abdf0b9ce963b6c"
        self.search_history = []
        
        self.setup_ui()
    
    def setup_ui(self):
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        label_font = tkfont.Font(family="Helvetica", size=12)
        button_font = tkfont.Font(family="Helvetica", size=11)
        large_font = tkfont.Font(family="Helvetica", size=16)
        
        header_frame = tk.Frame(self.root, bg="#2980b9", padx=20, pady=20)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="Weather Application",
            font=title_font,
            bg="#2980b9",
            fg="#ffffff"
        )
        title_label.pack()
        
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        input_frame = tk.Frame(main_frame, bg="#ffffff", padx=20, pady=15)
        input_frame.pack(fill=tk.X)
        
        city_label = tk.Label(
            input_frame,
            text="City Name:",
            font=label_font,
            bg="#ffffff",
            fg="#1a1a2e"
        )
        city_label.pack(anchor="w", padx=(0, 10))
        
        self.city_entry = tk.Entry(
            input_frame,
            font=large_font,
            bg="#f5f5f5",
            fg="#1a1a2e",
            relief="flat",
            highlightthickness=2,
            highlightbackground="#00796b",
            highlightcolor="#00796b"
        )
        self.city_entry.pack(fill=tk.X, padx=(0, 10))
        
        unit_frame = tk.Frame(input_frame, bg="#ffffff")
        unit_frame.pack(fill=tk.X, pady=10)
        
        self.unit_var = tk.StringVar(value="Celsius")
        
        tk.Label(
            unit_frame,
            text="Unit:",
            font=label_font,
            bg="#ffffff",
            fg="#1a1a2e"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        celsius_rb = tk.Radiobutton(
            unit_frame,
            text="°C",
            variable=self.unit_var,
            value="Celsius",
            font=label_font,
            bg="#ffffff",
            fg="#1a1a2e",
            selectcolor="#00796b",
            activebackground="#e0f7fa"
        )
        celsius_rb.pack(side=tk.LEFT)
        
        fahrenheit_rb = tk.Radiobutton(
            unit_frame,
            text="°F",
            variable=self.unit_var,
            value="Fahrenheit",
            font=label_font,
            bg="#ffffff",
            fg="#1a1a2e",
            selectcolor="#00796b",
            activebackground="#e0f7fa"
        )
        fahrenheit_rb.pack(side=tk.LEFT, padx=(15, 0))
        
        button_frame = tk.Frame(input_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, pady=10)
        
        self.get_weather_btn = tk.Button(
            button_frame,
            text="Get Weather",
            font=tkfont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#00796b",
            fg="white",
            activebackground="#00669c",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.get_weather,
            padx=20,
            pady=8
        )
        self.get_weather_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="Clear",
            font=button_font,
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.clear_results,
            padx=15,
            pady=8
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        history_label = tk.Label(
            button_frame,
            text="History:",
            font=label_font,
            bg="#ffffff",
            fg="#95a5a6"
        )
        history_label.pack(side=tk.LEFT, padx=(15, 0))
        
        self.history_btn = ttk.Combobox(
            button_frame,
            width=20,
            state="readonly",
            values=[],
            font=label_font
        )
        self.history_btn.pack(side=tk.LEFT, padx=5)
        
        weather_frame = tk.Frame(main_frame, bg="#ffffff", padx=20, pady=15)
        weather_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(weather_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(weather_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_weather_card = tk.Frame(scrollable_frame, bg="#4facfe", padx=25, pady=20)
        main_weather_card.pack(fill=tk.X, pady=(0, 15))
        
        self.main_weather_inner = tk.Frame(main_weather_card, bg="#4facfe")
        self.main_weather_inner.pack(fill=tk.BOTH, expand=True)
        
        self.city_label = tk.Label(
            self.main_weather_inner,
            text="",
            font=tkfont.Font(family="Helvetica", size=22, weight="bold"),
            bg="#4facfe",
            fg="#ffffff"
        )
        self.city_label.pack(anchor="w")
        
        self.description_label = tk.Label(
            self.main_weather_inner,
            text="",
            font=tkfont.Font(family="Helvetica", size=14, weight="normal"),
            bg="#4facfe",
            fg="#e0f7fa"
        )
        self.description_label.pack(anchor="w", pady=(5, 0))
        
        self.temp_display = tk.Label(
            self.main_weather_inner,
            text="--",
            font=tkfont.Font(family="Helvetica", size=56, weight="bold"),
            bg="#4facfe",
            fg="#ffffff"
        )
        self.temp_display.pack(anchor="w", pady=(10, 0))
        
        self.weather_icon_label = tk.Label(
            self.main_weather_inner,
            text="",
            font=tkfont.Font(family="Segoe UI Emoji", size=50),
            bg="#4facfe",
            fg="#ffffff"
        )
        self.weather_icon_label.pack(side=tk.RIGHT)
        
        details_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", padx=15, pady=15)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        self.detail_labels = {}
        self.create_detail_cards(details_frame)
    
    def create_detail_cards(self, parent):
        card_colors = ["#e3f2fd", "#f3e5f5", "#e8f5e9", "#fff3e0", "#fce4ec", "#e0f2f1"]
        icons = ["🌡️", "🤗", "💧", "🌊", "💨", "☁️"]
        labels = ["Temperature", "Feels Like", "Humidity", "Pressure", "Wind", "Description"]
        
        for i, (label_text, icon, bg_color) in enumerate(zip(labels, icons, card_colors)):
            card = tk.Frame(parent, bg=bg_color, padx=15, pady=12)
            card.grid(row=i//3, column=i%3, sticky="nsew", padx=5, pady=5)
            parent.grid_columnconfigure(i%3, weight=1)
            
            icon_label = tk.Label(
                card,
                text=icon,
                font=tkfont.Font(family="Segoe UI Emoji", size=24),
                bg=bg_color
            )
            icon_label.pack(anchor="w")
            
            name_label = tk.Label(
                card,
                text=label_text,
                font=tkfont.Font(family="Helvetica", size=9, weight="bold"),
                bg=bg_color,
                fg="#616161"
            )
            name_label.pack(anchor="w")
            
            value_label = tk.Label(
                card,
                text="-",
                font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
                bg=bg_color,
                fg="#1a1a2e"
            )
            value_label.pack(anchor="w")
            self.detail_labels[label_text] = value_label
    
    def update_weather_icon(self, weather_condition):
        icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Smoke": "🌫️",
            "Haze": "🌫️",
            "Dust": "🌫️",
            "Fog": "🌫️",
            "Sand": "🌫️",
            "Ash": "🌫️",
            "Squall": "🌪️",
            "Tornado": "🌪️"
        }
        
        icon = icons.get(weather_condition, "")
        self.weather_icon_label.config(text=icon)
    
    def get_weather(self):
        city = self.city_entry.get().strip()
        
        if not city:
            self.show_error("Please enter a city name.")
            return
        
        if not self.api_key:
            self.show_error("API key not set. Set OPENWEATHER_API_KEY environment variable.")
            return
        
        self.set_loading_state(True)
        self.root.update_idletasks()
        
        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            unit = "metric" if self.unit_var.get() == "Celsius" else "imperial"
            complete_url = f"{base_url}q={city}&appid={self.api_key}&units={unit}"
            response = requests.get(complete_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("cod") != "404":
                    self.display_weather(data)
                    self.add_to_history(city)
                else:
                    self.show_error(f"City '{city}' not found.")
            else:
                self.show_error(f"Error fetching weather: {response.status_code}")
        except requests.exceptions.Timeout:
            self.show_error("Request timeout. Please try again.")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Network error: {str(e)}")
        except Exception as e:
            self.show_error(f"Unexpected error: {str(e)}")
        finally:
            self.set_loading_state(False)
    
    def display_weather(self, data):
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        city = data.get("name", "")
        
        temp_celsius = main.get("temp", 0)
        feels_like_celsius = main.get("feels_like", 0)
        humidity = main.get("humidity", 0)
        pressure = main.get("pressure", 0)
        wind_speed = data.get("wind", {}).get("speed", 0)
        description = weather.get("description", "").capitalize()
        weather_main = weather.get("main", "").capitalize()
        
        unit = self.unit_var.get()
        
        if unit == "Fahrenheit":
            temp = f"{round(temp_celsius * 9/5 + 32, 1)}°F"
            feels_like = f"{round(feels_like_celsius * 9/5 + 32, 1)}°F"
        else:
            temp = f"{round(temp_celsius, 1)}°C"
            feels_like = f"{round(feels_like_celsius, 1)}°C"
        
        self.city_label.config(text=city)
        self.description_label.config(text=description)
        self.temp_display.config(text=temp)
        self.update_weather_icon(weather_main)
        self.detail_labels["Temperature"].config(text=temp)
        self.detail_labels["Feels Like"].config(text=feels_like)
        self.detail_labels["Humidity"].config(text=f"{humidity}%")
        self.detail_labels["Pressure"].config(text=f"{pressure} hPa")
        self.detail_labels["Wind"].config(text=f"{wind_speed} m/s")
        self.detail_labels["Description"].config(text=description)
    
    def add_to_history(self, city):
        if city not in self.search_history:
            self.search_history.insert(0, city)
            self.history_btn['values'] = list(dict.fromkeys(self.search_history))[:10]
    
    def set_loading_state(self, loading):
        if loading:
            self.get_weather_btn.config(state="disabled", text="Loading...")
            self.city_entry.config(state="disabled")
        else:
            self.get_weather_btn.config(state="normal", text="Get Weather")
            self.city_entry.config(state="normal")
    
    def show_error(self, message):
        self.city_label.config(text=f"⚠️ Error", fg="#e74c3c")
        self.description_label.config(text=message, fg="#e74c3c")
        self.temp_display.config(text="--", fg="#e74c3c")
        self.weather_icon_label.config(text="⚠️")
        for label in self.detail_labels.values():
            label.config(text="")
    
    def clear_results(self):
        self.city_label.config(text="")
        self.description_label.config(text="")
        self.temp_display.config(text="--")
        self.weather_icon_label.config(text="")
        for label in self.detail_labels.values():
            label.config(text="")
        self.city_entry.delete(0, tk.END)
        self.city_entry.focus()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
