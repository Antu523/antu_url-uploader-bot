const { Telegraf } = require('telegraf');
const express = require('express');

// Render-এর জন্য ছোট ওয়েব সার্ভার
const app = express();
app.get('/', (req, res) => res.send('Bot is Alive!'));
app.listen(process.env.PORT || 8080);

// Environment Variables থেকে টোকেন নেওয়া
const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => ctx.reply('হাই! আমাকে সরাসরি ডাউনলোড লিংক দিন।'));

bot.on('text', async (ctx) => {
    const url = ctx.message.text;
    if (url.startsWith('http')) {
        try {
            await ctx.reply('ফাইলটি টেলিগ্রামে পাঠানো হচ্ছে...');
            await ctx.replyWithDocument(url);
        } catch (error) {
            await ctx.reply('এরর: ফাইলটি পাঠানো সম্ভব হয়নি। সরাসরি ডাউনলোড লিংক ব্যবহার করুন।');
        }
    }
});

bot.launch();
console.log("বোট চালু হয়েছে...");
