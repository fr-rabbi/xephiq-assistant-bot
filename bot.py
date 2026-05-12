from pyrogram import Client
from config import *

app = Client(
    "XephiqAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

print("⚡ Xephiq Assistant Running...")

app.run()
