const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Advanced Bot is Online!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf(process.env.BOT_TOKEN);

// লুপ এবং বারবার মেসেজ আসা বন্ধ করার জন্য
const processingUrls = new Set();

bot.start((ctx) => ctx.reply('আমি এখন আরও শক্তিশালী! যে কোনো মুভি বা ফাইল লিংক দিন, আমি সেটি ব্রাউজার হিসেবে ধরার চেষ্টা করব। 🔥'));

bot.on('text', async (ctx) => {
    const url = ctx.message.text;
    if (!url.startsWith('http')) return;

    if (processingUrls.has(url)) return;
    processingUrls.add(url);

    const statusMsg = await ctx.reply('লিংক যাচাই করা হচ্ছে... অনুগ্রহ করে ধৈর্য ধরুন। ⏳');

    try {
        await ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, 'সার্ভারের সাথে কানেক্ট করা হচ্ছে... ফাইলটি বড় হলে ৫-১০ মিনিট সময় লাগতে পারে। 📂');

        const response = await axios({
            method: 'get',
            url: url,
            responseType: 'stream',
            timeout: 0, 
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://google.com'
            }
        });

        // সরাসরি আপলোড শুরু
        await ctx.replyWithDocument({ 
            source: response.data, 
            filename: 'Bot_File_' + Date.now() + '.mkv' 
        });

        await ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, '✅ সফলভাবে আপলোড সম্পন্ন হয়েছে!');

    } catch (error) {
        console.log("Error:", error.message);
        let errorMsg = '❌ আপলোড ব্যর্থ হয়েছে!';
        if (error.response && error.response.status === 403) {
            errorMsg = '❌ এরর ৪০৩: ওয়েবসাইটটি বোটকে ব্লক করেছে। অন্য কোনো লিংক ট্রাই করুন।';
        } else {
            errorMsg = '❌ ফাইলটি অনেক বড় (২ জিবির বেশি) অথবা লিংকে সমস্যা আছে।';
        }
        await ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, errorMsg);
    } finally {
        processingUrls.delete(url);
    }
});

bot.catch((err) => console.error('Telegraf Error:', err));
bot.launch();
