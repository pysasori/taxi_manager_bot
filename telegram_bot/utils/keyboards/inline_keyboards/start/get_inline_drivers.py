from asgiref.sync import sync_to_async
from aiogram import types
from telegram_bot.models import Driver
from typing import List


async def get_inline_drivers() -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup with driver options.
    """
    drivers: List[Driver] = await sync_to_async(list)(Driver.objects.all())
    buttons: List[List[types.InlineKeyboardButton]] = []
    for driver in drivers:
        button: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text=driver.name,
            callback_data=f"driver_{driver.id}"
        )
        buttons.append([button])
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
