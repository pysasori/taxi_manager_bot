import asyncio
import logging
import sys

from django.core.management.base import BaseCommand
from telegram_bot.main import main


class Command(BaseCommand):
    help = "Start telegram bot"

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
