from aiogram import types, Router
from aiogram.exceptions import TelegramBadRequest

from bot import bot
from database.database import pg_con

router = Router()


async def update_reaction_count(conn, chat_id, message_id, delta):
    data_message = await conn.fetchrow(
        'SELECT reaction_count FROM message WHERE chat_id = $1 AND message_id = $2',
        chat_id, message_id
    )

    if data_message is None and delta > 0:
        await conn.execute(
            'INSERT INTO message (chat_id, message_id, reaction_count) VALUES ($1, $2, $3)',
            chat_id, message_id, delta
        )
    elif data_message:
        await conn.execute(
            'UPDATE message SET reaction_count = reaction_count + $3 WHERE chat_id = $1 AND message_id = $2',
            chat_id, message_id, delta
        )


@router.message_reaction()
async def register_message_reaction(event: types.MessageReactionUpdated):
    if event.chat.type not in {'group', 'supergroup'}:
        return

    conn = await pg_con()

    data_reaction = await conn.fetchval('SELECT emoji_list FROM chat WHERE chat_id = $1', event.chat.id)
    if not data_reaction:
        return

    valid_emojis = set(data_reaction)

    if event.new_reaction:
        for reaction in event.new_reaction:
            emoji = reaction.model_dump()['emoji']
            if emoji in valid_emojis:
                await update_reaction_count(conn, event.chat.id, event.message_id, 1)

    if event.old_reaction:
        for reaction in event.old_reaction:
            emoji = reaction.model_dump()['emoji']
            if emoji in valid_emojis:
                await update_reaction_count(conn, event.chat.id, event.message_id, -1)

    reaction_count_message = await conn.fetchrow('SELECT reaction_count FROM message WHERE chat_id = $1 AND message_id = $2',
                                              event.chat.id, event.message_id
                                                 )

    reaction_count_chat = await conn.fetchrow('SELECT min_reaction_count, channel_id FROM chat WHERE chat_id = $1',
                                              event.chat.id
                                              )

    try:
        if reaction_count_message[0] >= reaction_count_chat[0] and reaction_count_chat[1] is not None:
            await bot.copy_message(message_id=event.message_id, from_chat_id=event.chat.id, chat_id=reaction_count_chat[1])
    except TelegramBadRequest:
        return