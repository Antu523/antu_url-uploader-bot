import os
from flask import Flask
server = Flask(__name__)

@server.route("/")
def home():
    return "Bot is running!" os
import requests
from pyrogram import Client, filters

# আপনার তথ্য এখানে বসান
API_ID = 31866475  # নম্বরটি দিন, কোটেশন ছাড়া
API_HASH = "8406c1d6680cfdb39d588b1494a6a90a"
BOT_TOKEN = "8675890827:AAG2SV3eye90yknrF9v-kPEJaef8pS16NXY"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("বট সচল আছে! সরাসরি কোনো ফাইল লিংক দিন, আমি সেটি আপলোড করে দেব।")

@app.on_message(filters.text & filters.private)
async def upload_file(client, message):
    url = message.text
    if not url.startswith("http"):
        return await message.reply_text("দয়া করে একটি সঠিক URL দিন।")

    sent_msg = await message.reply_text("লিংকটি প্রসেস করা হচ্ছে...")
    
    try:
        # ফাইলের নাম বের করা
        file_name = url.split("/")[-1] or "downloaded_file"
        
        # ডাউনলোড শুরু
        await sent_msg.edit("ডাউনলোড শুরু হয়েছে...")
        r = requests.get(url, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # আপলোড শুরু
        await sent_msg.edit("ডাউনলোড শেষ! এখন টেলিগ্রামে আপলোড হচ্ছে...")
        await message.reply_document(file_name)
        
        # ফাইলটি ডিলিট করা
        os.remove(file_name)
        await sent_msg.delete()
        
    except Exception as e:
        await sent_msg.edit(f"দুঃখিত, কোনো সমস্যা হয়েছে: {str(e)}")

print("বটটি চালু হচ্ছে...")
import asyncio

# আগের সব কোড ঠিক থাকবে...

async def main():
    async with app:
        print("বটটি সফলভাবে চালু হয়েছে!")
        await asyncio.Event().wait()

if__name__== "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
if __name__ == "__main__":
    # পোর্ট সেট করা যাতে Render এটাকে সচল মনে করে
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
