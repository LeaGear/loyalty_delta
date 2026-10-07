import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers.user_private import user_private_public_router, user_private_protected_router

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_routers(user_private_public_router, user_private_protected_router)

async def main():

    print("Bot is running...")
    await dp.start_polling(bot)
    print("Bot is off...")


asyncio.run(main())
