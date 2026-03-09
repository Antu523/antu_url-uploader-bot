const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');
const contentDisposition = require('content-disposition');
const mime = require('mime-types');

const app = express();
app.get('/', (req, res) => res.send('Bot is Live!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => ctx.reply('আমি প্রস্তুত! যে কোনো লিংক দিন, আমি সেটি টেলিগ্রামে আপলোড করার চেষ্টা করব। 🔥'));

bot.on('text', async (ctx) => {
    const url = ctx.message.text;
    if (!url.startsWith('http')) return;

    const statusMsg = await ctx.reply('লিংক বিশ্লেষণ করা হচ্ছে... 🔍');

    try {
        const response = await axios({
            method: 'get',
            url: url,
            responseType: 'stream',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
            }
        });

        // ফাইলের নাম বের করার চেষ্টা
        let filename = 'file_' + Date.now();
        const cd = response.headers['content-disposition'];
        if (cd) {
            const parsed = contentDisposition.parse(cd);
            if (parsed.parameters.filename) filename = parsed.parameters.filename;
        } else {
            const contentType = response.headers['content-type'];
            const extension = mime.extension(contentType);
            if (extension) filename += `.${extension}`;
        }

        await ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, `ফাইল পাওয়া গেছে: ${filename}\nআপলোড শুরু হচ্ছে... 📤`);

        // টেলিগ্রামে আপলোড
        await ctx.replyWithDocument({ source: response.data, filename: filename });
        
        ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, '✅ আপলোড সফল হয়েছে!');

    } catch (error) {
        console.error(error);
        ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, '❌ এই লিংকটি কাজ করছে না। সার্ভার হয়তো বোটকে ব্লক করেছে।');
    }
});

bot.launch();
