import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
bot = Bot(BOT_TOKEN) if BOT_TOKEN else None
dp = Dispatcher()


@dp.message(F.text.lower().startswith("/start"))
async def start(message: Message) -> None:
    text = (
        "Привет! Go Out Today — свайпы мест. Открой мини-приложение по кнопке, выбери фильтры, "
        "свайпай и зови друзей."
    )
    await message.answer(text)


@dp.message()
async def fallback(message: Message) -> None:
    await message.answer("Используй мини-приложение для свайпов. Напиши /start.")


async def main() -> None:
    if not bot:
        print("Set BOT_TOKEN in env")
        return
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
