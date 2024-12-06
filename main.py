from aiogram import Bot, Dispatcher

import asyncio
import yaml

from bot import bot
from routers import setup_routers

config = yaml.safe_load(open('config.yaml'))

dp = Dispatcher()
setup_routers(dp)


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))