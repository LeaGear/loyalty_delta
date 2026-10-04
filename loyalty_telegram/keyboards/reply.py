from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser

reg_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Registration")]
    ],
    resize_keyboard=True
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Get code!")
        ],
        [
            KeyboardButton(text="My profile"),
            KeyboardButton(text="Settings")
        ]
    ],
    resize_keyboard=True
)

share_contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Share telegram phone number", request_contact=True)
        ]
    ]
)