from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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
# CONFIG
# =========================

FORCE_CHANNEL = "Xephiq"
OWNER_ID = 123456789

ALLOWED_MENTIONS = [
    "@xephiq",
    "@xephiqcommunity",
    "@xephiqassistantbot"
]

LINK_KEYWORDS = [
    "http",
    "https",
    "t.me/",
    "telegram.me",
    "discord.gg",
    "youtube.com"
]

NSFW_WORDS = [
    "sex",
    "porn",
    "nude",
    "18+",
    "xxx"
]

WARNINGS = {}
MESSAGE_COUNT = {}

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
# FORCE JOIN CHECK
# =========================

async def check_force_join(user_id):

    try:
        member = await app.get_chat_member(
            FORCE_CHANNEL,
            user_id
        )

        return member.status not in ["left", "kicked"]

    except:
        return False

# =========================
# ADMIN CHECK
# =========================

async def is_admin(chat_id, user_id):

    member = await app.get_chat_member(chat_id, user_id)

    return member.status in [
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    ]

# =========================
# START COMMAND
# =========================

@app.on_message(filters.private & filters.command("start"))
async def start(_, message: Message):

    joined = await check_force_join(message.from_user.id)

    if not joined:

        buttons = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "🚀 Join Xephiq Channel",
                    url="https://t.me/Xephiq"
                )
            ]]
        )

        await message.reply_text(
            "⚠️ You must join our official channel first!",
            reply_markup=buttons
        )
        return

    text = (
        "⚡ Welcome to Xephiq Assistant Bot

"
        "Moderation • Security • Automation
"
        "Powered by Xephiq 🚀"
    )

    await message.reply_text(text)

# =========================
# HELP COMMAND
# =========================

@app.on_message(filters.command("help"))
async def help_command(_, message: Message):

    text = (
        "⚡ Xephiq Assistant Commands

"
        "/start - Start bot
"
        "/help - Show commands
"
        "/rules - Community rules
"
        "/ping - Bot status
"
        "/warn - Warn user
"
        "/id - User ID"
    )

    await message.reply_text(text)

# =========================
# RULES COMMAND
# =========================

@app.on_message(filters.command("rules"))
async def rules(_, message: Message):

    text = (
        "⚡ Xephiq Community Rules

"
        "• Respect Everyone
"
        "• No Spam
"
        "• No NSFW
"
        "• No External Links
"
        "• No Promotions
"
        "• Stay Active 🚀"
    )

    await message.reply_text(text)

# =========================
# PING COMMAND
# =========================

@app.on_message(filters.command("ping"))
async def ping(_, message: Message):

    await message.reply_text(
        "🏓 Pong!
Xephiq Assistant Online ⚡"
    )

# =========================
# USER ID COMMAND
# =========================

@app.on_message(filters.command("id"))
async def user_id(_, message: Message):

    await message.reply_text(
        f"🆔 Your ID: {message.from_user.id}"
    )

# =========================
# AUTO WELCOME
# =========================

@app.on_message(filters.new_chat_members)
async def welcome(_, message: Message):

    for user in message.new_chat_members:

        text = (
            f"⚡ Welcome {user.mention}!

"
            "🚀 Official Channel: @Xephiq
"
            "🤖 Assistant: @XephiqAssistantBot

"
            "Use /rules to read rules."
        )

        await message.reply_text(text)

# =========================
# WARN SYSTEM
# =========================

@app.on_message(filters.command("warn") & filters.group)
async def warn(_, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("Reply to a user.")

    admin = await is_admin(
        message.chat.id,
        message.from_user.id
    )

    if not admin:
        return

    target = message.reply_to_message.from_user

    if target.id not in WARNINGS:
        WARNINGS[target.id] = 0

    WARNINGS[target.id] += 1

    warns = WARNINGS[target.id]

    await message.reply_text(
        f"⚠️ {target.mention} warned!
Warnings: {warns}/3"
    )

    if warns >= 3:

        await app.restrict_chat_member(
            message.chat.id,
            target.id,
            permissions={}
        )

        await message.reply_text(
            f"🔇 {target.mention} muted after 3 warnings!"
        )

# =========================
# SECURITY FILTER
# =========================

@app.on_message(filters.group & filters.text)
async def security(_, message: Message):

    if not message.from_user:
        return

    admin = await is_admin(
        message.chat.id,
        message.from_user.id
    )

    if admin:
        return

    text = message.text.lower()

    # LINK BLOCK
    for word in LINK_KEYWORDS:

        if word in text:

            await message.delete()

            await message.reply_text(
                "🚫 External links are not allowed!"
            )
            return

    # PHONE NUMBER BLOCK
    pattern = r"(?:\+88|88)?01[3-9]\d{8}"

    if re.search(pattern, text):

        await message.delete()

        await message.reply_text(
            "🚫 Phone numbers are not allowed!"
        )
        return

    # MENTION BLOCK
    if "@" in text:

        blocked = True

        for item in ALLOWED_MENTIONS:

            if item in text:
                blocked = False

        if blocked:

            await message.delete()

            await message.reply_text(
                "🚫 External mentions are not allowed!"
            )
            return

    # BAD WORD FILTER
    for word in BAD_WORDS:

        if re.search(rf"\b{word}\b", text):

            await message.delete()

            await message.reply_text(
                "⚠️ Bad language detected!"
            )
            return

    # NSFW FILTER
    for word in NSFW_WORDS:

        if word in text:

            await message.delete()

            await message.reply_text(
                "🚫 NSFW content is not allowed!"
            )
            return

# =========================
# FLOOD PROTECTION
# =========================

@app.on_message(filters.group & filters.text)
async def anti_flood(_, message: Message):

    user_id = message.from_user.id

    if user_id not in MESSAGE_COUNT:
        MESSAGE_COUNT[user_id] = 0

    MESSAGE_COUNT[user_id] += 1

    if MESSAGE_COUNT[user_id] > 5:

        await message.reply_text(
            "⚠️ Stop spamming messages!"
        )

# =========================
# BOT START
# =========================

print("⚡ Xephiq Assistant Bot Running...")

app.run()
