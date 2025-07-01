import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIOw

API_KEY = "85b53730217373a534dc9947f2e99dd9"  # Replace with your OpenWeatherMap API Key

# Helper to fetch weather data
def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        print(f"[DEBUG] HTTP status: {response.status_code}")
        print(f"[DEBUG] Raw response: {response.text}")
        try:
            data = response.json()
            print(f"[DEBUG] API response for city '{city}': {data}")
        except Exception as json_err:
            print(f"[ERROR] Could not parse JSON: {json_err}")
            return None, f"Could not parse JSON: {json_err}\nRaw response: {response.text}"
        if response.status_code != 200 or data.get("cod") != 200:
            print(f"[ERROR] API error: {data.get('message', 'Unknown error')}")
            return None, f"API error: {data.get('message', 'Unknown error')}\nHTTP status: {response.status_code}\nRaw response: {response.text}"
        return data, None
    except Exception as e:
        print(f"[EXCEPTION] Exception occurred: {e}")
        return None, f"Exception occurred: {e}"

def get_icon_image(icon_code):
    try:
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        img_data = icon_response.content
        icon_img = Image.open(BytesIO(img_data))
        return ImageTk.PhotoImage(icon_img)
    except:
        return None

def update_weather():
    city = city_var.get()
    if not city:
        messagebox.showwarning("Input Required", "Please enter a city name.")
        return
    data, error = fetch_weather(city)
    if error:
        messagebox.showerror("Error", f"{error}\n(See terminal for details)")
        return
    # Main weather
    temp = f"{round(data['main']['temp'])}°C"
    desc = data['weather'][0]['description'].capitalize()
    humidity = f"{data['main']['humidity']}%"
    wind = f"{data['wind']['speed']} km/h"
    wind_dir = deg_to_compass(data['wind'].get('deg', 0))
    visibility = f"{data.get('visibility', 0) / 1000:.1f} km"
    city_name = f"{data['name']}, {data['sys'].get('country', '')}"
    # Rain
    rain = f"{data.get('rain', {}).get('1h', 0) * 100:.0f}%" if 'rain' in data else '0%'
    # Sunrise/Sunset
    from datetime import datetime
    sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p').lstrip('0')
    sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p').lstrip('0')
    # Icon
    icon_code = data['weather'][0]['icon']
    icon_img = get_icon_image(icon_code)
    if icon_img:
        weather_icon.config(image=icon_img)
        weather_icon.image = icon_img
    # Update left panel
    temp_label.config(text=temp)
    desc_label.config(text=desc)
    rain_label.config(text=f"Rain - {rain}")
    city_label.config(text=city_name)
    # Update right panel cards
    cards['Humidity'].config(text=humidity)
    cards['Wind Status'].config(text=f"{wind} {wind_dir}")
    cards['Visibility'].config(text=visibility)
    cards['Sunrise & Sunset'].config(text=f"{sunrise} / {sunset}")
    # Placeholders for unavailable data
    cards['UV Index'].config(text='N/A')
    cards['Air Quality'].config(text='N/A')

def deg_to_compass(num):
    val = int((num/22.5)+.5)
    arr = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
           'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    return arr[(val % 16)]

# --- UI Setup ---
root = tk.Tk()
root.title("SkyCast - Weather App")
root.state('zoomed')  # Full screen for Windows
root.configure(bg="#f3f4f8")
root.resizable(True, True)

# Left panel
left_frame = tk.Frame(root, bg="white", width=260, height=480)
left_frame.place(x=20, y=10)
left_frame.pack_propagate(False)

city_var = tk.StringVar()
city_entry = tk.Entry(left_frame, textvariable=city_var, font=("Segoe UI", 12), justify="center")
city_entry.pack(pady=(20, 10), padx=20, fill='x')
city_entry.insert(0, 'Enter city...')

search_button = tk.Button(left_frame, text="Get Weather", font=("Segoe UI", 12), bg="#00ffe7", fg="#1e1e2f", command=update_weather)
search_button.pack(pady=(0, 20), padx=20, fill='x')

weather_icon = tk.Label(left_frame, bg="white")
weather_icon.pack(pady=0)

temp_label = tk.Label(left_frame, text="--°C", font=("Segoe UI", 32, "bold"), bg="white")
temp_label.pack(pady=(10, 0))

desc_label = tk.Label(left_frame, text="--", font=("Segoe UI", 12), bg="white")
desc_label.pack()

rain_label = tk.Label(left_frame, text="Rain - --%", font=("Segoe UI", 10), fg="#888", bg="white")
rain_label.pack(pady=(0, 10))

city_label = tk.Label(left_frame, text="City, Country", font=("Segoe UI", 12, "bold"), bg="white")
city_label.pack(pady=(10, 0))

# Right panel
right_frame = tk.Frame(root, bg="#f3f4f8", width=480, height=480)
right_frame.place(x=300, y=10)

highlights_label = tk.Label(right_frame, text="Today's Highlights", font=("Segoe UI", 14, "bold"), bg="#f3f4f8")
highlights_label.pack(anchor='w', pady=(10, 0), padx=10)

cards_frame = tk.Frame(right_frame, bg="#f3f4f8")
cards_frame.pack(pady=10, padx=10, fill='both', expand=True)

for i in range(2):
    cards_frame.rowconfigure(i, weight=1)
for j in range(3):
    cards_frame.columnconfigure(j, weight=1)

cards = {}
card_data = [
    ('UV Index', '--'),
    ('Wind Status', '--'),
    ('Sunrise & Sunset', '--'),
    ('Humidity', '--'),
    ('Visibility', '--'),
    ('Air Quality', '--'),
]
card_border = '#d1d5db'
card_bg = 'white'

for i, (title, value) in enumerate(card_data):
    card = tk.Frame(cards_frame, bg=card_bg, highlightbackground=card_border, highlightthickness=1)
    card.grid(row=i//3, column=i%3, padx=18, pady=18, sticky='nsew')
    label = tk.Label(card, text=title, font=('Segoe UI', 11, 'bold'), bg=card_bg, fg="#2563eb")
    label.pack(anchor='nw', padx=10, pady=(12, 0))
    value_label = tk.Label(card, text=value, font=('Segoe UI', 20, 'bold'), bg=card_bg, fg="#222")
    value_label.pack(anchor='w', padx=10, pady=(4, 10))
    cards[title] = value_label

root.mainloop()
