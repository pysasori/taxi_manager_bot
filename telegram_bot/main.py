from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from .handlers import work_shift, start, fuel_bill, change_car
from .bot import bot


async def main() -> None:
    storage = MemoryStorage()
    dp = Dispatcher(parse_mode="HTML", storage=storage)
    dp.include_routers(
        work_shift.router,
        fuel_bill.router,
        start.router,
        change_car.router,
    )

    await dp.start_polling(bot)
