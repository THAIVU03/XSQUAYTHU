import requests
import telebot
import re

# Thay token bot Telegram của bạn
TELEGRAM_BOT_TOKEN = "7618979983:AAGDWrAVf6NgNkBTa7dS-kmH0k5BbWHhNw8"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Danh sách Access Token của tài khoản TuongTacCheo
TTC_ACCOUNTS = [
    "05a5a8f5c5500958b7c1106fec81cc4b",
    "another_token_here",
    "another_token_here_2"
]

# API URL của TuongTacCheo
LOGIN_URL = "https://tuongtaccheo.com/logintoken.php"
BUY_FOLLOW_URL = "https://tuongtaccheo.com/api/buy.php"

def extract_tiktok_username(link):
    """Hàm lấy username từ link TikTok"""
    match = re.search(r'tiktok.com/@([\w\.\-]+)', link)
    return match.group(1) if match else None

@bot.message_handler(commands=['ttctt'])
def handle_ttctt(message):
    chat_id = message.chat.id
    parts = message.text.split()
    
    if len(parts) != 3:
        bot.send_message(chat_id, "⚠️ Sai cú pháp! Vui lòng nhập đúng định dạng:\n`/ttctt <link TikTok> <số lượng>`", parse_mode="Markdown")
        return

    tiktok_link = parts[1]
    try:
        follow_count = int(parts[2])
    except ValueError:
        bot.send_message(chat_id, "⚠️ Số lượng follow phải là số nguyên!")
        return
    
    tiktok_username = extract_tiktok_username(tiktok_link)
    
    if not tiktok_username:
        bot.send_message(chat_id, "⚠️ Không tìm thấy username trong link TikTok!")
        return

    bot.send_message(chat_id, f"🔄 Đang tìm tài khoản có đủ xu để mua {follow_count} follow cho @{tiktok_username}...")

    for token in TTC_ACCOUNTS:
        # Đăng nhập tài khoản TuongTacCheo
        login_response = requests.post(LOGIN_URL, data={"access_token": token})
        
        if login_response.status_code == 200 and login_response.json().get("status") == "success":
            user = login_response.json()["data"]["user"]
            sodu = int(login_response.json()["data"]["sodu"])  # Chuyển số dư thành số nguyên
            
            if sodu < (follow_count * 20):  # Giả sử 1 follow = 20 xu
                bot.send_message(chat_id, f"⚠️ Tài khoản {user} có {sodu} xu, không đủ để mua {follow_count} follow.")
                continue
            
            # Mua follow TikTok
            buy_response = requests.post(BUY_FOLLOW_URL, data={
                "access_token": token,
                "id": tiktok_username,
                "type": "follow",
                "soluong": follow_count
            })
            
            if buy_response.status_code == 200 and buy_response.json().get("status") == "success":
                bot.send_message(chat_id, f"✅ Tài khoản {user} ({sodu} xu) đã mua {follow_count} follow thành công cho @{tiktok_username}! 🎉")
                return  # Dừng vòng lặp sau khi mua thành công
            else:
                bot.send_message(chat_id, f"❌ Tài khoản {user} mua follow thất bại. Chuyển sang tài khoản khác...")
        else:
            bot.send_message(chat_id, f"⚠️ Đăng nhập thất bại với tài khoản {token[:5]}***")

    bot.send_message(chat_id, "❌ Không có tài khoản nào có đủ xu để mua follow TikTok!")

# Chạy bot Telegram
bot.polling(none_stop=True)
