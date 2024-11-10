# services/weather_api.py
import aiohttp
import json
from datetime import datetime, timedelta

class WeatherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
    
    async def search_cities(self, query: str) -> list:
        params = {
            "q": query,
            "limit": 5,
            "appid": self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.geocoding_url, params=params) as response:
                if response.status == 200:
                    cities = await response.json()
                    return [
                        {
                            "name": city["name"],
                            "country": city.get("country", ""),
                            "state": city.get("state", ""),
                            "lat": city["lat"],
                            "lon": city["lon"]
                        }
                        for city in cities
                    ]
                return []

    async def get_weather(self, lat: float, lon: float, city_name: str) -> dict:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": "ru"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    weather_data = await response.json()
                    return {
                        "city": city_name,
                        "temperature": weather_data["main"]["temp"],
                        "feels_like": weather_data["main"]["feels_like"],
                        "description": weather_data["weather"][0]["description"],
                        "humidity": weather_data["main"]["humidity"],
                        "pressure": weather_data["main"]["pressure"],
                        "wind_speed": weather_data["wind"]["speed"],
                        "icon": weather_data["weather"][0]["icon"],
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    raise Exception(f"Error getting weather: {weather_data['message']}")

    async def get_weekly_stats(self, lat: float, lon: float, city_name: str) -> dict:
        """Получение статистики погоды за последние 5 дней (максимум бесплатного API)"""
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": "ru"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.forecast_url, params=params) as response:
                if response.status == 200:
                    forecast_data = await response.json()
                    
                    # Группируем данные по дням
                    daily_stats = {}
                    for item in forecast_data['list']:
                        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                        if date not in daily_stats:
                            daily_stats[date] = {
                                'temps': [],
                                'humidity': [],
                                'pressure': [],
                                'wind_speed': []
                            }
                        
                        daily_stats[date]['temps'].append(item['main']['temp'])
                        daily_stats[date]['humidity'].append(item['main']['humidity'])
                        daily_stats[date]['pressure'].append(item['main']['pressure'])
                        daily_stats[date]['wind_speed'].append(item['wind']['speed'])
                    
                    # Вычисляем статистику для каждого дня
                    weekly_stats = {
                        "city": city_name,
                        "coordinates": {"lat": lat, "lon": lon},
                        "generated_at": datetime.now().isoformat(),
                        "daily_statistics": {}
                    }
                    
                    for date, stats in daily_stats.items():
                        weekly_stats["daily_statistics"][date] = {
                            "temperature": {
                                "min": min(stats['temps']),
                                "max": max(stats['temps']),
                                "avg": sum(stats['temps']) / len(stats['temps'])
                            },
                            "humidity": {
                                "min": min(stats['humidity']),
                                "max": max(stats['humidity']),
                                "avg": sum(stats['humidity']) / len(stats['humidity'])
                            },
                            "pressure": {
                                "min": min(stats['pressure']),
                                "max": max(stats['pressure']),
                                "avg": sum(stats['pressure']) / len(stats['pressure'])
                            },
                            "wind_speed": {
                                "min": min(stats['wind_speed']),
                                "max": max(stats['wind_speed']),
                                "avg": sum(stats['wind_speed']) / len(stats['wind_speed'])
                            }
                        }
                    
                    return weekly_stats
                else:
                    raise Exception("Error getting forecast data")

    def save_to_json(self, data: dict, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filename