const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot is Live!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf(process.env.BOT_TOKEN);

// লুপ বন্ধ করার জন্য একটি প্রসেসিং হ্যান্ডলার
const processingUrls = new Set();

bot.on('text', async (ctx) => {
    const url = ctx.message.text;
    if (!url.startsWith('http')) return;

    // যদি এই ইউআরএলটি অলরেডি প্রসেসিং থাকে, তবে ইগনোর করবে
    if (processingUrls.has(url)) return;
    processingUrls.add(url);

    const statusMsg = await ctx.reply('প্রসেসিং শুরু হয়েছে... অনুগ্রহ করে অপেক্ষা করুন। একই লিংক বারবার দেবেন না। ⏳');

    try {
        const response = await axios({
            method: 'get',
            url: url,
            responseType: 'stream',
            timeout: 0, // টাইমআউট বন্ধ করা
            headers: { 'User-Agent': 'Mozilla/5.0' }
        });

        await ctx.replyWithDocument({ source: response.data, filename: 'Movie_' + Date.now() + '.mkv' });
        await ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, '✅ সফলভাবে আপলোড হয়েছে!');

    } catch (error) {
        console.log("Error:", error.message);
        await ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, '❌ আপলোড ব্যর্থ! ফাইলটি হয়তো অনেক বড় বা লিংকটি কাজ করছে না।');
    } finally {
        // প্রসেসিং শেষ হলে লিস্ট থেকে মুছে ফেলবে
        processingUrls.delete(url);
    }
});

// এরর হ্যান্ডলার যোগ করা যাতে বোট ক্র্যাশ না করে
bot.catch((err) => {
    console.log('Telegraf error', err);
});

bot.launch();
