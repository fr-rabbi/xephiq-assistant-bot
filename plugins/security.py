from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from bot import app
import re

MESSAGE_COUNT = {}

LINK_KEYWORDS = [
    "http",
    "https",
    "www.",
    ".com",
    ".net",
    "t.me/",
    "telegram.me",
    "discord.gg",
    "youtube.com"
]

BAD_WORDS = [
    "porn",
    "sex",
    "nude",
    "fuck",
    "bitch",
    "xxx",
    "চোদা",
    "মাগি"
]

ALLOWED_MENTIONS = [
    "@xephiq",
    "@xephiqcommunity",
    "@xephiqassistantbot"
]


@app.on_message(filters.group & filters.text)
async def security(_, message: Message):

    if not message.from_user:
        return

    member = await app.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status in [
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    ]:
        return

    text = message.text.lower()

    for word in LINK_KEYWORDS:

        if word in text:

            await message.delete()

            await message.reply_text(
                "🚫 Links are not allowed!"
            )

            return

    pattern = r"(?:\+88|88)?01[3-9]\d{8}"

    if re.search(pattern, text):

        await message.delete()

        await message.reply_text(
            "🚫 Phone numbers are not allowed!"
        )

        return

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

    for word in BAD_WORDS:

        if word in text:

            await message.delete()

            await message.reply_text(
                "⚠️ Restricted content detected!"
            )

            return

    user_id = message.from_user.id

    if user_id not in MESSAGE_COUNT:
        MESSAGE_COUNT[user_id] = 0

    MESSAGE_COUNT[user_id] += 1

    if MESSAGE_COUNT[user_id] > 5:

        await message.reply_text(
            "⚠️ Stop spamming!"
)
