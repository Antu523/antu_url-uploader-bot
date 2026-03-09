const { Telegraf } = require('telegraf');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot is Online!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => ctx.reply('স্বাগতম! আমাকে সরাসরি ডাউনলোড লিংক দিন। আমি ব্রাউজার হেডার ব্যবহার করে ফাইল ধরার চেষ্টা করব।'));

bot.on('text', async (ctx) => {
    const url = ctx.message.text;
    if (url.startsWith('http')) {
        try {
            await ctx.reply('লিংকটি যাচাই করা হচ্ছে... বড় ফাইল হলে একটু সময় লাগতে পারে।');
            
            // হেডার্স ব্যবহার করে ফাইল পাঠানোর চেষ্টা
            await ctx.replyWithDocument({ 
                url: url,
                filename: 'Bot_File_' + Date.now() 
            }, {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                    'Referer': url,
                    'Accept': '*/*'
                }
            });

        } catch (error) {
            console.log("Error details:", error.message);
            await ctx.reply('দুঃখিত! এই লিংকটি কাজ করেনি।\n\nসম্ভাব্য কারণ:\n১. লিংকটি আপনার আইপি (IP) বা সেশনের সাথে লক করা।\n২. ফাইলের সাইজ ২ জিবির বেশি।\n৩. সার্ভার বোটের রিকোয়েস্ট ব্লক করে দিয়েছে।');
        }
    }
});

bot.launch();
console.log("বোট সচল আছে...");
