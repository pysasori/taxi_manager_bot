from aiogram import types
from typing import List


async def inline_check_shift() -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup for confirming the shift check.
    """
    buttons: List[List[types.InlineKeyboardButton]] = [
        [types.InlineKeyboardButton(text="Да", callback_data="mileage_car_shift_info")],
        [types.InlineKeyboardButton(text="Нет", callback_data="main_menu")],
    ]
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
