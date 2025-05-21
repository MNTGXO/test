from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import CHANNELS, BOT_USERNAME, REDIRECT_CHANNEL, REDIRECT_INVITE
import asyncio

RESULTS = {}

async def handle_search(client: Client, message: Message):
    query = message.text.strip()
    results = []

    for channel_id in CHANNELS:
        try:
            async for msg in client.search_messages(channel_id, query=query, filter="document"):
                file_name = msg.document.file_name if msg.document else "No Name"
                file_size = sizeof_fmt(msg.document.file_size) if msg.document else "Unknown Size"
                results.append({"msg_id": msg.id, "chat_id": msg.chat.id, "name": file_name, "size": file_size})
        except Exception:
            continue

    if not results:
        return await message.reply("No results found.")

    RESULTS[message.chat.id] = results
    await send_page(client, message, page=0)

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T"]:
        if abs(num) < 1024.0:
            return f"{num:.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} P{suffix}"

async def send_page(client, message, page):
    results = RESULTS.get(message.chat.id, [])
    start = page * 10
    end = start + 10
    buttons = []

    for item in results[start:end]:
        callback_data = f"get_{item['chat_id']}_{item['msg_id']}"
        buttons.append([InlineKeyboardButton(f"[{item['size']}] {item['name']}", callback_data=callback_data)])

    nav_buttons = []
    if start > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"page_{page - 1}"))
    if end < len(results):
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_{page + 1}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    await message.reply("Select a file:", reply_markup=InlineKeyboardMarkup(buttons))

async def handle_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data

    if data.startswith("page_"):
        page = int(data.split("_")[1])
        await callback_query.message.delete()
        await send_page(client, callback_query.message, page)
        await callback_query.answer()

    elif data.startswith("get_"):
        _, chat_id, msg_id = data.split("_", 2)
        chat_id = int(chat_id)
        msg_id = int(msg_id)
        user = callback_query.from_user

        try:
            fwd_msg = await client.copy_message(REDIRECT_CHANNEL, chat_id, msg_id)
            file_link = f"https://t.me/c/{str(fwd_msg.chat.id)[4:]}/{fwd_msg.id}"
            buttons = [
                [InlineKeyboardButton("📁 File Link", url=file_link)],
                [InlineKeyboardButton("🔗 Get Access to Channel", url=REDIRECT_INVITE)]
            ]

            reply = await callback_query.message.reply_text(
                f"**Here's your file:**", reply_markup=InlineKeyboardMarkup(buttons)
            )

            await asyncio.sleep(120)
            await client.delete_messages(REDIRECT_CHANNEL, fwd_msg.id)
            await reply.delete()
            await callback_query.message.delete()

        except Exception as e:
            await callback_query.message.reply(f"Failed to send file: {e}")
        await callback_query.answer()
