import tkinter as tk
import requests

# Add your OpenWeatherMap API key directly
api_key = "c5b6d867d25225d52abdf0b9ce963b6c"  # Replace with your actual API key

def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}"
    response = requests.get(complete_url)
    return response.json()

def show_weather():
    city = city_entry.get()
    weather_data = get_weather(city, api_key)
    if weather_data.get("cod") != "404":
        main = weather_data.get("main", {})
        temperature = main.get("temp", "N/A")
        if temperature != "N/A":
            temperature = round(temperature - 273.15, 2)  # Convert from Kelvin to Celsius
        pressure = main.get("pressure", "N/A")
        humidity = main.get("humidity", "N/A")
        weather_desc = weather_data.get("weather", [{}])[0].get("description", "N/A")
        weather_info = f"Temperature: {temperature}°C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nDescription: {weather_desc}"
    else:
        error_message = weather_data.get("message", "City Not Found!")
        weather_info = f"Error: {error_message}"
    weather_label.config(text=weather_info)
    expand_weather_info()

def expand_weather_info():
    weather_label.pack(side="left", pady=20)
    weather_label.after(10, lambda: weather_label.config(height=weather_label.winfo_height() + 1))
    if weather_label.winfo_height() < get_weather_button.winfo_y() - weather_label.winfo_y() - 20:
        weather_label.after(10, expand_weather_info)
    else:
        weather_label.after(3000, collapse_weather_info)  # Auto-collapse after 3 seconds

def collapse_weather_info():
    if weather_label.winfo_height() > 0:
        weather_label.config(height=weather_label.winfo_height() - 1)
        weather_label.after(10, collapse_weather_info)
    else:
        weather_label.pack_forget()

# Create the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.configure(bg="#e0f7fa")

# Create and place the widgets
city_label = tk.Label(root, text="Enter city name:", bg="#e0f7fa", font=("Helvetica", 14, "bold"))
city_label.pack(pady=20)

city_entry = tk.Entry(root, font=("Helvetica", 14))
city_entry.pack(pady=10)

get_weather_button = tk.Button(root, text="Get Weather", command=show_weather, bg="#00796b", fg="white", font=("Helvetica", 14, "bold"))
get_weather_button.pack(pady=20)

weather_label = tk.Label(root, text="", justify="left", bg="#e0f7fa", font=("Helvetica", 14), height=0)
weather_label.pack_forget()

# Run the application
root.mainloop()
