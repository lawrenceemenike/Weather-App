import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")
        master.geometry("300x400")
        master.configure(bg='#f0f0f0')

        self.location_label = tk.Label(master, text="Location: Lagos, Nigeria", font=("Arial", 14), bg='#f0f0f0')
        self.location_label.pack(pady=10)

        self.temperature_label = tk.Label(master, text="", font=("Arial", 24, "bold"), bg='#f0f0f0')
        self.temperature_label.pack(pady=10)

        self.condition_label = tk.Label(master, text="", font=("Arial", 16), bg='#f0f0f0')
        self.condition_label.pack(pady=10)

        self.icon_label = tk.Label(master, bg='#f0f0f0')
        self.icon_label.pack(pady=10)

        self.umbrella_label = tk.Label(master, text="", font=("Arial", 14), bg='#f0f0f0', fg='#007acc')
        self.umbrella_label.pack(pady=10)

        self.update_button = tk.Button(master, text="Update Weather", command=self.update_weather, bg='#007acc', fg='white', font=("Arial", 12))
        self.update_button.pack(pady=20)

        self.update_weather()

    def update_weather(self):
        try:
            open_weather_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
            api_key = "83f0e1fbb92f655dd0170e27b3c1232c"

            weather_params = {
                "lat": 6.52437,
                "lon": 3.379206,
                "appid": api_key,
                "cnt": 4,
                "units": "metric"  # Use metric units for Celsius
            }

            response = requests.get(open_weather_endpoint, params=weather_params)
            response.raise_for_status()
            weather_data = response.json()

            current_temp = round(weather_data["list"][0]["main"]["temp"])
            condition = weather_data["list"][0]["weather"][0]["description"].capitalize()
            icon_code = weather_data["list"][0]["weather"][0]["icon"]

            self.temperature_label.config(text=f"{current_temp}°C")
            self.condition_label.config(text=condition)

            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            icon_data = icon_response.content
            icon_image = Image.open(io.BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.icon_label.config(image=icon_photo)
            self.icon_label.image = icon_photo

            will_rain = any(int(hour_data["weather"][0]['id']) < 700 for hour_data in weather_data["list"])
            
            if will_rain:
                self.umbrella_label.config(text="Bring an umbrella!")
            else:
                self.umbrella_label.config(text="No need for an umbrella.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()