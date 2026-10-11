from aiogram import BaseMiddleware

from keyboards.reply import reg_keyboard
from logic.api_client import check_user_status

class RegisteredOnlyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = data['event_from_user']
        response = await check_user_status(user.id)
        if response is None:
            await event.answer("Service unavailable!")
            return
        if response.status_code != 200:
            await event.answer("Please register first: /register", reply_markup=reg_keyboard)
            return
        return await handler(event, data)

