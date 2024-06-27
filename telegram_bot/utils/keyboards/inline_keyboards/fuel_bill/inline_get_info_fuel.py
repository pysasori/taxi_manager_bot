from aiogram import types
from typing import List


async def inline_get_info_fuel() -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup for confirming fuel information entry.
    """
    buttons: List[List[types.InlineKeyboardButton]] = [
        [types.InlineKeyboardButton(text="Да", callback_data="get_info_fuel_volume")],
        [types.InlineKeyboardButton(text="Нет", callback_data="main_menu")],
    ]
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
