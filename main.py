import asyncio
import datetime
import os

from bot.base import Bot
from dotenv import load_dotenv

load_dotenv()

async def main():
    bot = Bot(os.getenv("BOT_TOKEN"), int(os.getenv("COUNT_WORKERS")))
    print('bot has been started')

    try:
        await bot.start()
        while True:
            await asyncio.sleep(3600)  # или await some signal
    except KeyboardInterrupt:
        print("\nstopping", datetime.datetime.now())
        await bot.stop()
        print('bot has been stopped', datetime.datetime.now())

if __name__ == '__main__':
    asyncio.run(main())