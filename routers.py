from aiogram import Dispatcher
from events import join_chat, reactions
from commands import set_channel

def setup_routers(dp: Dispatcher):
    dp.include_router(reactions.router)
    dp.include_router(join_chat.router)
    dp.include_router(set_channel.router)