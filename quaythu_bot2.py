import telebot
import random
import time
from datetime import datetime
from collections import defaultdict
import requests

TOKEN = '7618979983:AAGDWrAVf6NgNkBTa7dS-kmH0k5BbWHhNw8'
bot = telebot.TeleBot(TOKEN)

# Thêm API key cho ChatGPT
CHATGPT_API_KEY = 'sk-...zSMA'  # Thay thế bằng API key của bạn

def chatgpt_response(prompt):
    headers = {
        'Authorization': f'Bearer {CHATGPT_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo',  # Bạn có thể thay đổi model nếu cần
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 100,  # Số lượng token tối đa cho phản hồi
    }
    
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "❗ Đã xảy ra lỗi khi gọi API ChatGPT."

@bot.message_handler(commands=['chatgpt'])
def chatgpt_command(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    
    # Lấy câu hỏi từ tin nhắn
    question = message.text[len('/chatgpt '):].strip()  # Xóa lệnh khỏi câu hỏi
    if not question:
        bot.send_message(chat_id, "❗ Bạn chưa nhập câu hỏi. Hãy nhập theo cú pháp: /chatgpt [câu hỏi]")
        return
    
    # Gọi API ChatGPT để nhận phản hồi
    response = chatgpt_response(question)
    
    # Gửi phản hồi cho người dùng
    bot.send_message(chat_id, f"👤 <a href='tg://user?id={user_id}'>{user_name}</a>: {response}", parse_mode='HTML')

# Các lệnh khác của bot ...

@bot.polling()
