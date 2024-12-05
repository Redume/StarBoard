from aiogram import Bot, Dispatcher, types
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER

import asyncio
import yaml

from database.database import pg_con

config = yaml.safe_load(open('config.yaml'))

dp = Dispatcher()
bot = Bot(config['token'])


@dp.message_reaction()
async def message_reaction_handler(event: types.MessageReactionUpdated):
    if event.chat.type != 'group' and event.chat.type != 'supergroup':
        return

    conn = await pg_con()

    if event.new_reaction is not None and len(event.new_reaction) > 0:

        for n in range(len(event.new_reaction)):
            data_reaction = await conn.fetchrow('SELECT emoji_list FROM chat WHERE chat_id = $1', event.chat.id)


            if data_reaction[0][n] == event.new_reaction[n].model_dump()['emoji']:
                data_message = await conn.fetchrow(
                                                'SELECT reaction_count FROM message '
                                                'WHERE chat_id = $1 AND message_id = $2',
                                                    event.chat.id,
                                                    event.message_id
                                                )

                if data_message is None:
                    await conn.execute(
                                        'INSERT INTO message (chat_id, message_id, reaction_count) VALUES ($1, $2, $3)',
                                            event.chat.id,
                                            event.message_id,
                                            1
                                        )
                else:
                    await conn.execute('UPDATE message SET reaction_count = reaction_count + 1 '
                                       'WHERE chat_id = $1 AND message_id = $2',
                                           event.chat.id,
                                           event.message_id,
                                       )
    if event.old_reaction is not None and len(event.old_reaction) > 0:

        for n in range(len(event.old_reaction)):
            data_reaction = await conn.fetchrow('SELECT emoji_list FROM chat WHERE chat_id = $1', event.chat.id)

            if data_reaction[0][n] == event.old_reaction[n].model_dump()['emoji']:
                data_message = await conn.fetchrow(
                    'SELECT reaction_count FROM message '
                    'WHERE chat_id = $1 AND message_id = $2',
                    event.chat.id,
                    event.message_id
                )

                if data_message is None:
                    return

                else:
                    await conn.execute('UPDATE message SET reaction_count = reaction_count - 1 '
                                       'WHERE chat_id = $1 AND message_id = $2',
                                       event.chat.id,
                                       event.message_id
                                       )


@dp.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER))
async def event_channel(channel: types.Message):
    if channel.chat.type != 'group' and channel.chat.type != 'supergroup':
        return

    conn = await pg_con()
    data = await conn.fetch('SELECT emoji_list FROM chat WHERE chat_id = $1', channel.chat.id)

    if len(data) == 0:
        await conn.execute('INSERT INTO chat (chat_id) VALUES ($1)', channel.chat.id)


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))