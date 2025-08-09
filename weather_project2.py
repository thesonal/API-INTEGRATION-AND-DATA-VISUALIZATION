import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# --- Setup ---
API_KEY = "7b747e2f7c8feafface47df1b2da7a6a"  # 🔑 Replace with your actual OpenWeatherMap API key
CITY = "Ulhasnagar"
UNITS = "metric"

# --- Fetch Forecast Data ---
url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units={UNITS}"
response = requests.get(url)
data = response.json()
if response.status_code != 200:
    print("Error fetching data:", data.get("message"))
    exit()

# --- Parse Forecast Data ---
timestamps, temps, humidity, conditions = [], [], [], []
for entry in data['list']:
    dt = datetime.fromtimestamp(entry['dt'])
    timestamps.append(dt.strftime('%d %b %H:%M'))
    temps.append(entry['main']['temp'])
    humidity.append(entry['main']['humidity'])
    conditions.append(entry['weather'][0]['main'])

# --- Extract Current Weather Info ---
current_temp = temps[0]
current_humidity = humidity[0]
wind_speed = data['list'][0]['wind']['speed']
weather_condition = conditions[0]

# --- Suggestion Based on Condition ---
def get_suggestion(condition):
    suggestions = {
        'Clear': "☀️ Time to soak up the sun — go out!",
        'Rain': "🌧️ Perfect weather for chai and coding indoors.",
        'Clouds': "☁️ Great for a cozy read or quiet focus.",
        'Mist': "🌫️ Calm and introspective vibes — maybe some journaling?",
        'Snow': "❄️ Stay warm — blanket, snacks, and movies!",
        'Thunderstorm': "⛈️ Unplug and relax — safety first!"
    }
    return suggestions.get(condition, f"Weather looks {condition.lower()} — stay flexible!")

print(f"\nWeather Now in {CITY}: {weather_condition}, {current_temp}°C")
print(f"Suggestion: {get_suggestion(weather_condition)}\n")

# --- Prepare DataFrames ---
forecast_df = pd.DataFrame({
    'Time': timestamps,
    'Temperature (°C)': temps,
    'Humidity (%)': humidity
})

bar_df = pd.DataFrame({
    'Metric': ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)'],
    'Value': [current_temp, current_humidity, wind_speed]
})

# --- Create Save Directory ---
save_dir = "Weather_Charts"
os.makedirs(save_dir, exist_ok=True)

# --- Plot Dual-Axis Forecast Chart ---
fig, ax1 = plt.subplots(figsize=(10, 5))  # Initialize subplot and first axis
ax1.plot(forecast_df['Time'], forecast_df['Temperature (°C)'], color='red', marker='o', label='Temperature')
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature (°C)", color='red')
ax1.tick_params(axis='y', labelcolor='red')
ax1.set_xticks(forecast_df['Time'][::8])
ax1.tick_params(axis='x', rotation=45)

ax2 = ax1.twinx()  # Create second axis sharing the same x-axis
ax2.plot(forecast_df['Time'], forecast_df['Humidity (%)'], color='blue', marker='x', label='Humidity')
ax2.set_ylabel("Humidity (%)", color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

plt.title(f"5-Day Temperature & Humidity Forecast for {CITY}")
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "forecast_dual_axis_chart.png"), dpi=300)
plt.show()

# --- Create DataFrame for Bar Chart ---
bar_df = pd.DataFrame({
    'Metric': ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)'],
    'Value': [current_temp, current_humidity, wind_speed]
})

# --- Plot Bar Chart ---
plt.figure(figsize=(6, 5))
plt.title(f"Current Weather Stats for {CITY}")
plt.bar(bar_df['Metric'], bar_df['Value'], color=['tomato', 'royalblue', 'green'])
plt.ylabel("Value")
plt.tight_layout()

# --- Save and Show ---
plt.savefig(os.path.join(save_dir, "current_weather_bar_chart.png"), dpi=300)
plt.show()