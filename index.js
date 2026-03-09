const { Telegraf } = require('telegraf');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot is Online!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => ctx.reply('স্বাগতম! আমাকে একটি সরাসরি ডাউনলোড লিংক দিন।'));

bot.on('text', async (ctx) => {
    const url = ctx.message.text;
    if (url.startsWith('http')) {
        try {
            await ctx.reply('প্রসেসিং হচ্ছে... বড় ফাইল হলে একটু সময় লাগতে পারে।');
            await ctx.replyWithDocument(url);
        } catch (error) {
            await ctx.reply('দুঃখিত, এই লিংকটি থেকে ফাইল আপলোড করা সম্ভব হয়নি।');
        }
    }
});

bot.launch();
console.log("বোট সচল আছে...");
