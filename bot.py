import os
import requests
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("বট ক্লাউড সার্ভারে চালু হয়েছে!")

@app.on_message(filters.text & filters.private)
async def upload_file(client, message):
    url = message.text
    sent_msg = await message.reply_text("সার্ভারে ডাউনলোড হচ্ছে (০ এমবি খরচ)...")
    
    file_name = url.split("/")[-1] or "file"
    r = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(r.content)
        
    await sent_msg.edit("টেলিগ্রামে আপলোড হচ্ছে...")
    await message.reply_document(file_name)
    os.remove(file_name)
    await sent_msg.delete()

app.run()
