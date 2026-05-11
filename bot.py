from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import os
import re

# =========================
# ENV VARIABLES
# =========================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# =========================
# BOT CLIENT
# =========================

app = Client(
    "XephiqAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================
# LOAD BAD WORDS
# =========================

with open("banned_words.txt", "r") as f:
    BAD_WORDS = [word.strip().lower() for word in f.readlines()]

# =========================
# START COMMAND
# =========================

@app.on_message(filters.command("start"))
async def start(_, message: Message):

    text = (
        "⚡ Welcome to Xephiq Assistant Bot\n\n"
        "A powerful Telegram community management bot.\n\n"
        "Code • Create • Conquer 🚀"
    )

    await message.reply_text(text)

# =========================
# HELP COMMAND
# =========================

@app.on_message(filters.command("help"))
async def help_command(_, message: Message):

    text = (
        "⚡ Xephiq Assistant Commands\n\n"
        "/start - Start bot\n"
        "/help - Show commands\n"
        "/rules - Group rules\n"
        "/ping - Bot status\n"
        "/about - About bot"
    )

    await message.reply_text(text)

# =========================
# RULES COMMAND
# =========================

@app.on_message(filters.command("rules"))
async def rules(_, message: Message):

    text = (
        "⚡ Xephiq Community Rules\n\n"
        "• Respect Everyone\n"
        "• No Spam\n"
        "• No Scam Links\n"
        "• Tech Discussion Only\n"
        "• Stay Active 🚀"
    )

    await message.reply_text(text)

# =========================
# ABOUT COMMAND
# =========================

@app.on_message(filters.command("about"))
async def about(_, message: Message):

    text = (
        "⚡ Xephiq Assistant Bot\n\n"
        "Moderation • Security • Automation\n"
        "Powered by Xephiq 🚀"
    )

    await message.reply_text(text)

# =========================
# PING COMMAND
# =========================

@app.on_message(filters.command("ping"))
async def ping(_, message: Message):

    await message.reply_text(
        "🏓 Pong!\nXephiq Assistant Bot Online ⚡"
    )

# =========================
# AUTO WELCOME
# =========================

@app.on_message(filters.new_chat_members)
async def welcome(_, message: Message):

    for user in message.new_chat_members:

        text = (
            f"⚡ Welcome {user.mention}!\n\n"
            "Welcome to Xephiq Community 🚀\n"
            "Use /rules to read the rules."
        )

        await message.reply_text(text)

# =========================
# ANTI LINK SYSTEM
# =========================

@app.on_message(filters.text & filters.group)
async def anti_link(_, message: Message):

    if not message.from_user:
        return

    member = await app.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status in [
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR
    ]:
        return

    text = message.text.lower()

    if "http" in text or "t.me/" in text:

        await message.delete()

        await message.reply_text(
            "🚫 Links are not allowed!"
        )

# =========================
# BAD WORD FILTER
# =========================

@app.on_message(filters.text & filters.group)
async def bad_words(_, message: Message):

    if not message.text:
        return

    text = message.text.lower()

    for word in BAD_WORDS:

        if re.search(rf"\\b{word}\\b", text):

            await message.delete()

            await message.reply_text(
                "⚠️ Bad language detected!"
            )

            break

# =========================
# AUTO REPLY
# =========================

@app.on_message(filters.text & filters.private)
async def auto_reply(_, message: Message):

    text = message.text.lower()

    replies = {
        "hi": "⚡ Hello from Xephiq!",
        "hello": "👋 Welcome!",
        "bot": "🤖 Xephiq Assistant Online!",
        "help": "Use /help command ⚡"
    }

    for key, value in replies.items():

        if key in text:
            await message.reply_text(value)
            break

# =========================
# BOT START
# =========================

print("⚡ Xephiq Assistant Bot Running...")

app.run()
