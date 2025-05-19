# 🌤️ GetWeather CLI

GetWeather is a lightweight, emoji-powered command-line tool that fetches weather forecasts using the OpenWeatherMap API
https://openweathermap.org/api

### 🛠️ Features ###

- ✅ ZIP code and city/state-based forecast lookups
- 📅 Forecasts from 1–10 days (because we like options)
- ☂️ “Pack Umbrella?” forecast built-in
- 🌈 Emoji support for quick glances (optional toggle)
- 🧪 Clean, structured output perfect for terminals


### 🚀 Quick Start ###

git clone https://github.com/yourusername/GetWeather.git
cd GetWeather
pip install -r requirements.txt
cp GetWeather.env.template GetWeather.env

python GetWeather.py --zip 11211
python GetWeather.py --city "Los Angeles" --state CA --days 5
