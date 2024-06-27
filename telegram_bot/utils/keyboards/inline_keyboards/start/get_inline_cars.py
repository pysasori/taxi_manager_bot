from asgiref.sync import sync_to_async
from aiogram import types
from telegram_bot.models import Car
from typing import List


async def get_inline_cars() -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup with car options.
    """
    cars: List[Car] = await sync_to_async(list)(Car.objects.all())
    buttons: List[List[types.InlineKeyboardButton]] = []
    for car in cars:
        button: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text=f'{car.name}({car.number_car})',
            callback_data=f"car_{car.id}"
        )
        buttons.append([button])
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
