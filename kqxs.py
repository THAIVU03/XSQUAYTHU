import telebot
import requests

TOKEN = '7618979983:AAGDWrAVf6NgNkBTa7dS-kmH0k5BbWHhNw8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['sxmb'])
def sxmb(message):
    api_url = 'https://nguyenmanh.name.vn/api/xsmb?apikey=OUEaxPOl'
    response = requests.get(api_url)
    data = response.json()
    
    if data['status'] == 200:
        result = data['result']
        bot.reply_to(message, f'<blockquote>{result}</blockquote>', parse_mode='HTML')
    else:
        bot.reply_to(message, 'Lỗi khi lấy kết quả xổ số.')

bot.polling()