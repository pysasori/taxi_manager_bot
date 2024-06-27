from aiogram import types
from typing import List


async def inline_change_car() -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup for changing the car.
    """
    buttons: List[List[types.InlineKeyboardButton]] = [
        [types.InlineKeyboardButton(text="Да", callback_data="change_car_get")],
        [types.InlineKeyboardButton(text="Нет", callback_data="main_menu")],
    ]
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
