from aiogram import F, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from logic.api_client import registration_new_client, check_user_status
from keyboards.reply import main_keyboard, reg_keyboard, share_contact_keyboard

user_private_router = Router()

class RegistrationNewClientState(StatesGroup):
    user_phone_number = State()
    user_name = State()
    user_id = State()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    response = await check_user_status(message.from_user.id)
    print(response)
    if response.status_code == 200:
        await message.answer("Main Menu", reply_markup=main_keyboard)
    else:
        await message.answer(f"Hello, {message.from_user.first_name}!", reply_markup=reg_keyboard)

@user_private_router.message(F.text == 'Registration')
async def registration_start(message: types.Message, state: FSMContext):
    response = await check_user_status(message.from_user.id)
    if response.status_code == 200:
        await message.answer("You are registered!", reply_markup=main_keyboard)
        return
    await message.answer("Share your contact!", reply_markup=share_contact_keyboard)
    await state.set_state(RegistrationNewClientState.user_phone_number)

@user_private_router.message(RegistrationNewClientState.user_phone_number, F.contact)
async def registration_get_user_contact(message: types.Message, state: FSMContext):
    if message.contact.user_id != message.from_user.id:
        await message.answer("Please share your own contact using the button.")
        return
    number = "+" + message.contact.phone_number.lstrip("+")
    await state.update_data(user_phone_number=number, user_id=message.contact.user_id)
    name = " ".join(filter(None, [message.contact.first_name, message.contact.last_name]))
    name = "" #TODO: Only for  testing
    if not name:
        await message.answer("Your profile has no name. Enter please!", reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationNewClientState.user_name)
        return
    await state.update_data(user_name=name)
    await registration_complete(message,state)

@user_private_router.message(RegistrationNewClientState.user_phone_number)
async def registration_wrong_contact(message: types.Message):
    await message.answer("Please use the button to share your contact.",
                         reply_markup=share_contact_keyboard)

@user_private_router.message(RegistrationNewClientState.user_name, F.text)
async def registration_get_custom_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if len(name) > 100:
        await message.answer("Name is too long. Try a shorter one!")
        return
    await state.update_data(user_name=name)
    await message.answer(f"Your name is {name}")
    await registration_complete(message, state)

async def registration_complete(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    response = await registration_new_client(
        user_data.get("user_name"),
        user_data.get("user_phone_number"),
        user_data.get("user_id")
    )
    if response.status_code == 200:
        await message.answer(
            f"Your name -> {user_data.get('user_name')}\n"
            f"Your phone number -> {user_data.get('user_phone_number')}\n"
            f"Thank you for registration!",
            reply_markup=main_keyboard
        )
        await state.clear()
    else:
        await message.answer(f"Ohhhhh shiiit!((( - {response.json().get('detail')}")