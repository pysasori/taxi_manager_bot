from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from asgiref.sync import sync_to_async
from django.db.models import Subquery

import telegram_bot.utils as utils
from ..bot import bot
from ..models import Driver, FuelBill

router: Router = Router()


class States(StatesGroup):
    get_info_fuel_volume: State = State()
    get_info_fuel_price: State = State()


@router.callback_query(lambda c: c.data == "get_info_fuel")
async def get_info_fuel(callback: types.CallbackQuery) -> None:
    """
    Callback handler for initiating the process of entering fuel information.

    """
    await callback.message.edit_text(
        "Вы действительно хотите отправить данные о заправке❓",
        reply_markup=await utils.inline_get_info_fuel()
    )


@router.callback_query(lambda c: c.data == "get_info_fuel_volume")
async def get_info_fuel_volume(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for starting the process of entering fuel volume.

    """
    await state.set_state(States.get_info_fuel_volume)
    await callback.message.edit_text("Введите объем топлива")


@router.message(States.get_info_fuel_volume)
async def get_info_fuel_volume_agree(message: Message, state: FSMContext) -> None:
    """
    Message handler for confirming the entered fuel volume.

    """
    await message.answer(
        f"Ваш объем топлива {message.text} литров. Верно?",
        reply_markup=await utils.inline_get_info_fuel_volume_agree()
    )
    await state.update_data(get_info_fuel_volume=message.text)
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@router.callback_query(lambda c: c.data == "get_info_fuel_price")
async def get_info_fuel_price(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for starting the process of entering fuel price.

    """
    await state.set_state(States.get_info_fuel_price)
    await callback.message.edit_text("Введите цену топлива")


@router.message(States.get_info_fuel_price)
async def get_info_fuel_price_agree(message: Message, state: FSMContext) -> None:
    """
    Message handler for confirming the entered fuel price.

    """
    await message.answer(
        f"Ваша цена за топливо {message.text} евро. Верно?",
        reply_markup=await utils.inline_get_info_fuel_price_agree()
    )
    await state.update_data(get_info_fuel_price=message.text)
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@router.callback_query(lambda c: c.data == "close_get_info_fuel")
async def close_get_info_fuel(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for confirming the closure of fuel information entry and saving the data.

    """
    user_data: dict = await state.get_data()

    driver_subquery = Driver.objects.filter(telegram_id=callback.from_user.id).values('id')[:1]

    await sync_to_async(FuelBill.objects.create)(
        driver_id=Subquery(driver_subquery),
        price=user_data.get('get_info_fuel_price'),
        volume=user_data.get('get_info_fuel_volume')
    )

    await callback.message.edit_text('Ваши данные внесены, спасибо❗')
    await state.clear()
    await callback.message.answer(
        f"👉 Выберите нужный вам пункт",
        reply_markup=await utils.inline_main_menu()
    )
