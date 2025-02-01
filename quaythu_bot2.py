import requests
import telebot

# Thay token bot Telegram của bạn
TELEGRAM_BOT_TOKEN = "7618979983:AAGDWrAVf6NgNkBTa7dS-kmH0k5BbWHhNw8"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Đọc danh sách tài khoản từ file
def load_accounts(file_path="ttc_accounts.txt"):
    accounts = []
    try:
        with open(file_path, "r") as file:
            for line in file.readlines():
                if line.strip():
                    username, password = line.strip().split("|")  # Sử dụng '|' làm ký tự phân cách
                    accounts.append((username, password))
    except FileNotFoundError:
        return accounts  # Trả về danh sách rỗng nếu file không tồn tại
    return accounts

# Ghi tài khoản mới vào file
def save_account(username, password, file_path="ttc_accounts.txt"):
    with open(file_path, "a") as file:
        file.write(f"{username}|{password}\n")

# API login TuongTacCheo
LOGIN_URL = "https://tuongtaccheo.com/login.php"

def login_ttc(username, password):
    """ Đăng nhập TuongTacCheo và lấy số dư """
    response = requests.post(LOGIN_URL, data={"username": username, "password": password})
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            balance = int(data["data"]["sodu"])  # Chuyển đổi sang int
            return username, balance
        else:
            return None, "Thông tin đăng nhập không đúng!"
    else:
        return None, "Lỗi kết nối API"

@bot.message_handler(commands=['check_balance'])
def handle_check_balance(message):
    chat_id = message.chat.id
    accounts = load_accounts()
    
    if not accounts:
        bot.send_message(chat_id, "⚠️ Không tìm thấy tài khoản nào trong file `ttc_accounts.txt`!")
        return
    
    total_balance = 0
    response_messages = []
    for username, password in accounts:
        user, balance_or_error = login_ttc(username, password)
        if user:
            response_messages.append(f"✅ Tài khoản: {user} | Số dư: {balance_or_error} xu")
            total_balance += balance_or_error  # Cộng dồn số dư
        else:
            response_messages.append(f"❌ {balance_or_error} với tài khoản {username}")

    # Tính số lượng theo dõi có thể mua được
    follow_cost = 1500  # Giá mỗi theo dõi
    if total_balance > 0:
        total_followers = total_balance // follow_cost
        response_messages.append(f"\nTổng số dư tất cả tài khoản: {total_balance} xu")
        response_messages.append(f"Số lượng theo dõi TikTok có thể mua: {total_followers} theo dõi")
    else:
        response_messages.append("\n⚠️ Tổng số dư không đủ để mua theo dõi TikTok!")

    bot.send_message(chat_id, "\n".join(response_messages))

@bot.message_handler(commands=['add_account'])
def handle_add_account(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Vui lòng nhập tài khoản theo định dạng: username|password")
    bot.register_next_step_handler(msg, process_new_account)

def process_new_account(message):
    chat_id = message.chat.id
    try:
        username, password = message.text.split("|")
        save_account(username.strip(), password.strip())  # Lưu tài khoản mới vào file
        bot.send_message(chat_id, f"✅ Tài khoản {username} đã được thêm thành công!")
    except ValueError:
        bot.send_message(chat_id, "❌ Định dạng không đúng! Vui lòng sử dụng: username|password")

# Chạy bot Telegram
bot.polling(none_stop=True)
