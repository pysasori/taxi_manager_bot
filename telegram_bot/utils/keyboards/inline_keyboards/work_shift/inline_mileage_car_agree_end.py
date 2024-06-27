from aiogram import types
from typing import List


async def inline_mileage_car_agree_end() -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup for confirming the entered mileage at the end of a shift.
    """
    buttons: List[List[types.InlineKeyboardButton]] = [
        [types.InlineKeyboardButton(text="Да, я все ввел верно", callback_data="close_shift")],
        [types.InlineKeyboardButton(text="Нет, я ошибся", callback_data="agree_end_shift")],
    ]
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
