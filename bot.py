import os
import asyncio
from pyrogram import Client, filters
import requests

# এনভায়রনমেন্ট ভেরিয়েবল থেকে তথ্য নেওয়া
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("বট এখন ক্লাউড সার্ভারে সচল আছে! (০ এমবি খরচ)")

@app.on_message(filters.text & filters.private)
async def upload_file(client, message):
    url = message.text
    if not url.startswith("http"):
        return await message.reply_text("দয়া করে সঠিক ডাউনলোড লিঙ্ক দিন।")
        
    sent_msg = await message.reply_text("সার্ভারে ডাউনলোড হচ্ছে (আপনার ডাটা খরচ হবে না)...")
    
    try:
        file_name = url.split("/")[-1] or "file"
        r = requests.get(url, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        
        await sent_msg.edit("টেলিগ্রামে আপলোড হচ্ছে...")
        await message.reply_document(file_name)
        os.remove(file_name)
        await sent_msg.delete()
    except Exception as e:
        await sent_msg.edit(f"Error: {str(e)}")

# মেইন ফাংশন যা এরর হ্যান্ডেল করবে
async def main():
    await app.start()
    print("বট সচল হয়েছে!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
