from aiogram import types, Router
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER

from database.database import pg_con

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER))
async def join_chat(event: types.Message):
    if event.chat.type not in {'group', 'supergroup'}:
        return

    conn = await pg_con()
    data = await conn.fetch('SELECT emoji_list FROM chat WHERE chat_id = $1', event.chat.id)

    if len(data) == 0:
        await conn.execute('INSERT INTO chat (chat_id) VALUES ($1)', event.chat.id)
