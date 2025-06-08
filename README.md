**⛅ GetWeather: Check Weather on the Command Line 🌤️**

Command line weather tool that does the following ... 

- Connect to OpenWeatherMap.org via API.
- Download daily weather summary.
- Determine if you should pack an umbrella.
- Display output.

<pre>
prompt$ python GetWeather.py --zip 06905

🌤️   Fetching weather for your daily briefing ...

🌡️   Current Temp:	63.21°F

📅  Today (Jun 08)
🌡️  High Temp:		77.83°F
❄️  Low Temp:		61.18°F
💨  Feels Like:		63.46°F
☂️  Pack Umbrella:	No (4%)

</pre>


**📄 Usage: How to Use 🌦️**

Use flags to control how the script fetches and displays your forecast.
Supports multiple location types, temperature units, and forecast durations.

<pre>
⛅ GetWeather: A flexible CLI tool to check today’s weather. 🌤️

Usage:
  GetWeather.py [options]

🌍 Location Options:
  --zip <zipcode>             Fetch weather using ZIP code.
  --city <city> --state <st>  Use city and state combo.
                              Example: --city "Huntington Beach" --state CA

📆 Forecast Options:
  --days <1-10>               Number of forecast days to display. Default: 1.

🌡️ Units:
  --units <type>              Choose units: 'Imperial' (°F), 'Metric' (°C), or 'Standard' (Kelvin).
                              Default: Imperial

🛠️ Utilities:
  --version                   Show script version.
  --help                      Display this help message.

📌 Examples:
  GetWeather.py --zip 06905
  GetWeather.py --city "Huntington Beach" --state CA --units Metric --days 3

🌟 Pro Tips:
  • Use an .env file to set default ZIP or city/state.
  • 'Standard' returns temperatures in Kelvin — useful for labs.
  • Add this to a morning script or cronjob for daily forecasts.
  • If no data shows, check your API key and location details.
  • Pack an umbrella if it's going to rain. ☂️🌦️
</pre>

**🛠️ Requirements**

<pre>Python 3.x
requests
</pre>

**📦 Installation**
<pre>git clone https://github.com/your-username/GetWeather.git
cd GetWeather
pip install -r requirements.txt
cp GetWeather.env.template GetWeather.env
</pre>

**🧪 Environment Setup**
<pre>WEATHER_API_KEY=your_api_key_here
DEFAULT_ZIP=06905
DEFAULT_CITY=Stamford
DEFAULT_STATE=CT
</pre>
