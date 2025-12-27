import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.handlers import channel, user

# logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    if BOT_TOKEN == "PLACEHOLDER_TOKEN":
        print("ERROR: BOT_TOKEN is not set in .env file!")
        return

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Register routers
    dp.include_router(channel.router)
    dp.include_router(user.router)
    
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
