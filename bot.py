import os
import asyncio
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# Render-এর জন্য ওয়েব সার্ভার
web_app = Flask('')
@web_app.route('/')
def home(): return "Bot is Alive!"
def run(): web_app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# Environment Variables থেকে ডাটা নেয়া
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('হাই! আমাকে ডাউনলোড লিংক দিন।')

@client.on(events.NewMessage)
async def handler(event):
    if event.text.startswith("http"):
        msg = await event.respond("ডাউনলোড শুরু হচ্ছে...")
        try:
            # সরাসরি ফাইল আপলোড (Telethon এটি খুব ভালো হ্যান্ডেল করে)
            await client.send_file(event.chat_id, event.text, caption="আপনার ফাইল")
            await msg.delete()
        except Exception as e:
            await msg.edit(f"এরর: {str(e)}")

if __name__ == "__main__":
    keep_alive()
    print("বোট চালু হয়েছে...")
    client.run_until_disconnected()
