from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.database import pg_con
from filters.chat_type import ChatTypeFilter

router = Router()

@router.message(Command('set_channel'), ChatTypeFilter(chat_type=["group", "supergroup"]))
async def set_channel(message: Message):
    args = message.text.split()

    if len(args) < 2:
        return message.reply('Отсутствует ID канала (формат BOT API)')

    conn = await pg_con()

    data = await conn.fetchrow('SELECT channel_id FROM chat WHERE chat_id = $1', message.chat.id)

    if data[0] == args[1]:
        return message.reply('Такой ID канала уже установлен')

    await conn.execute('UPDATE chat SET channel_id = $1 WHERE chat_id = $2 ', args[1], message.chat.id)