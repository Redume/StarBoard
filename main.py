import asyncio

import yaml
from aiogram import Dispatcher

from bot import bot
from routers import setup_routers

config = yaml.safe_load(open('config.yaml'))

dp = Dispatcher()
setup_routers(dp)


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
