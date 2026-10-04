from aiogram import F, types, Router
from aiogram.filters import CommandStart

from logic.api_client import fast_test

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"Hello, {message.from_user.first_name}!")

@user_private_router.message(F.text == '/bob')
async def bob_cmd(message: types.Message):
    resp = await fast_test()
    await message.answer(resp.get("message"))