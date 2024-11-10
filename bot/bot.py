# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import load_config
from handlers.user_handlers import router
from services.weather_api import WeatherAPI

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Загружаем конфиг
    config = load_config()
    
    # Инициализируем бота и диспетчер
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Создаем экземпляр WeatherAPI
    weather_api = WeatherAPI(config.WEATHER_API_KEY)
    
    # Регистрируем роутер
    dp.include_router(router)
    
    # Передаем weather_api в middleware
    dp["weather_api"] = weather_api
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


