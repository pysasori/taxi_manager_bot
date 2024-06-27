# import asyncio
#
# from main.celery import app
# from telegram_bot import utils
# from telegram_bot.models import WorkShift
# from telegram_bot.bot import bot
#
# @app.task #регистриуем таску
# def repeat_order_make():
#     zxc = WorkShift.objects.filter(active=True).all()
#     for shift in zxc:
#
#         asyncio.run(send_notification_message(shift.chat_id))
#
#
# async def send_notification_message(chat_id: str) -> None:
#     """Отправляем напоминалку"""
#     await bot.send_message(
#         chat_id=int(chat_id),
#         text="Ваша смена идет",
#         reply_markup=await utils.inline_current_shift()
#     )
import asyncio
from asgiref.sync import sync_to_async
from main.celery import app
from telegram_bot import utils
from telegram_bot.models import WorkShift
from telegram_bot.bot import bot

@app.task
def repeat_order_make():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_repeat_order_make())

async def run_repeat_order_make():
    zxc = await sync_to_async(list)(WorkShift.objects.filter(active=True))
    tasks = []
    for shift in zxc:
        tasks.append(send_notification_message(shift.chat_id))
    await asyncio.gather(*tasks)

async def send_notification_message(chat_id: str) -> None:
    """Отправляем напоминалку"""
    await bot.send_message(
        chat_id=int(chat_id),
        text="Ваша смена все еще идет❗ ",
        reply_markup=await utils.inline_current_shift()
    )