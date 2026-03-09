import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters

# ১. রেন্ডারের পোর্ট বাইন্ডিংয়ের জন্য ফ্লস্ক সার্ভার
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Running!", 200

def run_flask():
    # রেন্ডার অটোমেটিক একটি PORT এনভায়রনমেন্ট ভ্যারিয়েবল দেয়
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# ২. টেলিগ্রাম বট কনফিগারেশন
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("বট সচল আছে!")

# ৩. মেইন রানার
async def main():
    # ফ্লস্ককে আলাদা থ্রেডে চালানো যেন রেন্ডার পোর্ট খুঁজে পায়
    threading.Thread(target=run_flask, daemon=True).start()
    
    await app.start()
    print("Bot is Live!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
