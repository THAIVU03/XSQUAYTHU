import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Cấu hình logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Khóa API OpenAI
openai.api_key = 'sk-...zSMA'  # Thay thế bằng khóa API của bạn

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Chào bạn! Tôi là bot ChatGPT. Bạn có thể hỏi bất cứ điều gì!')

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response.choices[0].message.content
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text('Đã xảy ra lỗi. Vui lòng thử lại sau.')

if __name__ == '__main__':
    app = ApplicationBuilder().token('7618979983:AAGDWrAVf6NgNkBTa7dS-kmH0k5BbWHhNw8').build()  # Thay thế bằng token bot của bạn
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    
    app.run_polling()
