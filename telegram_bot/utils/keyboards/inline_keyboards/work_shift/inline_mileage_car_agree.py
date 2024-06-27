from aiogram import types
from typing import List


async def inline_mileage_car_agree() -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup for confirming the entered mileage.
    """
    buttons: List[List[types.InlineKeyboardButton]] = [
        [types.InlineKeyboardButton(text="Да, я все ввел верно", callback_data="current_shift")],
        [types.InlineKeyboardButton(text="Нет, я ошибся", callback_data="mileage_car_shift_info")],
    ]
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
