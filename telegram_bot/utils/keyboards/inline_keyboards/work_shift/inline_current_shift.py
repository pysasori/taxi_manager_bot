from aiogram import types
from typing import List


async def inline_current_shift() -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup for the current shift menu.
    """
    buttons: List[List[types.InlineKeyboardButton]] = [
        [types.InlineKeyboardButton(text="Закончить смену", callback_data="end_shift")],
        [types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data="main_menu")],
    ]
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
