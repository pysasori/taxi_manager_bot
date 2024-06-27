from aiogram import types
from typing import List


async def inline_get_info_fuel_volume_agree() -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup for confirming the entered fuel volume.
    """
    buttons: List[List[types.InlineKeyboardButton]] = [
        [types.InlineKeyboardButton(text="Да", callback_data="get_info_fuel_price")],
        [types.InlineKeyboardButton(text="Нет", callback_data="get_info_fuel_volume")],
    ]
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

