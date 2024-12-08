from aiogram import Dispatcher

from events import join_chat, reactions
from commands import set_channel, set_emoji

def setup_routers(dp: Dispatcher):
    # Events
    dp.include_router(reactions.router)
    dp.include_router(join_chat.router)

    # Commands
    dp.include_router(set_channel.router)
    dp.include_router(set_emoji.router)
