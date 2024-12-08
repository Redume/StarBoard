from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.database import pg_con
from filters.chat_type import ChatTypeFilter

import emoji

router = Router()


@router.message(Command('set_emoji'), ChatTypeFilter(chat_type=["group", "supergroup"]))
async def set_emoji(message: Message):
    args = message.text.split()[1:]
    emojis = []

    print(len(args))

    if len(args) < 1:
        return await message.reply('Укажи emoji в качестве аргумента')

    if emoji.is_emoji(args[0][0]) is False:
        return await message.reply('Не распознан emoji в тексте')



    for n in range(len(args)):
        for x in range(len(args[n])):

            if emoji.is_emoji(args[n][x]) is True:
                emojis.append(args[n][x])

    conn = await pg_con()

    await conn.execute('UPDATE chat SET emoji_list = $2 WHERE chat_id = $1', message.chat.id, emojis)

    await message.reply(f'Следующие emoji были установлены: {''.join(str(x) for x in emojis)}')
