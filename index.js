const { Telegraf } = require('telegraf');
const express = require('express');
const axios = require('axios');

const app = express();
app.get('/', (req, res) => res.send('Progress Bot is Online!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.on('text', async (ctx) => {
    const url = ctx.message.text;
    if (!url.startsWith('http')) return;

    const statusMsg = await ctx.reply('ফাইল চেক করা হচ্ছে... ⏳');

    try {
        const response = await axios({
            method: 'get',
            url: url,
            responseType: 'stream',
            headers: { 'User-Agent': 'Mozilla/5.0' }
        });

        const totalLength = response.headers['content-length'];
        let downloadedLength = 0;
        let lastUpdate = 0;

        response.data.on('data', (chunk) => {
            downloadedLength += chunk.length;
            const progress = ((downloadedLength / totalLength) * 100).toFixed(2);
            const now = Date.now();

            // প্রতি ২ সেকেন্ড অন্তর প্রোগ্রেস আপডেট করবে (টেলিগ্রাম লিমিট এড়াতে)
            if (now - lastUpdate > 2000) {
                const progressBar = "▓".repeat(Math.floor(progress / 10)) + "░".repeat(10 - Math.floor(progress / 10));
                ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, 
                    `ডাউনলোড হচ্ছে...\n\n[${progressBar}] ${progress}%\nভায়া: Render Server`).catch(() => {});
                lastUpdate = now;
            }
        });

        await ctx.replyWithDocument({ source: response.data, filename: 'File_' + Date.now() });
        ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, '✅ আপলোড সম্পন্ন!');

    } catch (error) {
        ctx.telegram.editMessageText(ctx.chat.id, statusMsg.message_id, null, '❌ এই লিংক থেকে প্রোগ্রেস বার দেখানো সম্ভব নয়।');
    }
});

bot.launch();
