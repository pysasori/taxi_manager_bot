from aiogram import types
import os


async def inline_main_menu(username: str = os.getenv('USERNAME')) -> types.InlineKeyboardMarkup:
    """
    Asynchronously retrieves inline keyboard markup for the main menu.
    """
    buttons: list = [
        [types.InlineKeyboardButton(text="Смена", callback_data="check_shift")],
        [types.InlineKeyboardButton(text="Фактура за бензин", callback_data="get_info_fuel")],
        [types.InlineKeyboardButton(text="Связаться с администратором", url=f'https://t.me/{username}')],
    ]
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
