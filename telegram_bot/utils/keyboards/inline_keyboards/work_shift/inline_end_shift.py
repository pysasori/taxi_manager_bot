from aiogram import types
from typing import List


async def inline_end_shift() -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup for confirming the end of the shift.
    """
    buttons: List[List[types.InlineKeyboardButton]] = [
        [types.InlineKeyboardButton(text="Да, я хочу закончить смену", callback_data="agree_end_shift")],
        [types.InlineKeyboardButton(text="Нет, я хочу продолжить смену", callback_data="current_shift")],
    ]
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
