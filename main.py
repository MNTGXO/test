from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from config import API_ID, API_HASH, BOT_TOKEN
from mn_bots.search import handle_search, handle_callback
from mn_bots.start import handle_start

app = Client("file_search_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.command("start"))
async def start_command(client, message: Message):
    await handle_start(client, message)

@app.on_message(filters.private & filters.text & ~filters.command("start"))
async def search_command(client, message: Message):
    await handle_search(client, message)

@app.on_callback_query()
async def callback_query(client, callback_query: CallbackQuery):
    await handle_callback(client, callback_query)

if __name__ == "__main__":
    app.run()
