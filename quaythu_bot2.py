import requests
import telebot

# Thay token bot Telegram của bạn
TELEGRAM_BOT_TOKEN = "7618979983:AAGDWrAVf6NgNkBTa7dS-kmH0k5BbWHhNw8"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Đọc danh sách token từ file
def load_tokens(file_path="ttc_accounts.txt"):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# API login TuongTacCheo
LOGIN_URL = "https://tuongtaccheo.com/logintoken.php"

def login_ttc(access_token):
    """ Đăng nhập TuongTacCheo và lấy số dư """
    response = requests.post(LOGIN_URL, data={"access_token": access_token})
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            user = data["data"]["user"]
            balance = data["data"]["sodu"]
            return user, balance
        else:
            return None, "Token lỗi!"
    else:
        return None, "Lỗi kết nối API"

@bot.message_handler(commands=['check_balance'])
def handle_check_balance(message):
    chat_id = message.chat.id
    tokens = load_tokens()
    
    if not tokens:
        bot.send_message(chat_id, "⚠️ Không tìm thấy token nào trong file `ttc_accounts.txt`!")
        return
    
    response_messages = []
    for token in tokens:
        user, balance_or_error = login_ttc(token)
        if user:
            response_messages.append(f"✅ Tài khoản: {user} | Số dư: {balance_or_error} xu")
        else:
            response_messages.append(f"❌ {balance_or_error} với token {token[:5]}***")

    bot.send_message(chat_id, "\n".join(response_messages))

# Chạy bot Telegram
bot.polling(none_stop=True)
