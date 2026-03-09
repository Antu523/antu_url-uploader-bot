import os
import asyncio
import threading
import requests
from flask import Flask
from pyrogram import Client, filters, idle

# Render-এর জন্য হেলথ চেক সার্ভার (Flask)
web_app = Flask(__name__)
@web_app.route('/')
def home():
    return "Bot is Alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# টেলিগ্রাম বট কনফিগারেশন
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("মিশন সফল! বট এখন ক্লাউডে লাইভ আছে।")

@app.on_message(filters.text & filters.private)
async def upload_file(client, message):
    url = message.text
    if not url.startswith("http"): return
    
    sent_msg = await message.reply_text("ডাউনলোড হচ্ছে (আপনার ডাটা খরচ হবে না)...")
    try:
        file_name = url.split("/")[-1] or "file"
        r = requests.get(url, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        
        await sent_msg.edit("আপলোড হচ্ছে...")
        await message.reply_document(file_name)
        os.remove(file_name)
        await sent_msg.delete()
    except Exception as e:
        await sent_msg.edit(f"Error: {str(e)}")

async def main():
    # Flask সার্ভারকে আলাদা থ্রেডে চালানো
    threading.Thread(target=run_web, daemon=True).start()
    
    # বট শুরু করা
    await app.start()
    print("Bot is Live on Render!")
    await idle() # বটকে সচল রাখবে
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
