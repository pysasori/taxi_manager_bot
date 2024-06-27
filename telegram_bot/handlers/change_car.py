from aiogram import Router, types, F
from asgiref.sync import sync_to_async
from django.db.models import Subquery

import telegram_bot.utils as utils
from telegram_bot.models import Driver

router: Router = Router()


@router.callback_query(lambda c: c.data == "change_car")
async def change_car(callback: types.CallbackQuery) -> None:
    """
    Callback handler for initiating the process of changing the car.

    """
    await callback.message.edit_text(
        "Вы действительно хотите сменить машину❓",
        reply_markup=await utils.inline_change_car()
    )


@router.callback_query(lambda c: c.data == "change_car_get")
async def change_car_get(callback: types.CallbackQuery) -> None:
    """
    Callback handler for selecting the car to change to.

    """
    await callback.message.edit_text(
        "Выберите машину для смены",
        reply_markup=await utils.get_inline_change_car()
    )


@router.callback_query(F.data.startswith("change_car_"))
async def process_car_id(callback: types.CallbackQuery) -> None:
    """
    Callback handler for processing the selected car ID for change.

    """
    car_id: str = callback.data.split("_")[-1]
    await sync_to_async(Driver.objects.filter(telegram_id=callback.from_user.id).update)(car_id=car_id)
    await callback.message.edit_text(
        "Ваша машина изменена‼️ \n👉 Выберите нужный вам пункт",
        reply_markup=await utils.inline_main_menu()
    )
