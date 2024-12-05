from aiogram import Bot, Dispatcher

import asyncio
import yaml

from events import join_chat, reactions

config = yaml.safe_load(open('config.yaml'))

dp = Dispatcher()
bot = Bot(config['token'])

dp.include_router(router=reactions.router)
dp.include_router(router=join_chat.router)


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))