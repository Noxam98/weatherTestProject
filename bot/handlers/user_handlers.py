# handlers/user_handlers.py
from aiogram import Router, F, Bot, types
from aiogram.filters import Command
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.weather_api import WeatherAPI
from uuid import uuid4
import os

router = Router()

def get_search_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔍 Поиск города", 
        switch_inline_query_current_chat=""
    )
    return builder.as_markup()

def get_weather_keyboard(lat: float, lon: float, city_name: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📥 Скачать статистику (JSON)",
        callback_data=f"get_stats:{lat}:{lon}:{city_name}"
    )
    builder.button(
        text="🔍 Новый поиск",
        switch_inline_query_current_chat=""
    )
    return builder.as_markup()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот погоды.\n"
        "Нажмите на кнопку ниже, чтобы начать поиск города:",
        reply_markup=get_search_keyboard()
    )

@router.inline_query()
async def inline_query_handler(query: InlineQuery, weather_api: WeatherAPI):
    if len(query.query) < 2:
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title="🔍 Поиск города",
                    input_message_content=InputTextMessageContent(
                        message_text="Для поиска города введите минимум 2 буквы"
                    ),
                    description="Введите минимум 2 буквы для поиска"
                )
            ],
            cache_time=1
        )

    cities = await weather_api.search_cities(query.query)
    
    if not cities:
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title="❌ Город не найден",
                    input_message_content=InputTextMessageContent(
                        message_text="Город не найден. Попробуйте другое название или напишите на английском языке."
                    ),
                    description="Попробуйте другое название или напишите на английском"
                )
            ],
            cache_time=300
        )

    results = []
    for city in cities:
        weather_data = await weather_api.get_weather(city['lat'], city['lon'], city['name'])
        if weather_data:
            city_name = f"{city['name']}, {city.get('country', '')}"
            temperature = weather_data['temperature']
            description = weather_data['description']
            humidity = weather_data['humidity']
            feels_like = weather_data.get('feels_like', temperature)
            pressure = weather_data.get('pressure', 'N/A')
            wind_speed = weather_data.get('wind_speed', 'N/A')
            weather_icon = weather_data.get('icon', '01d')
            
            message_text = (
                f"🏙 Погода в городе {city_name}:\n\n"
                f"🌡 Температура: {temperature}°C\n"
                f"🌡 Ощущается как: {feels_like}°C\n"
                f"💧 Влажность: {humidity}%\n"
                f"🌪 Давление: {pressure} hPa\n"
                f"💨 Ветер: {wind_speed} м/с\n"
                f"☁️ {description.capitalize()}"
            )
            
            title = f"{city['name']} ({city['country']}): {temperature}°C"
            description_text = f"{description.capitalize()}, Ветер: {wind_speed} м/с"
            
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=title,
                    description=description_text,
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode="HTML"
                    ),
                    reply_markup=get_weather_keyboard(
                        city['lat'],
                        city['lon'],
                        city['name']
                    ),
                    thumb_url=f"https://openweathermap.org/img/w/{weather_icon}.png",
                    thumb_width=50,
                    thumb_height=50
                )
            )

    await query.answer(results, cache_time=300)

@router.callback_query(lambda c: c.data.startswith('get_stats:'))
async def get_stats_callback(callback_query: types.CallbackQuery, weather_api: WeatherAPI, bot: Bot):
    _, lat, lon, city_name = callback_query.data.split(':')
    try:
        # Получаем статистику за неделю
        weekly_stats = await weather_api.get_weekly_stats(float(lat), float(lon), city_name)
        
        # Создаем имя файла с использованием user_id для уникальности
        filename = f"weather_stats_{callback_query.from_user.id}_{city_name.lower().replace(' ', '_')}.json"
        
        # Сохраняем статистику в JSON
        weather_api.save_to_json(weekly_stats, filename)
        
        # Отправляем файл
        doc = types.FSInputFile(filename)
        await bot.send_document(
            callback_query.from_user.id,
            document=doc,
            caption=f"📊 Статистика погоды за 5 дней для города {city_name}"
        )
        
        # Удаляем временный файл
        os.remove(filename)
        
        await callback_query.answer("Статистика успешно отправлена!")
        
    except Exception as e:
        await callback_query.answer(f"Ошибка при получении статистики: {str(e)}", show_alert=True)
