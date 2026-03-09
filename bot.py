import os
import asyncio
import requests
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# ১. রেন্ডারের পোর্ট চেক পাস করার জন্য ফ্লস্ক সার্ভার
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Running!", 200

def run_flask():
    # রেন্ডার থেকে পোর্ট নিয়ে সার্ভার চালু করা
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# ২. টেলিগ্রাম বট কনফিগারেশন
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("অভিনন্দন! আপনার বট এখন ক্লাউড সার্ভারে সচল আছে।")

@app.on_message(filters.text & filters.private)
async def upload_file(client, message):
    url = message.text
    if not url.startswith("http"): return
    
    sent_msg = await message.reply_text("ক্লাউড সার্ভারে ডাউনলোড হচ্ছে (আপনার ডাটা খরচ হবে না)...")
    try:
        file_name = url.split("/")[-1] or "file"
        r = requests.get(url, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        
        await sent_msg.edit("টেলিগ্রামে আপলোড হচ্ছে...")
        await message.reply_document(file_name)
        os.remove(file_name)
        await sent_msg.delete()
    except Exception as e:
        await sent_msg.edit(f"Error: {str(e)}")

# ৩. মেইন ফাংশন যা সবকিছু কন্ট্রোল করবে
async def main():
    # ফ্লস্ক সার্ভারকে আলাদা থ্রেডে চালু করা
    Thread(target=run_flask).start()
    
    # বট শুরু করা
    await app.start()
    print("Bot is Live!")
    
    # বটকে স্থায়ীভাবে সচল রাখা
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Python ৩.১০+ এর জন্য স্ট্যান্ডার্ড রান পদ্ধতি
    asyncio.run(main())
