from pyrogram import Client
from pyrogram.types import Message

async def handle_start(client: Client, message: Message):
    await message.reply_text(
        f"👋 Hi {message.from_user.mention},\n\n"
        "Send me a search query and I’ll find files for you!",
        quote=True
    )
