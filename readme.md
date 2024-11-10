# Weather Service
A comprehensive weather information service consisting of a Telegram bot and web application.

## Components

### 1. Weather Bot 🤖
A Telegram bot for getting weather information using the OpenWeather API.

#### Bot Features
- 🔍 City search through inline mode
- 🌡️ Current weather display (temperature, humidity, pressure, wind)
- 📊 5-day weather statistics download in JSON format
- 🌍 Worldwide city support

### 2. Web Application 🌐
A modern web interface for weather monitoring and forecasting.

#### Web App Features
- 📱 Responsive design for all devices
- 🗺️ Interactive weather map
- 📈 Detailed weather graphs and charts
- ⚡ Real-time weather updates
- 🎯 Location-based weather detection
- 📅 7-day weather forecast

## Installation

### Prerequisites
- Python 3.9+ (for bot)
- Node.js (for web app)
- Git

### Project Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/weather-service.git
cd weather-service
```

### Bot Setup
1. Navigate to bot directory:
```bash
cd bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file in the bot directory:
```env
BOT_TOKEN=your_telegram_bot_token
WEATHER_API_KEY=your_openweather_api_key
```

### Web Application Setup
1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

## Running Applications

### Start the Bot
```bash
cd bot
python bot.py
```

### Start the Web Application
```bash
cd frontend
npm run dev
```

The web application will be available at `http://localhost:5173`

## Bot Usage
1. Start the bot with `/start` command
2. Click "🔍 Search City" button
3. Enter city name (minimum 2 letters)
4. Select desired city from the list
5. Get current weather information
6. Use "📥 Download Statistics (JSON)" button to get detailed 5-day statistics

## Getting Required Tokens
1. Create a bot through [@BotFather](https://t.me/BotFather) and get the token
2. Get API key from [OpenWeather](https://openweathermap.org/api)

## License
MIT