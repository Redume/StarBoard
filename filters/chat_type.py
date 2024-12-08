from aiogram.filters import BaseFilter
from aiogram.types import Message

# https://stackoverflow.com/a/78272229/20781634
class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: str | list):
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type