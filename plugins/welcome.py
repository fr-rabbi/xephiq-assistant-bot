from pyrogram import filters
from pyrogram.types import Message
from bot import app


@app.on_message(filters.new_chat_members)
async def welcome(_, message: Message):

    for user in message.new_chat_members:

        text = (
            f"⚡ Welcome {user.mention}!\n\n"
            "🚀 Official Channel: @Xephiq\n"
            "🤖 Assistant: @XephiqAssistantBot"
        )

        await message.reply_text(text)
