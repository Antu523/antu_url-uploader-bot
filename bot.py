import os
import time
import asyncio
import aiohttp
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message

# আপনার ক্রেডেনশিয়াল এখানে দিন
API_ID = "31866475"
API_HASH = "8406c1d6680cfdb39d588b1494a6a90a"
BOT_TOKEN = "8675890827:AAG2SV3eye90yknrF9v-kPEJaef8pS16NXY"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# প্রগ্রেস বার ফাংশন
async def progress_bar(current, total, message, start_time):
    now = time.time()
    diff = now - start_time
    if round(diff % 4.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        
        progress_str = f"[{'#' * int(percentage/10)}{'.' * (10 - int(percentage/10))}]"
        tmp = f"{progress_str} {round(percentage, 2)}%\n" \
              f"সম্পন্ন: {current // (1024*1024)}MB / {total // (1024*1024)}MB\n" \
              f"গতি: {speed // 1024:.2f} KB/s"
        
        try:
            await message.edit(tmp)
        except:
            pass

@app.on_message(filters.text & filters.private)
async def upload_link(client, message: Message):
    url = message.text
    if not url.startswith("http"):
        return

    status = await message.reply("লিংক প্রসেস করা হচ্ছে... ⏳")
    file_name = url.split("/")[-1] or "file.zip"

    try:
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                total_size = int(response.headers.get('content-length', 0))
                
                # ফাইল ডাউনলোড শুরু
                await status.edit("সার্ভারে ডাউনলোড হচ্ছে... 📥")
                async with aiofiles.open(file_name, mode='wb') as f:
                    downloaded = 0
                    async for chunk in response.content.iter_chunked(1024 * 1024):
                        await f.write(chunk)
                        downloaded += len(chunk)
                        await progress_bar(downloaded, total_size, status, start_time)

        # ফাইল আপলোড শুরু
        await status.edit("টেলিগ্রামে আপলোড হচ্ছে... 📤")
        up_start = time.time()
        await message.reply_document(
            document=file_name,
            progress=progress_bar,
            progress_args=(status, up_start)
        )
        
        await status.delete()
        os.remove(file_name) # স্টোরেজ খালি করতে ডিলিট

    except Exception as e:
        await status.edit(f"দুঃখিত, এরর হয়েছে: {str(e)}")
        if os.path.exists(file_name):
            os.remove(file_name)

print("বোটটি সচল আছে...")
app.run()
from flask import Flask
from threading import Thread

# ওয়েব সার্ভার তৈরি
web_app = Flask('')

@web_app.route('/')
def home():
    return "বোট সচল আছে!"

def run():
    web_app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# আপনার মূল কোডের app.run() এর ঠিক আগে keep_alive() কল করুন
if __name__ == "__main__":
    keep_alive()
    app.run()
