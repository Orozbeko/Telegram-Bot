from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from os import getenv
from database.database import Database
from pathlib import Path


database = Database(Path('__file__').parent / 'db.sqlite')


load_dotenv()
bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher()


async def set_menu():
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Начало"),
        types.BotCommand(command="opros", description="Пройдите опрос"),
        types.BotCommand(command="shop", description="Магазин")
    ])