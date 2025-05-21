import threading
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from config import API_ID, API_HASH, BOT_TOKEN
from mn_bots.search import handle_search, handle_callback
from mn_bots.start import handle_start
from web import app as flask_app

bot = Client("file_search_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.private & filters.command("start"))
async def start_command(client, message: Message):
    await handle_start(client, message)

@bot.on_message(filters.private & filters.text & ~filters.command("start"))
async def search_command(client, message: Message):
    await handle_search(client, message)

@bot.on_callback_query()
async def callback_query(client, callback_query: CallbackQuery):
    await handle_callback(client, callback_query)

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run()
