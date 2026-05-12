from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from bot import app
from config import FORCE_CHANNEL

async def subscribed(user_id):

    try:
        member = await app.get_chat_member(
            FORCE_CHANNEL,
            user_id
        )

        return member.status not in [
            "left",
            "kicked"
        ]

    except:
        return False


@app.on_message(filters.private & filters.command("start"))
async def start(_, message: Message):

    check = await subscribed(
        message.from_user.id
    )

    if not check:

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🚀 Join Xephiq",
                        url="https://t.me/Xephiq"
                    )
                ]
            ]
        )

        await message.reply_text(
            "⚠️ Join our channel first!",
            reply_markup=buttons
        )

        return

    await message.reply_text(
        "⚡ Welcome to Xephiq Assistant Bot 🚀"
  )
