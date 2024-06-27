from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from asgiref.sync import sync_to_async
from django.utils import timezone

import telegram_bot.utils as utils
from telegram_bot.models import Driver, WorkShift
from telegram_bot.bot import bot

router: Router = Router()


class States(StatesGroup):
    mileage_car_start: State = State()
    mileage_car_end: State = State()


def is_float(s: str) -> bool:
    """
    Check if the input string can be converted to a float.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


@router.callback_query(lambda c: c.data == "check_shift")
async def check_shift(callback: types.CallbackQuery) -> None:
    """
    Callback handler for checking the current shift status.

    """
    shift: WorkShift = await sync_to_async(
        WorkShift.objects.filter(driver__telegram_id=callback.from_user.id, active=True).first
    )()
    if shift:
        await callback.message.edit_text(
            f"Ваша смена идет❗",
            reply_markup=await utils.inline_current_shift()
        )
    else:
        await callback.message.edit_text(
            "Вы действительно хотите начать смену❓",
            reply_markup=await utils.inline_check_shift()
        )


@router.callback_query(lambda c: c.data == "mileage_car_shift_info")
async def mileage_car_shift_info(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for starting the process of entering car mileage.

    """
    await state.set_state(States.mileage_car_start)
    await callback.message.edit_text("Введите пробег автомобиля")


@router.message(States.mileage_car_start)
async def mileage_car_start(message: types.Message, state: FSMContext) -> None:
    """
    Message handler for entering the starting mileage of the car.

    """
    if is_float(message.text):
        driver: Driver = await sync_to_async(
            Driver.objects.filter(telegram_id=message.from_user.id).first
        )()
        mileage: float = await sync_to_async(lambda: driver.car.mileage)()
        if mileage < float(message.text):
            await message.answer(
                f"Ваш пробег {message.text} километров. Верно?",
                reply_markup=await utils.inline_mileage_car_agree()
            )
            await state.update_data(mileage_car_start=message.text)
        else:
            await message.answer(
                "Вы ввели неверный пробег, он меньше текущего"
                "\nПример пробега: 1698.65"
                "\nВведите пробег автомобиля снова"
            )
    else:
        await message.answer(
            "Вы ввели неверно число"
            "\nПример пробега: 1698.65"
            "\nВведите пробег автомобиля снова"
        )

    await bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@router.callback_query(lambda c: c.data == "current_shift")
async def current_shift(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for starting a new shift.

    """
    user_data: dict = await state.get_data()
    driver: Driver = await sync_to_async(Driver.objects.filter(telegram_id=callback.from_user.id).first)()
    if driver:
        await sync_to_async(WorkShift.objects.create)(
            driver=driver,
            car=await sync_to_async(lambda: driver.car)(),
            mileage_car_start=user_data.get('mileage_car_start'),
            start_trip=timezone.now(),
            chat_id=callback.message.chat.id
        )
    await state.clear()
    await callback.message.edit_text(
        f"Ваша смена Началась❗",
        reply_markup=await utils.inline_current_shift()
    )


@router.callback_query(lambda c: c.data == "end_shift")
async def end_shift(callback: types.CallbackQuery) -> None:
    """
    Callback handler for confirming the end of the shift.

    """
    await callback.message.edit_text(
        f"Вы действительно хотите завершить смену❓",
        reply_markup=await utils.inline_end_shift()
    )


@router.callback_query(lambda c: c.data == "agree_end_shift")
async def agree_end_shift(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for confirming the end of the shift and entering final car mileage.

    """
    await state.set_state(States.mileage_car_end)
    await callback.message.edit_text("Введите пробег автомобиля")


@router.message(States.mileage_car_end)
async def mileage_car_end(message: types.Message, state: FSMContext) -> None:
    """
    Message handler for entering the final mileage of the car.

    """
    if not is_float(message.text):
        await message.answer(
            "Вы ввели неверно число"
            "\nПример пробега: 1698.65"
            "\nВведите пробег автомобиля снова"
        )

    work_shift: WorkShift = await sync_to_async(WorkShift.objects.filter(
        driver__telegram_id=message.from_user.id,
        active=True
    ).first)()
    if float(message.text) - work_shift.mileage_car_start < 0:
        await message.answer(
            f"Вы ввели неверный пробег"
            f"\nВаш стартовый пробег {work_shift.mileage_car_start} км."
            f"\nСейчас вы ввели {message.text} км."
        )
    else:
        await message.answer(
            f"Ваш пробег {message.text} километров. Верно?",
            reply_markup=await utils.inline_mileage_car_agree_end()
        )
        await state.update_data(mileage_car_end=message.text)
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@router.callback_query(lambda c: c.data == "close_shift")
async def agree_end_shift(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for confirming the closure of the shift and updating shift details.

    """
    user_data: dict = await state.get_data()

    work_shift: WorkShift = await sync_to_async(
        WorkShift.objects.filter(driver__telegram_id=callback.from_user.id, active=True).first)()
    if work_shift:
        # Update work_shift fields
        work_shift.mileage_car_difference = float(user_data.get('mileage_car_end')) - work_shift.mileage_car_start
        work_shift.duration = timezone.now() - work_shift.start_trip
        work_shift.mileage_car_end = user_data.get('mileage_car_end')
        work_shift.active = False
        work_shift.end_trip = timezone.now()

        # Save changes to work_shift
        await sync_to_async(work_shift.save)()

        # Update car's mileage field
        car: Car = await sync_to_async(lambda: work_shift.car)()
        car.mileage = user_data.get('mileage_car_end')

        # Save changes to car
        await sync_to_async(car.save)()

    await state.clear()

    await callback.message.edit_text(
        f'Смена <b>{work_shift.start_trip.date()}</b> завершена❗ '
        f'\nДлина смены <b>{work_shift.formatted_duration}</b>❗'
        f'\nПробег <b>{work_shift.mileage_car_difference}</b> километров❗'
    )
    await callback.message.answer(
        f"👉 Выберите нужный вам пункт",
        reply_markup=await utils.inline_main_menu()
    )
