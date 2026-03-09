import os
import asyncio
import requests
from pyrogram import Client, filters
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# এনভায়রনমেন্ট ভেরিয়েবল
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# রেন্ডার সার্ভারের জন্য পোর্ট লিসেনার (এটি গুরুত্বপূর্ণ)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("মিশন সফল! বট এখন ক্লাউড সার্ভারে সচল আছে। (০ এমবি খরচ)")

@app.on_message(filters.text & filters.private)
async def upload_file(client, message):
    url = message.text
    if not url.startswith("http"):
        return
        
    sent_msg = await message.reply_text("সার্ভারে প্রসেসিং হচ্ছে (আপনার ডাটা খরচ হবে না)...")
    
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

async def main():
    # হেলথ চেক সার্ভার শুরু করা
    threading.Thread(target=run_health_check, daemon=True).start()
    await app.start()
    print("বট সচল হয়েছে!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
