from main import *
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, types
from aiogram.filters.command import Command
from aiogram.types import Message

WEATHER_API_KEY = 'KlrnNrBdipA7L9DwvbwLgPYvrziVBHA1'
WEATHER_API_URL = 'http://dataservice.accuweather.com/'

# логирование
logging.basicConfig(level=logging.INFO)
# бот и диспетчер
TOKEN = getenv("")
bot = Bot(token="")
dp = Dispatcher()


# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Добрый день! Я - бот прогноза погоды:)\n"
                        "Выберите команду:\n"
                        "/help - Список доступных команд\n"
                        "/weather - Прогноз погоды")


# Команда /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.reply("Доступные команды:\n"
                        "/start - Приветствие\n"
                        "/help - Справка по командам\n"
                        "/weather - Прогноз погоды")


# Команда /weather
@dp.message(Command("weather"))
async def cmd_weather(message: types.Message):
    await message.reply("Введите начальную и конечную точки маршрута (через запятую)")


@dp.message()
async def process_route(message: types.Message):
    route = message.text.split(',')
    route = [point.strip() for point in route]

    if len(route) < 2:
        await message.reply("Пожалуйста, введите начальную и конечную точки")
        return

    await message.reply('Погода в начальной точке:' + str(simple_get_weather(route[0])))
    await message.reply('Погода в конечной точке:' + str(simple_get_weather(route[1])))

@dp.errors()
async def error_handler(update: types.Update):
    logging.error(f'Update: {update} caused error')


async def main():
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_weather, Command("weather"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

