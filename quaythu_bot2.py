import logging
import random
import os
import time
import json
import ast
import string
import datetime
import requests
import math
from decimal import Decimal
from threading import Thread
from telegram import ChatAction
from bs4 import BeautifulSoup
from functools import wraps
from collections import deque
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler,ConversationHandler
from telegram import InputMediaAnimation
from telegram import ChatPermissions
from telegram import ParseMode
from telegram import User
from telegram.error import NetworkError, TelegramError
import threading
import pyfiglet
from colorama import Fore, Style, init

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

init(autoreset=True)

SICBO_GROUP_ID = -1002172465603
TAIXIU_GROUP_ID = -1002178971014
CHECKBB_FILE = "checkbb.txt"
groups_info = {}
joined_groups = {}
VIETTEL, VINAPHONE, MOBIPHONE, VIETNAMOBILE = range(4)
MENH_GIA = ["10000", "20000", "30000", "50000", "100000", "200000", "500000"]
mophien = True
inf_balance_user = {}
pending_transactions = {}
MAX_JACKPOT_AMOUNT = 1000000000000000000
huloc_default_amount = 10000000000000000
huloc_amount = 0
lottery_active = False
lottery_tickets = {}
lottery_timer = 0
taixiu_game_active = False
end_game_requested = False
taixiu_bets = {}
taixiu_result = None
jackpot = 0
jackpot_amount = 1000000000000000000
taixiu_timer = 0
recent_results = []
betting_time = 30
betting_timer = betting_time
aviator_lock = threading.Lock()
aviator_game_active = False
aviator_bets = {}
aviator_multiplier = 1.0
banned_groups = []
ket_balance = {}
banned_users = []
chat_id = -1002066327546
betting_records = {}
user_daily_claim = {}
MIN_DAILY_AMOUNT = 1000
MAX_DAILY_AMOUNT = 5000
user_balances = {}
winners = []
codes = {}
rooms = {}
user_code_usage = {}
DAILY_FILE_PATH = "daily.txt"
sodu_file_path = "sodu.txt"
codes_file_path = "code.txt"
user_code_usage_file = "user_code_usage.json"
TOKEN = "7618979983:AAGDWrAVf6NgNkBTa7dS-kmH0k5BbWHhNw8"
transaction_history_file = "transaction_history.json"
end_game_requested = False
xocdia_game_active = False
xocdia_bets = {}
xocdia_timer = 30
xocdia_result = None
horse_race_active = False
horse_race_bets = {}
horse_race_timer = 30
horse_race_results = []
admin_ids = 6793700101
ADMIN_IDS = 6793700101
admin_id = 6793700101
ADMIN_ID = 6793700101
authorized_users = 6793700101,5610191483,6496681221,6496681221,6755605749,6401417058,6022788354,6951810527,5777678653,6800698223,6272709789,5503054780
sicbo_game_active = False
sicbo_bets = {}
sicbo_timer = 0
GROUP_CHAT_ID = -1002481346270
VERIFIED_USERS_FILE = 'ver_rut.txt'
num_rounds = {}
with open("admin.txt", "w") as admin_file:
    admin_file.write(json.dumps(admin_id))
bet_types = {
    'T': {'name': 'Tài', 'multiplier': 2, 'condition': lambda total: 11 <= total <= 18},
    'X': {'name': 'Xỉu', 'multiplier': 2, 'condition': lambda total: 3 <= total <= 10},
    'L': {'name': 'Lẻ', 'multiplier': 2, 'condition': lambda total: total % 2 == 1},
    'C': {'name': 'Chẵn', 'multiplier': 2, 'condition': lambda total: total % 2 == 0},
    'D1': {'name': '2 Con 1', 'multiplier': 15, 'condition': lambda dice: dice.count(1) == 2},
    'D2': {'name': '2 Con 2', 'multiplier': 15, 'condition': lambda dice: dice.count(2) == 2},
    'D3': {'name': '2 Con 3', 'multiplier': 15, 'condition': lambda dice: dice.count(3) == 2},
    'D4': {'name': '2 Con 4', 'multiplier': 15, 'condition': lambda dice: dice.count(4) == 2},
    'D5': {'name': '2 Con 5', 'multiplier': 15, 'condition': lambda dice: dice.count(5) == 2},
    'D6': {'name': '2 Con 6', 'multiplier': 15, 'condition': lambda dice: dice.count(6) == 2},
    'BBK': {'name': 'Bão Bất Kỳ', 'multiplier': 31, 'condition': lambda dice: len(set(dice)) == 1},
    'B1': {'name': '3 Con 1', 'multiplier': 200, 'condition': lambda dice: dice == [1, 1, 1]},
    'B2': {'name': '3 Con 2', 'multiplier': 200, 'condition': lambda dice: dice == [2, 2, 2]},
    'B3': {'name': '3 Con 3', 'multiplier': 200, 'condition': lambda dice: dice == [3, 3, 3]},
    'B4': {'name': '3 Con 4', 'multiplier': 200, 'condition': lambda dice: dice == [4, 4, 4]},
    'B5': {'name': '3 Con 5', 'multiplier': 200, 'condition': lambda dice: dice == [5, 5, 5]},
    'B6': {'name': '3 Con 6', 'multiplier': 200, 'condition': lambda dice: dice == [6, 6, 6]},
    '4': {'name': 'Xúc xắc 4', 'multiplier': 66, 'condition': lambda total: total == 4},
    '5': {'name': 'Xúc xắc 5', 'multiplier': 33, 'condition': lambda total: total == 5},
    '6': {'name': 'Xúc xắc 6', 'multiplier': 21, 'condition': lambda total: total == 6},
    '7': {'name': 'Xúc xắc 7', 'multiplier': 14, 'condition': lambda total: total == 7},
    '8': {'name': 'Xúc xắc 8', 'multiplier': 10, 'condition': lambda total: total == 8},
    '9': {'name': 'Xúc xắc 9', 'multiplier': 8, 'condition': lambda total: total == 9},
    '10': {'name': 'Xúc xắc 10', 'multiplier': 7, 'condition': lambda total: total == 10},
    '11': {'name': 'Xúc xắc 11', 'multiplier': 7, 'condition': lambda total: total == 11},
    '12': {'name': 'Xúc xắc 12', 'multiplier': 8, 'condition': lambda total: total == 12},
    '13': {'name': 'Xúc xắc 13', 'multiplier': 10, 'condition': lambda total: total == 13},
    '14': {'name': 'Xúc xắc 14', 'multiplier': 14, 'condition': lambda total: total == 14},
    '15': {'name': 'Xúc xắc 15', 'multiplier': 21, 'condition': lambda total: total == 15},
    '16': {'name': 'Xúc xắc 16', 'multiplier': 33, 'condition': lambda total: total == 16},
    '17': {'name': 'Xúc xắc 17', 'multiplier': 66, 'condition': lambda total: total == 17},
    'P12': {'name': 'Xúc xắc 1 và 2', 'multiplier': 7, 'condition': lambda dice: dice.count(1) == 2 and dice.count(2) == 1},
    'P13': {'name': 'Xúc xắc 1 và 3', 'multiplier': 7, 'condition': lambda dice: dice.count(1) == 2 and dice.count(3) == 1},
    'P14': {'name': 'Xúc xắc 1 và 4', 'multiplier': 7, 'condition': lambda dice: dice.count(1) == 2 and dice.count(4) == 1},
    'P15': {'name': 'Xúc xắc 1 và 5', 'multiplier': 7, 'condition': lambda dice: dice.count(1) == 2 and dice.count(5) == 1},
    'P16': {'name': 'Xúc xắc 1 và 6', 'multiplier': 7, 'condition': lambda dice: dice.count(1) == 2 and dice.count(6) == 1},
    'P23': {'name': 'Xúc xắc 2 và 3', 'multiplier': 7, 'condition': lambda dice: dice.count(2) == 2 and dice.count(3) == 1},
    'P24': {'name': 'Xúc xắc 2 và 4', 'multiplier': 7, 'condition': lambda dice: dice.count(2) == 2 and dice.count(4) == 1},
    'P25': {'name': 'Xúc xắc 2 và 5', 'multiplier': 7, 'condition': lambda dice: dice.count(2) == 2 and dice.count(5) == 1},
    'P26': {'name': 'Xúc xắc 2 và 6', 'multiplier': 7, 'condition': lambda dice: dice.count(2) == 2 and dice.count(6) == 1},
    'P34': {'name': 'Xúc xắc 3 và 4', 'multiplier': 7, 'condition': lambda dice: dice.count(3) == 2 and dice.count(4) == 1},
    'P35': {'name': 'Xúc xắc 3 và 5', 'multiplier': 7, 'condition': lambda dice: dice.count(3) == 2 and dice.count(5) == 1},
    'P36': {'name': 'Xúc xắc 3 và 6', 'multiplier': 7, 'condition': lambda dice: dice.count(3) == 2 and dice.count(6) == 1},
    'P45': {'name': 'Xúc xắc 4 và 5', 'multiplier': 7, 'condition': lambda dice: dice.count(4) == 2 and dice.count(5) == 1},
    'P46': {'name': 'Xúc xắc 4 và 6', 'multiplier': 7, 'condition': lambda dice: dice.count(4) == 2 and dice.count(6) == 1},
    'P56': {'name': 'Xúc xắc 5 và 6', 'multiplier': 7, 'condition': lambda dice: dice.count(5) == 2 and dice.count(6) == 1},
    'S1': {'name': 'Xúc xắc 1', 'multiplier': 2, 'condition': lambda dice: 1 in dice},
    'S2': {'name': 'Xúc xắc 2', 'multiplier': 2, 'condition': lambda dice: 2 in dice},
    'S3': {'name': 'Xúc xắc 3', 'multiplier': 2, 'condition': lambda dice: 3 in dice},
    'S4': {'name': 'Xúc xắc 4', 'multiplier': 2, 'condition': lambda dice: 4 in dice},
    'S5': {'name': 'Xúc xắc 5', 'multiplier': 2, 'condition': lambda dice: 5 in dice},
    'S6': {'name': 'Xúc xắc 6', 'multiplier': 2, 'condition': lambda dice: 6 in dice},
    }

def retry_on_failure(retries=3, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except NetworkError as e:
                    print(f"Xảy ra lỗi mạng: {e}. Thử lại sau {delay} giây...")
                    time.sleep(delay)
                except TelegramError as e:
                    print(f"Xảy ra lỗi Telegram: {e}")
                    break  
            return None
        return wrapper
    return decorator
def restrict_room(func):
    @wraps(func)
    def wrapper(update, context):
        if update.message.chat_id == -1002178971014:
            update.message.reply_text(
                "Đây Không Phải Là 1 Lệnh Có Thể Sài Trong Room\n\nSử dụng mọi lệnh tại\n👉 t.me/ztrongzgroup 👈"
            )
        else:
            return func(update, context)
    return wrapper


def lock_chat(context, chat_id):
    context.bot.set_chat_permissions(
        chat_id=chat_id,
        permissions=ChatPermissions(
            can_send_messages=False
        )
    )

def unlock_chat(context, chat_id):
    context.bot.set_chat_permissions(
        chat_id=chat_id,
        permissions=ChatPermissions(
            can_send_messages=True
        )
    )
def add_admin(update, context):
    if update.message.from_user.id != 6793700101:
        update.message.reply_text("Only the main admin can add other admins.")
        return
    args = context.args
    if len(args) != 1:
        update.message.reply_text("Usage: /themad <admin_id>")
        return
    try:
        new_admin_id = int(args[0])
        all_admin_ids.append(new_admin_id)
        with open("admin.txt", "w") as admin_file:
            admin_file.write(json.dumps(all_admin_ids))
        update.message.reply_text("Admin added successfully.")
    except ValueError:
        update.message.reply_text("Invalid admin ID.")

def remove_admin(update, context):
    if update.message.from_user.id != 6793700101:
        update.message.reply_text("Only the main admin can remove other admins.")
        return
    args = context.args
    if len(args) != 1:
        update.message.reply_text("Usage: /xoaad <admin_id>")
        return
    try:
        remove_admin_id = int(args[0])
        if remove_admin_id not in all_admin_ids:
            update.message.reply_text("This user is not an admin.")
            return
        all_admin_ids.remove(remove_admin_id)
        with open("admin.txt", "w") as admin_file:
            admin_file.write(json.dumps(all_admin_ids))
        update.message.reply_text("Admin removed successfully.")
    except ValueError:
        update.message.reply_text("Invalid admin ID.")

@restrict_room
def start_horse_race(update, context):
    global horse_race_active, horse_race_bets, horse_race_timer

    if horse_race_active:
        update.message.reply_text("Trò chơi Đua Ngựa đang diễn ra! Vui lòng đợi đến khi kết thúc để tham gia.")
        return

    horse_race_active = True
    horse_race_bets = {}
    horse_race_timer = 30

    update.message.reply_text(
        "🏇 Trò chơi Đua Ngựa đã bắt đầu! 🏇\n\n"
        "Lệnh cược: /h <số tiền cược hoặc 'all'> <con chọn>\n\n"
        "Các con ngựa:\n"
        "1 - Ngựa 1\n"
        "2 - Ngựa 2\n"
        "3 - Ngựa 3\n"
        "4 - Ngựa 4\n"
        "5 - Ngựa 5\n\n"
        f"⏳ Còn {horse_race_timer} giây để đặt cược ⏳")

    threading.Thread(target=start_horse_race_timer, args=(update, context)).start()
def start_horse_race_timer(update, context):
    global horse_race_timer

    while horse_race_timer > 0:
        time.sleep(1)
        horse_race_timer -= 1
        if horse_race_timer % 10 == 0:
            update.message.reply_text(f"⏳ Còn {horse_race_timer} giây để đặt cược ⏳")

    update.message.reply_text("⏳ Hết thời gian đặt cược! ⏳")
    generate_horse_race_result(update, context)
def place_horse_bet(update, context):
    global horse_race_bets, horse_race_active, horse_race_timer

    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return

    if not horse_race_active:
        update.message.reply_text("Hiện không có trò chơi Đua Ngựa nào đang diễn ra.")
        return

    args = context.args
    if len(args) != 2:
        update.message.reply_text("Sử dụng: /h <số tiền cược hoặc 'all'> <con chọn>")
        return

    try:
        bet_amount = int(args[0]) if args[0].lower() != 'all' else user_balances.get(user_id, 0)
        horse_choice = int(args[1])
    except ValueError:
        update.message.reply_text("Số tiền cược phải là một số nguyên hoặc 'all' và con chọn phải là số từ 1 đến 5.")
        return

    if bet_amount <= 0 or horse_choice not in range(1, 6):
        update.message.reply_text("Số tiền cược hoặc con chọn không hợp lệ.")
        return

    if user_balances.get(user_id, 0) < bet_amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    if horse_race_timer == 0:
        update.message.reply_text("Hết thời gian đặt cược. Vui lòng chờ đợi kết quả.")
        return

    if user_id not in horse_race_bets:
        horse_race_bets[user_id] = []

    horse_race_bets[user_id].append((horse_choice, bet_amount))
    update.message.reply_text(f"Bạn đã đặt cược {format_currency(bet_amount)} vào con ngựa {horse_choice}!")

    user_balances[user_id] -= bet_amount
def generate_horse_race_result(update, context):
    global horse_race_active, horse_race_bets, horse_race_results

    if not horse_race_active:
        update.message.reply_text("Hiện không có trò chơi Đua Ngựa nào đang diễn ra.")
        return

    horse_race_active = False

    horse_race_results = random.sample(range(1, 6), 5)
    winner = horse_race_results[0]

    update.message.reply_text("‼️ Kết quả đua ngựa ‼️")
    time.sleep(2)
    update.message.reply_text(f"💢 TOP 5 💢 : Ngựa {horse_race_results[4]}")
    update.message.reply_text(f"💢 TOP 4 💢 : Ngựa {horse_race_results[3]}")
    time.sleep(1)
    update.message.reply_text(f"‼️ GIỜ LÀ ĐẾN CÁC TOP ‼️")
    time.sleep(1)
    update.message.reply_text(f"🏆 TOP 3 🏆 : Ngựa {horse_race_results[2]}")
    update.message.reply_text(f"🏆 TOP 2 🏆 : Ngựa {horse_race_results[1]}")
    update.message.reply_text(f"🏆 TOP 1 🏆 : Ngựa {horse_race_results[0]}")

    winners = {}
    for user_id, bets in horse_race_bets.items():
        user_total_winnings = 0
        for choice, amount in bets:
            if choice == horse_race_results[0]:
                user_total_winnings += amount * 5
            elif choice == horse_race_results[1]:
                user_total_winnings += amount * 1
            elif choice == horse_race_results[2]:
                user_total_winnings -= amount * 0.5

        if user_total_winnings != 0:
            winners[user_id] = user_total_winnings

    result_message = "🎮 Kết quả cược 🎮 :\n\n"
    if len(winners) == 0:
        result_message += "Không có người chơi nào thắng cược!"
    else:
        result_message += "Người chơi - Tiền thắng\n"
        for user_id, amount_won in winners.items():
            update_user_balance(user_id, amount_won)
            result_message += f"{user_id} - {format_currency(amount_won)}\n"

    update.message.reply_text(result_message)
    horse_race_bets.clear()
def bang_gia_xu(update, context):
    gia_xu = [
        (10000, 750),
        (20000, 2000),
        (50000, 3500),
        (100000, 7000),
        (200000, 14000)
    ]
    message = "💰 **Bảng Giá Xu** 💰\n\n"
    for gia, xu in gia_xu:
        message += f"{format_currency(gia)} = {xu} MB\n"
    return message

@restrict_room
def nap(update, context):
    user_id = update.message.from_user.id
    account_info = (
        "💳 **Số Tài Khoản**: 0909743280\n"
        "👤 **Chủ Tài Khoản**: LÊ PHƯỚC TRỌNG\n"
        "🏦 **Ngân Hàng**: MOMO BANKING\n"
        f"📄 **Nội Dung**: {user_id}\n"
        "‼️ Vui lòng chuyển > 10,000đ để nạp ‼️"
    )

    bang_gia = bang_gia_xu(update, context)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=account_info + "\n\n" + bang_gia,
        parse_mode="Markdown"
    )
def fix_user_balance():
    global user_balances
    for user_id in user_balances:
        if isinstance(user_balances[user_id], float):
            user_balances[user_id] = int(user_balances[user_id])
            print(
                f"Số dư của người dùng {user_id} đã được chỉnh về số nguyên: {user_balances[user_id]}"
            )

@restrict_room
def start_xocdia(update, context):
    global xocdia_game_active, xocdia_bets, xocdia_timer

    if xocdia_game_active:
        update.message.reply_text(
            "Trò chơi Xóc Đĩa đang diễn ra! Vui lòng đợi đến khi kết thúc để tham gia."
        )
        return

    xocdia_game_active = True
    xocdia_bets = {}
    xocdia_timer = 30

    update.message.reply_text(
        "⚪️⚫️ Trò chơi Xóc Đĩa đã bắt đầu! ⚪️⚫️\n\n"
        "Lệnh cược: /xocdia <Cửa chọn> <Cược hoặc 'all'>\n\n"
        "Các cửa cược:\n"
        "- L : Lẻ (1:2) ⚪️⚪️⚪️⚫️ / ⚫️⚫️⚫️⚪️\n\n"
        "- C : Chẵn (1:2) ⚪️⚫️⚪️⚫️\n\n"
        "- 3T : Lẻ 3 trắng (1:4) ⚪️⚪️⚪️⚫️\n\n"
        "- 3D : Lẻ 3 đen (1:4) ⚫️⚫️⚫️⚪️\n\n"
        "- 4T : Tứ trắng (1:16) ⚪️⚪️⚪️⚪️\n\n"
        "- 4D : Tứ đen (1:16) ⚫️⚫️⚫️⚫️\n\n"
        f"⏳ Còn {xocdia_timer} giây để đặt cược ⏳")

    threading.Thread(target=start_xocdia_timer, args=(update, context)).start()

@restrict_room
def giaxu(update, context):
    update.message.reply_text("Nhắn /nap Có Tổng Hợp Giá Xu")

@restrict_room
def start_xocdia_timer(update, context):
    global xocdia_timer

    while xocdia_timer > 0:
        time.sleep(1)
        xocdia_timer -= 1
        if xocdia_timer % 10 == 0:
            update.message.reply_text(
                f"⏳ Còn {xocdia_timer} giây để đặt cược ⏳")

    update.message.reply_text("⏳ Hết thời gian đặt cược! ⏳")
    generate_xocdia_result(update, context)

@restrict_room
def xocdia(update, context):
    global xocdia_game_active, xocdia_timer, xocdia_bets

    if not xocdia_game_active:
        update.message.reply_text(
            "Hiện không có trò chơi Xóc Đĩa nào đang diễn ra.")
        return

    args = context.args
    if len(args) != 2:
        update.message.reply_text(
            "Sử dụng: /xocdia <Cửa chọn> <Cược hoặc 'all'>")
        return

    bet_option = args[0].upper()
    bet_amount = 0
    if args[1].lower() == 'all':
        bet_amount = user_balances.get(user_id, 0)
    else:
        try:
            bet_amount = int(args[1])
        except ValueError:
            update.message.reply_text(
                "Số tiền cược phải là một số nguyên hoặc 'all'.")
            return

    user_id = update.message.from_user.id
    if user_balances.get(user_id, 0) < bet_amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    if xocdia_timer == 0:
        update.message.reply_text(
            "Hết thời gian đặt cược. Vui lòng chờ đợi kết quả.")
        return

    valid_options = ['L', 'C', '3T', '3D', '4T', '4D']
    if bet_option not in valid_options:
        update.message.reply_text("Lựa chọn cửa không hợp lệ.")
        return

    if user_id not in xocdia_bets:
        xocdia_bets[user_id] = []

    xocdia_bets[user_id].append((bet_option, bet_amount))
    update.message.reply_text(
        f"Bạn đã đặt cược {format_currency(bet_amount)} vào cửa {bet_option}!")

    user_balances[user_id] -= bet_amount
def generate_xocdia_result(update, context):
    global xocdia_game_active, xocdia_result, xocdia_bets

    if not xocdia_game_active:
        update.message.reply_text(
            "Hiện không có trò chơi Xóc Đĩa nào đang diễn ra.")
        return

    result_option = random.choice(['L', 'C', '3T', '3D', '4T', '4D'])

    result_message = "KẾT QUẢ: "
    if result_option == 'L':
        result_message += "LẺ"
        emojis = """
        LẺ BẤT KỲ
        """
    if result_option == 'C':
        result_message += "CHẴN"
        emojis = "⚫️⚪️\n⚫️⚪️"
    elif result_option == '3T':
        result_message += "LẺ 3 TRẮNG"
        emojis = "⚪️⚪️\n⚪️⚫️"
    elif result_option == '3D':
        result_message += "LẺ 3 ĐEN"
        emojis = "⚫️⚫️\n⚫️⚪️"
    elif result_option == '4T':
        result_message += "TỨ TRẮNG"
        emojis = "⚪️⚪️\n⚪️⚪️"
    elif result_option == '4D':
        result_message += "TỨ ĐEN"
        emojis = "⚫️⚫️\n⚫️⚫️"

    update.message.reply_text(result_message)

    emojis_lines = "\n".join([emojis] * 1)
    update.message.reply_text(emojis_lines)

    winners = {}
    for user_id, bets in xocdia_bets.items():
        user_total_winnings = 0
        for choice, amount in bets:
            if choice == result_option:
                if choice in ['L', 'C']:
                    user_total_winnings += amount * 2
                elif choice in ['3T', '3D']:
                    user_total_winnings += amount * 4
                elif choice in ['4T', '4D']:
                    user_total_winnings += amount * 16
        if user_total_winnings > 0:
            winners[user_id] = user_total_winnings

    result_message = "Kết quả cược:\n"
    if len(winners) == 0:
        result_message += "Không có người chơi nào thắng cược!"
    else:
        result_message += "Người chơi - Tiền thắng\n"
        for user_id, amount_won in winners.items():
            update_user_balance(user_id, amount_won)
            result_message += f"{user_id} - {format_currency(amount_won)}\n"

    update.message.reply_text(result_message)

    xocdia_bets.clear()

    xocdia_game_active = False
def convert_floats_to_ints(data):
    if isinstance(data, float):
        return int(data)
    elif isinstance(data, list):
        return [convert_floats_to_ints(item) for item in data]
    elif isinstance(data, dict):
        return {
            key: convert_floats_to_ints(value)
            for key, value in data.items()
        }
    else:
        return data
def restrict_private_chats(func):

    @wraps(func)
    def wrapper(update, context):
        if update.message.chat_id < 0:
            return func(update, context)
        else:
            update.message.reply_text(
                "Chỉ có thể sử dụng lệnh này trong nhóm.\nNHÓM CHÍNH CỦA BOT : t.me/ztrongzgroup \nCÁC NHÓM KHÁC ĐỀU LÀ GIẢ MẠO, CƯỚP BOT"
            )

    return wrapper
def restrict_group(func):

    @wraps(func)
    def wrapper(update, context):
        if update.message.chat_id == -1002066327546:
            return func(update, context)
        else:
            update.message.reply_text(
                "Địt mẹ sài sài cái lồn.\nt.me/admztrongz mua source bot ib")

    return wrapper

def update_user_balance(user_id, amount):
    if user_id in user_balances:
        user_balances[user_id] += amount
    else:
        user_balances[user_id] = amount
def draw_card():
    return random.choice(
        ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
def format_cards(cards):
    return ', '.join(cards)
def format_currency(amount):
    return f"${amount:,.2f}"
@restrict_room
def bac(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return
    user_id = update.message.from_user.id
    args = context.args

    if len(args) != 1:
        update.message.reply_text("Sử dụng: /bac <Số tiền cược hoặc 'all'>")
        return

    if args[0].lower() == 'all':
        bet_amount = user_balances.get(user_id, 0)
    else:
        try:
            bet_amount = int(args[0])
        except ValueError:
            update.message.reply_text(
                "Số tiền cược phải là một số nguyên hoặc 'all'.")
            return

    if bet_amount <= 0:
        update.message.reply_text("Số tiền cược phải lớn hơn 0.")
        return

    if user_balances.get(user_id, 0) < bet_amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    update_user_balance(user_id, -bet_amount)

    player_cards = [draw_card(), draw_card()]
    banker_cards = [draw_card(), draw_card()]
    player_total = calculate_total_value_bac(player_cards)
    banker_total = calculate_total_value_bac(banker_cards)
    context.bot.send_chat_action(chat_id=chat_id,
                                 action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(chat_id=chat_id, photo=open('bacchaha.jfif', 'rb'))
    update.message.reply_text(
        f"💰 Bạn đã đặt cược {format_currency(bet_amount)} vào trò chơi Baccarat! 💰\n\n🃏 Bài của bạn: {format_cards(player_cards)}\n🃏 Bài của người chia: {format_cards(banker_cards[0])} và một lá ẩn.\n\n> /bactiep < để rút thêm lá bài"
    )

    context.chat_data[user_id] = {
        "bet_amount": bet_amount,
        "player_cards": player_cards,
        "banker_cards": banker_cards,
        "player_total": player_total,
        "banker_total": banker_total
    }
@restrict_room
def bactiep(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return
    user_id = update.message.from_user.id
    if user_id not in context.chat_data:
        update.message.reply_text("Bạn chưa tham gia trò chơi Baccarat nào.")
        return

    player_cards = context.chat_data[user_id]["player_cards"]
    player_total = context.chat_data[user_id]["player_total"]
    banker_cards = context.chat_data[user_id]["banker_cards"]
    banker_total = context.chat_data[user_id]["banker_total"]

    player_cards.append(draw_card())
    player_total = calculate_total_value_bac(player_cards)

    if player_total <= 5:
        banker_cards.append(draw_card())
        banker_total = calculate_total_value_bac(banker_cards)

    update.message.reply_text(
        f"🃏 Bài của bạn: {format_cards(player_cards)}\n🃏 Bài của người chia: {format_cards(banker_cards)}"
    )

    player_result = compare_bac(player_total, banker_total)
    if player_result == "win":
        update.message.reply_text(
            f"🎉 Bạn đã thắng! Số tiền nhận được: {format_currency(context.chat_data[user_id]['bet_amount'] * 2)} 🎉"
        )
        update_user_balance(user_id,
                            context.chat_data[user_id]['bet_amount'] * 2)
    elif player_result == "lose":
        update.message.reply_text("😔 Bạn đã thua. Thử lại lần sau nhé! ❌")
        update_user_balance(user_id, -context.chat_data[user_id]['bet_amount'])
    else:
        update.message.reply_text(
            "😐 Hòa. Số điểm của bạn và người chia bằng nhau.")
        update_user_balance(user_id, context.chat_data[user_id]['bet_amount'])

    del context.chat_data[user_id]
def calculate_total_value_bac(cards):
    total_value = sum([
        10 if card in ['J', 'Q', 'K'] else 0 if card == 'A' else int(card)
        for card in cards
    ]) % 10
    return total_value
def compare_bac(player_total, banker_total):
    if player_total > banker_total:
        return "win"
    elif player_total < banker_total:
        return "lose"
    else:
        return "tie"
def calculate_total_value_bac(cards):
    total_value = sum([
        10 if card in ['J', 'Q', 'K'] else 0 if card == 'A' else int(card)
        for card in cards
    ]) % 10
    return total_value
def compare_bac(player_total, banker_total):
    if player_total > banker_total:
        return "win"
    elif player_total < banker_total:
        return "lose"
    else:
        return "tie"
@restrict_room
def blackjack(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return
    user_id = update.message.from_user.id
    args = context.args

    if len(args) != 1:
        update.message.reply_text("Sử dụng: /bj <Số tiền cược hoặc 'all'>")
        return

    if args[0].lower() == 'all':
        bet_amount = user_balances.get(user_id, 0)
    else:
        try:
            bet_amount = int(args[0])
        except ValueError:
            update.message.reply_text(
                "Số tiền cược phải là một số nguyên hoặc 'all'.")
            return

    if bet_amount < 1000:
        update.message.reply_text("Số tiền cược phải lớn hơn hoặc bằng 1000.")
        return

    if user_balances.get(user_id, 0) < bet_amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    update_user_balance(user_id, -bet_amount)
    dealer_cards = draw_initial_cards()
    player_cards = draw_initial_cards()
    context.bot.send_chat_action(chat_id=chat_id,
                                 action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(chat_id=chat_id, photo=open('bjhaha.jfif', 'rb'))
    update.message.reply_text(
        f"💰 Bạn đã đặt cược {format_currency(bet_amount)} vào game Blackjack! 💰\n\n🃏 Bài của bạn: {format_cards(player_cards)}\n🃏 Bài của nhà cái: {format_cards(dealer_cards[0])} và một lá ẩn.\n\n> /hit < để rút thêm lá bài\n\n> /stand < để dừng cược và xem KQ"
    )

    context.chat_data[user_id] = {
        "bet_amount": bet_amount,
        "dealer_cards": dealer_cards,
        "player_cards": player_cards,
        "stand": False
    }
@restrict_room
def hit(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return
    user_id = update.message.from_user.id
    if user_id not in context.chat_data:
        update.message.reply_text("Bạn chưa tham gia game Blackjack nào.")
        return

    if context.chat_data[user_id]["stand"]:
        update.message.reply_text("Bạn đã chọn Stand, không thể rút thêm.")
        return

    player_cards = context.chat_data[user_id]["player_cards"]
    player_cards.append(draw_card())

    update.message.reply_text(
        f"🃏 Bạn đã rút thêm một lá: {format_cards([player_cards[-1]])}\n🃏 Bài của bạn: {format_cards(player_cards)}"
    )

    total_value = calculate_total_value(player_cards)
    if total_value > 21:
        update.message.reply_text(
            f"😔 Bạn đã vượt quá 21! Bạn đã thua {format_currency(context.chat_data[user_id]['bet_amount'])}."
        )
        update_user_balance(user_id,
                            context.chat_data[user_id]['bet_amount'] * -1)
        del context.chat_data[user_id]
    elif total_value == 21:
        update.message.reply_text(
            f"🎉 Chúc mừng! Bạn đã có 21 điểm! Bạn đã thắng {format_currency(context.chat_data[user_id]['bet_amount'] * 2)}."
        )
        update_user_balance(user_id,
                            context.chat_data[user_id]['bet_amount'] * 2)
        del context.chat_data[user_id]
@restrict_room
def stand(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot .")
        return
    user_id = update.message.from_user.id
    if user_id not in context.chat_data:
        update.message.reply_text("Bạn chưa tham gia game Blackjack nào.")
        return

    if context.chat_data[user_id]["stand"]:
        update.message.reply_text("Bạn đã chọn Stand, không thể chọn lại.")
        return

    context.chat_data[user_id]["stand"] = True
    dealer_cards = context.chat_data[user_id]["dealer_cards"]
    player_cards = context.chat_data[user_id]["player_cards"]

    while calculate_total_value(dealer_cards) < 17:
        dealer_cards.append(draw_card())

    dealer_total = calculate_total_value(dealer_cards)
    player_total = calculate_total_value(player_cards)

    update.message.reply_text(
        f"🃏 Bài của nhà cái: {format_cards(dealer_cards)}")
    time.sleep(1)

    if dealer_total > 21 or dealer_total < player_total:
        update.message.reply_text(
            f"🎉 Chúc mừng! Bạn đã thắng {format_currency(context.chat_data[user_id]['bet_amount'] * 2)}."
        )
        update_user_balance(user_id,
                            context.chat_data[user_id]['bet_amount'] * 2)
    elif dealer_total == player_total:
        update.message.reply_text(
            f"😐 Hòa. Số điểm của bạn và nhà cái đều là {player_total}.")
        update_user_balance(user_id, context.chat_data[user_id]['bet_amount'])
    else:
        update.message.reply_text(
            f"😔 Bạn đã thua. Số điểm của nhà cái ({dealer_total}) cao hơn số điểm của bạn ({player_total})."
        )
        update_user_balance(user_id,
                            context.chat_data[user_id]['bet_amount'] * -1)

    del context.chat_data[user_id]
def draw_initial_cards():
    return [draw_card(), draw_card()]
def draw_card():
    return random.choice(
        ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
def format_cards(cards):
    return ', '.join(cards)
def calculate_total_value(cards):
    total_value = 0
    number_of_aces = 0

    for card in cards:
        if card.isdigit():
            total_value += int(card)
        elif card in ['J', 'Q', 'K']:
            total_value += 10
        elif card == 'A':
            number_of_aces += 1
            total_value += 11

    while total_value > 21 and number_of_aces > 0:
        total_value -= 10
        number_of_aces -= 1

    return total_value
@restrict_room
def taolistcode(update, context):
    user_id = update.message.from_user.id
    if user_id != 6793700101:
        update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này.")
        return

    args = context.args
    if len(args) != 2:
        update.message.reply_text(
            "Sử dụng: /taolistcode <Số tiền 1 code> <Số code>")
        return

    try:
        amount_per_code = int(args[0])
        num_codes = int(args[1])
    except ValueError:
        update.message.reply_text("Số tiền và số code phải là số nguyên.")
        return

    if amount_per_code <= 0 or num_codes <= 0:
        update.message.reply_text("Số tiền và số code phải lớn hơn 0.")
        return

    code_list = []
    for _ in range(num_codes):
        code_name = generate_random_code(length=10)
        codes[code_name] = (amount_per_code, 1, False)
        code_list.append(code_name)

    save_codes()

    code_list_text = "\n".join(code_list)
    context.bot.send_message(
        chat_id=-1002066327546,
        text=
        f"Đây Là List Code Mới\n\n{code_list_text}\n\nLệnh Sài /code <code> để nhập code\nhttps://t.me/ztrongzcode"
    )
@restrict_room
def roulette(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot .")
        return
    user_id = update.message.from_user.id
    args = context.args

    if len(args) != 2:
        update.message.reply_text(
            "Sử dụng: /rou <C hoặc L hoặc số từ 0 đến 36> <Số tiền cược hoặc 'all'>\nC và L : Tỷ lệ ăn 1:2\n0 - 36 : Tỷ lệ ăn khi trúng số là 1:35\n0 : Nổ JACKPOT"
        )
        return

    choice = args[0].upper()
    valid_choices = ['C', 'L'] + [str(i) for i in range(37)]
    if choice not in valid_choices:
        update.message.reply_text(
            "Lựa chọn không hợp lệ. Vui lòng chọn 'C', 'L' hoặc số từ 0 đến 36."
        )
        return

    if args[1].lower() == 'all':
        amount = user_balances.get(user_id, 0)
    else:
        try:
            amount = int(args[1])
        except ValueError:
            update.message.reply_text(
                "Số tiền cược phải là một số nguyên hoặc 'all'.")
            return

    if amount < 1000:
        update.message.reply_text("Số tiền cược phải lớn hơn hoặc bằng 1000.")
        return

    if user_balances.get(user_id, 0) < amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    update_user_balance(user_id, -amount)
    gif_url = "https://media.giphy.com/media/T2JZjjKwucfyZfq6I8/giphy.gif"
    update.message.reply_animation(animation=gif_url)
    spin_result = random.randint(0, 36)
    is_even = spin_result % 2 == 0 and spin_result != 0
    is_odd = spin_result % 2 != 0
    update.message.reply_text(f"🎡 Hãy Chờ Đợi Kết Quả Quay!!")
    time.sleep(1)
    update.message.reply_text(f"🎡 Rolling !!")
    update.message.reply_text(f"🎡 Kết Quả Quay Đã Được Xác Định!!")
    time.sleep(1)
    update.message.reply_text(f"🎡 Kết quả quay là : {spin_result} 🎡")
    time.sleep(2)

    win_amount = 0
    if choice == 'C' and is_even:
        win_amount = amount * 2
    elif choice == 'L' and is_odd:
        win_amount = amount * 2
    elif choice == str(spin_result):
        win_amount = amount * 35

    if win_amount > 0:
        update_user_balance(user_id, win_amount)
        update.message.reply_text(
            f"🎉 Bạn đã thắng! Số tiền nhận được: {format_currency(win_amount)} 🎉"
        )
    else:
        update.message.reply_text("❌ Bạn đã thua. Thử lại lần sau nhé! ❌")
        update.message.reply_text(
            f"Số dư hiện tại của bạn: {format_currency(user_balances.get(user_id, 0))}"
        )

    if spin_result == 0:
        jackpot_amount = load_jackpot()
        update_user_balance(user_id, jackpot_amount)

        message_text = f"🌟 Bạn đã nổ JACKPOT và nhận được {format_currency(jackpot_amount)}! 🌟"
        sent_message = update.message.reply_text(message_text)

        update.message.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=sent_message.message_id, disable_notification=True)

        save_jackpot(0)
        record_jackpot_winner(user_id, jackpot_amount)
def load_used_codes():
    try:
        with open('used_codes.txt', 'r') as file:
            content = file.read().strip()
            if content == '':
                return {}
            file.seek(0)
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Lỗi JSONDecodeError: {e}")
        return {}
def save_used_code(used_codes):
    with open('used_codes.txt', 'w') as file:
        json.dump(used_codes, file, ensure_ascii=False, indent=4)
def has_used_code(user_id, code_name):
    used_codes = load_used_codes()
    return code_name in used_codes.get(str(user_id), [])
def record_used_code(user_id, code_name):
    used_codes = load_used_codes()
    if str(user_id) not in used_codes:
        used_codes[str(user_id)] = []
    used_codes[str(user_id)].append(code_name)
    save_used_code(used_codes)
def generate_random_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def taocode(update, context):
    user_id = update.message.from_user.id
    args = context.args

    if len(args) != 2:
        update.message.reply_text(
            "Sử dụng: /taocode <số tiền> <số lượt sử dụng>")
        return

    try:
        amount = int(args[0])
        uses_left = int(args[1])
    except ValueError:
        update.message.reply_text(
            "Số tiền và số lượt sử dụng phải là các số nguyên.")
        return

    if amount <= 0 or uses_left <= 0:
        update.message.reply_text("Số tiền và số lượt sử dụng phải lớn hơn 0.")
        return

    fee = int(amount * 0.1)
    total_amount = amount - fee

    amount_to_deduct = int(amount * 0.02)
    update_user_balance(user_id, -amount_to_deduct)

    if user_balances.get(user_id, 0) < total_amount:
        update.message.reply_text("Số dư của bạn không đủ để tạo code.")
        return

    update_user_balance(user_id, -total_amount)

    code_name = generate_random_code()

    code_data = f"{code_name}:{total_amount}:{uses_left}:False\n"
    with open('code.txt', 'a') as file:
        file.write(code_data)

    jackpot_amount = total_amount / 1000  
    update_jackpot(jackpot_amount)

    update.message.reply_text(
        f"Bạn đã tạo code: {code_name} với số tiền: {format_currency(total_amount)} và số lượt sử dụng: {uses_left}. Số tiền đã được cộng vào hũ."
    )
def load_jackpot():
    if os.path.exists("jackpot.txt"):
        with open("jackpot.txt", "r") as file:
            return ast.literal_eval(file.read())
    return 0
def save_jackpot(jackpot):
    with open("jackpot.txt", "w") as file:
        file.write(str(jackpot))
@restrict_group
def lsjackpot(update, context):
    jackpot_history = load_jackpot_history()
    if not jackpot_history:
        update.message.reply_text("Chưa có lịch sử hũ.")
        return

    response = "🎉 Lịch sử hũ 🎉\n"
    for user_id, won_amount in jackpot_history:
        response += f"Người chơi ID {user_id} đã thắng hũ với số tiền\n👉{format_currency(won_amount)}\n\n"
    update.message.reply_text(response)

def jackpot(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot .")
        return
    jackpot_amount = load_jackpot()
    if jackpot_amount > MAX_JACKPOT_AMOUNT:
        jackpot_amount = MAX_JACKPOT_AMOUNT 
        save_jackpot(jackpot_amount)  
    update.message.reply_text(
        f"💰 Số tiền hiện có trong Jackpot là:\n\n{format_currency(jackpot_amount)}\n\n"
        "💰Ra Bão = Hũ JACKPOT🎲\n💰Ra 0 Ở Roulette = Hũ JACKPOT 🎡\n\n"
        "Pay : Tổng số tiền tạo chia 1000 và cộng hũ")
def calculate_tax(amount):
    return amount * 10
def load_transaction_history():
    if os.path.exists(transaction_history_file):
        with open(transaction_history_file, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                logger.error(
                    "Malformed JSON or empty transaction history file.")
                return []
    return []
def save_transaction_history(history):
    with open(transaction_history_file, "w") as file:
        json.dump(history, file)
def record_transaction(user_id, transaction_type, amount):
    history = load_transaction_history()
    history.append({
        "user_id": user_id,
        "transaction_type": transaction_type,
        "amount": amount,
        "timestamp": time.time()
    })
    save_transaction_history(history)
def load_jackpot_history():
    jackpot_history = []
    if os.path.exists("history.txt"):
        with open("history.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                user_id, won_amount = line.strip().split(":")
                jackpot_history.append((int(user_id), int(won_amount)))
    return jackpot_history
def load_user_balances():
    global user_balances
    user_balances = {}
    try:
        with open("sodu.txt", "r") as file:
            for line in file:
                user_id, balance = line.strip().split(":")
                try:
                    balance_value = float(balance)
                    if balance_value == float('inf'):
                        print(
                            f"Warning: user_id {user_id} has an infinite balance. Setting to hello."
                        )
                        balance_value = 123123123123123123123123123
                    user_balances[int(user_id)] = int(balance_value)
                except ValueError:
                    print(
                        f"Error: Invalid balance value for user_id {user_id}. Skipping."
                    )
    except FileNotFoundError:
        print("User balances file not found. Initializing empty balances.")
def save_user_balances():
    global user_balances
    with open(sodu_file_path, "w") as file:
        for user_id, balance in user_balances.items():
            file.write(f"{user_id}:{balance}\n")
def load_codes():
    global codes
    if os.path.exists(codes_file_path):
        with open(codes_file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(":")
                if len(data) == 4:
                    code_name, amount, uses_left, used = data
                    codes[code_name] = (float(amount), float(uses_left),
                                        used == "True")
                else:
                    print(f"Đang bỏ qua dòng không hợp lệ: {line}")
def save_codes():
    global codes
    with open(codes_file_path, "w") as file:
        for code_name, (amount, uses_left, used) in codes.items():
            file.write(f"{code_name}:{amount}:{uses_left}:{used}\n")
def load_user_code_usage():
    global user_code_usage
    if os.path.exists(user_code_usage_file):
        with open(user_code_usage_file, "r") as file:
            user_code_usage = json.load(file)
def save_user_code_usage():
    global user_code_usage
    with open(user_code_usage_file, "w") as file:
        json.dump(user_code_usage, file)
def update_user_balance(user_id, amount):
    global user_balances
    user_balances[user_id] = user_balances.get(user_id, 0) + amount
    save_user_balances()
def format_currency(amount):
    return "{:,}".format(amount)


@restrict_room
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    user_id = user.id

    if update.message.chat.type != 'private':  
        update.message.reply_text(
            "Chỉ có thể sử dụng lệnh /start trong chat riêng với bot."
        )
        return

    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return

    if user_id not in user_balances:
        update_user_balance(user_id, 0)

    keyboard = [
        [KeyboardButton("👤 Tài Khoản"), KeyboardButton("💵 Xem Số Dư")],
        [KeyboardButton("🎰 Danh Sách Game"), KeyboardButton("👥 Mời Bạn")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    update.message.reply_text(
        f"🎲𝙕𝙂𝙧𝙤𝙪𝙥 - 𝘾𝙖𝙨𝙞𝙣𝙤 𝘽𝙤𝙩 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢🎲\n"
        f"👉 t.me/ztrongzgroup 👈 \n"
        f"🎲𝙕𝙍𝙤𝙤𝙢 - 𝙍𝙤𝙤𝙢 𝘽𝙤𝙩 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢🎲\n"
        f"👉 t.me/ztrongzroom 👈 \n"
        f"🎲𝙕𝘾𝙝𝙖𝙩 - 𝙍𝙤𝙤𝙢 𝘾𝙝𝙖𝙩 𝘼𝙡𝙡🎲\n"
        f"👉 t.me/ztrongzchat 👈 \n"
        f"🍀ADMIN : @admztrongz🍀 \n"
        f"𝐒à𝐧 𝐂𝐚𝐬𝐢𝐧𝐨 𝐗𝐮 Ả𝐨 𝐆𝐢ả𝐢 𝐓𝐫í 𝐒ố 𝟏 𝐕𝐍", reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == "👤 Tài Khoản":
        profile(update, context)
    elif text == "💵 Xem Số Dư":
        sd(update, context)
    elif text == "🎰 Danh Sách Game":
        game(update, context)
    elif text == "👥 Mời Bạn":
        moi_ban(update, context)
    else:
        return
invited_users = {}
def moi_ban(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in invited_users:
        invite_link = f"https://t.me/ztrongzroom_bot?start={user_id}"
        update.message.reply_text(
            f"👥 Mời bạn bè bằng cách gửi link sau: {invite_link}\n\n"
            f"👥 Khi mời đủ 10 bạn bè bạn sẽ nhận được 10,000 VND từ @admztrongz"
        )
        invited_users[user_id] = invited_users.get(user_id, 0) + 1
        save_invited_users()
        if invited_users[user_id] == 1:
            update.message.reply_text("🎉 Bạn đã mời thành công 1 người.")
        else:
            update.message.reply_text(f"🎉 Bạn đã mời thành công {invited_users[user_id]} người.")
    else:
        update.message.reply_text("ℹ️ Bạn đã được mời rồi.")

def handle_show_invited_count(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in invited_users:
        update.message.reply_text(f"📄 Số người bạn đã mời: {invited_users[user_id]}")
    else:
        update.message.reply_text("ℹ️ Bạn chưa mời ai cả.")

def save_invited_users():
    with open(CHECKBB_FILE, "w") as file:
        for user_id, count in invited_users.items():
            file.write(f"{user_id}:{count}\n")

def load_invited_users():
    if os.path.exists(CHECKBB_FILE):
        with open(CHECKBB_FILE, "r") as file:
            for line in file:
                user_id, count = line.strip().split(":")
                invited_users[int(user_id)] = int(count)


def reset_jackpot(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("Cút")
        return
    if len(context.args) != 1:
        update.message.reply_text("Sử dụng: /resetjackpot <số dư>")
        return

    try:
        new_jackpot_amount = int(context.args[0])
        if new_jackpot_amount < 0:
            raise ValueError("Số dư không thể âm.")
        save_jackpot(new_jackpot_amount)
        update.message.reply_text(f"Jackpot đã được đặt lại thành: {format_currency(new_jackpot_amount)}")
    except ValueError:
        update.message.reply_text("Số dư phải là một số nguyên dương.")
@restrict_room
def send_dice_results(update, context):
    chat_id = update.message.chat_id
    dice_values = []
    for i in range(3):
        dice = context.bot.send_dice(chat_id=chat_id).dice
        time.sleep(1)
        dice_values.append(dice.value)

    total = sum(dice_values)
    if 18 >= total >= 11:
        result = "T"
    else:
        result = "X"
    time.sleep(1)

    update.message.reply_text(f"🎮 Tổng 🎮: {total}\n\n🎁 Kết quả 🎁: {result}")

    return dice_values, result, total
@restrict_room
def taixiu(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    args = context.args

    if len(args) != 2:
        update.message.reply_text(
            "Sử dụng: /tx <T hoặc X> <Số tiền cược hoặc 'all'>")
        return

    choice = args[0].upper()
    if choice not in ['T', 'X']:
        update.message.reply_text(
            "Lựa chọn không hợp lệ. Vui lòng chọn 'T' hoặc 'X'.")
        return

    if args[1].lower() == 'all':
        amount = user_balances.get(user_id, 0)
    else:
        try:
            amount = int(args[1])
        except ValueError:
            update.message.reply_text(
                "Số tiền cược phải là một số nguyên hoặc 'all'.")
            return

    if amount < 1000:
        update.message.reply_text("Số tiền cược phải lớn hơn hoặc bằng 1000.")
        return

    if user_balances.get(user_id, 0) < amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    record_transaction(user_id, "start_taixiu", amount)
    update_user_balance(user_id, -amount)

    dice_values, result, total = send_dice_results(update, context)

    if result == choice:
        win_amount = amount * 1.95
        update_user_balance(user_id, win_amount)
        update.message.reply_text(
            f"🎉 Chúc mừng bạn đã thắng! 🎉\n🏆 Số tiền nhận được: {format_currency(win_amount)}\n💰 Số dư mới: {format_currency(user_balances[user_id])}"
        )
        record_transaction(user_id, "end_taixiu", win_amount)
    else:
        update.message.reply_text("❌ Rất tiếc, bạn đã thua! 🎲")
        update.message.reply_text(
            f"💰 Số dư mới của bạn là: {format_currency(user_balances[user_id])}"
        )
        record_transaction(user_id, "end_taixiu", -amount)

    if len(set(dice_values)) == 1 and dice_values[0] in [1, 2, 3, 4, 5, 6]:
        jackpot_amount = load_jackpot()
        update_user_balance(user_id, jackpot_amount)
        jackpot_message = f"🌟🌟🌟 Chúc mừng! {user_id} đã trúng JACKPOT với số tiền {format_currency(jackpot_amount)} 🌟🌟🌟\nSố dư hiện tại của bạn: {format_currency(user_balances.get(user_id, 0))}"
        jackpot_sent_message = update.message.reply_text(jackpot_message)

        context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=jackpot_sent_message.message_id, disable_notification=True)

        save_jackpot(0)
        record_jackpot_winner(user_id, jackpot_amount)


def record_jackpot_winner(user_id, amount_won):
    jackpot_history = load_jackpot_history()
    jackpot_history.append((user_id, jackpot_amount))
    save_jackpot_history(history)
def update_jackpot(amount):
    jackpot_amount = load_jackpot()
    new_jackpot_amount = jackpot_amount + amount
    save_jackpot(new_jackpot_amount)
@restrict_room
def chuyentien(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return
    args = context.args

    if update.message.reply_to_message and len(args) == 1:
        recipient_id = update.message.reply_to_message.from_user.id
        try:
            amount = int(args[0])
        except ValueError:
            update.message.reply_text("Số tiền cần là một số nguyên.")
            return
    elif len(args) == 2:
        try:
            amount = int(args[0])
            recipient_id = int(args[1])
        except ValueError:
            update.message.reply_text("Số tiền và ID người nhận phải là các số nguyên.")
            return
    else:
        update.message.reply_text(
            "Có 2 Cách Chuyển :\n✅CÁCH 1 : /pay <số tiền chuyển> <ID> \n\n✅CÁCH 2 : /pay <số tiền chuyển> (Reply Tin Nhắn User Bạn Chuyển Tới)"
        )
        return

    if amount <= 0:
        update.message.reply_text("Số tiền phải lớn hơn 0.")
        return

    if amount < 10000000:
        update.message.reply_text("✅ Hạn Mức Chuyển ✅\nMIN = 10,000,000 VND")
        return

    if user_balances.get(user_id, 0) < amount:
        update.message.reply_text("Số dư của bạn không đủ để thực hiện giao dịch này.")
        return

    if recipient_id == user_id:
        update.message.reply_text("⁉️ Bot Không Thể Chuyển Cho Bot ⁉️")
        return

    fee = amount * 0.1
    net_amount = amount - fee

    user_balances[user_id] -= amount

    if user_balances[user_id] < 0:
        user_balances[user_id] += amount
        update.message.reply_text(
            "Giao dịch không thành công. Số dư của bạn không đủ để thực hiện giao dịch này."
        )
        return

    if recipient_id not in user_balances:
        user_balances[recipient_id] = 0
    user_balances[recipient_id] += net_amount

    update_jackpot(fee)

    try:
        context.bot.send_message(
            chat_id=recipient_id,
            text=f"✅ Bạn đã nhận được {format_currency(net_amount)} từ người dùng có ID {user_id}."
        )
    except Exception as e:
        username = f"@{update.message.reply_to_message.from_user.username}" if update.message.reply_to_message.from_user.username else f"ID {recipient_id}"
        update.message.reply_text(
            f"🚫 Không thể chuyển vì user nhận chưa có contact với bot\n🌐 {username} Vui Lòng Nhắn Bot @ztrongzroom_bot 🌐"
        )
        user_balances[user_id] += amount  # Revert the transaction
        user_balances[recipient_id] -= net_amount
        update_jackpot(-fee)  # Revert the fee update
        return

    update.message.reply_text(
        f"✅ Bạn đã chuyển {format_currency(amount)} tới người dùng có ID {recipient_id}. Phí 10% đã được trích xuống hũ."
    )

@restrict_room
def help_command(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot .")
        return
    update.message.reply_text(
        "🕹️ /start: Lệnh Thường✨\n\n"
        "🕹️ /game : Xem danh sách game và các lệnh🕹️\n\n"
        "🕹️ /sd : Xem số dư 💰\n\n"
        "🕹️ /profile : Xem profile 💰\n\n"
        "🕹️ /code : Nhập mã code 🔄\n\n"
        "🕹️ /jackpot : Xem tiền JACKPOT 💰\n\n"
        "🕹️ /pay : Chuyển tiền 💸\n\n"
        "🕹️ /doitien : Đổi tiền sang code 🔄\n\n"
        "🕹️ /top : Top số dư 💸\n\n"
        "📌 HỖ TRỢ 📌\n"
        "🕹️ ADMIN GAME : @admztrongz ❤️\n"
        "Thắc Mắc/Góp Ý/Báo Lỗi - Mua/Thuê Code Bot IB để được hỗ trợ\n\n"
        "Zalo : 0909743280\n"
        "FB : ZTrongz Phuoc")
def game(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("💵 Nạp Xu 💵", callback_data='nap'),
        ],
        [
            InlineKeyboardButton("💵 Rút Xu 💵", callback_data='rutmomo'),
        ],
        [
            InlineKeyboardButton("💰 Giá Xu 💰", callback_data='giaxu')
        ],
        [
            InlineKeyboardButton("🎲 Tài Xỉu 🎲", callback_data='tx'),
            InlineKeyboardButton("🎲 Tài Xỉu Room 🎲", callback_data='room')
        ],
        [
            InlineKeyboardButton("🃏 Blackjack 🃏", callback_data='bj'),
            InlineKeyboardButton("🎰 Roulette 🎰", callback_data='rou')
        ],
        [
            InlineKeyboardButton("🎴 Baccarat 🎴", callback_data='bac'),
            InlineKeyboardButton("✈️ Aviator ✈️", callback_data='startav')
        ],
        [
            InlineKeyboardButton("🎲 Sicbo 🎲", callback_data='sicbo'),
            InlineKeyboardButton("🎱 Keno 🎱", callback_data='keno')
        ],
        [    
            InlineKeyboardButton("⚪️ Xóc Đĩa Room ⚫️", callback_data='xocdia'),
            InlineKeyboardButton("🏇 Đua Ngựa 🏇", callback_data='starth')
        ],
        [
            InlineKeyboardButton("🎰 Slot 🎰", callback_data='slot'),
            InlineKeyboardButton("⚪️ Chẵn Lẻ ⚫️", callback_data='chanle')
        ],
        [
            InlineKeyboardButton("🎲 Solo Xúc Xắc 🎲", callback_data='solo'),
        ],
        [
            InlineKeyboardButton("🎫 Xổ Số 30S 🎫", callback_data='xs'),
            InlineKeyboardButton("🧧 Lân Hái Lộc 🧧", callback_data='hailoc')
        ],
        [
            InlineKeyboardButton("💰 JACKPOT 💰", callback_data='jackpot'),
            InlineKeyboardButton("🧧 HŨ LỘC 🧧", callback_data='huloc')
        ],
        [
            InlineKeyboardButton("✅ Top Số Dư ✅ ", callback_data='top'),
        ],
        [
            InlineKeyboardButton("🔥 TÀI XỈU ROOM 🔥", url='https://t.me/ztrongzroomtaixiu')
        ],
        [
            InlineKeyboardButton("🔥 SICBO ROOM 🔥", url='https://t.me/ztrongzroomsicbo')
        ],
        [
            InlineKeyboardButton("🔰 Admin Game 🔰", url='https://t.me/admztrongz')
        ], 
        [
            InlineKeyboardButton("❤️ Shop Admin ❤️", url='https://zrandomshop.com')
        ],
        [
            InlineKeyboardButton("✅ Cách Chơi Game ✅", url='https://t.me/ztrongzgroup/219422')
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Dưới đây là các game hiện có và lệnh:", reply_markup=reply_markup)
def gamebutton(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    command = query.data
    response_text = f"👉 Hãy Sử Dụng Lệnh: /{command}"

    query.edit_message_text(text=response_text)
def sd(update, context):
    sender = update.message.from_user

    if update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot:
        return

    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        replied_user = update.message.reply_to_message.from_user
        user_id = replied_user.id
        user_mention = replied_user.mention_html()
        user_text = f"💵 Số dư của {user_mention} là:"

    else:
        user_id = sender.id
        user_mention = sender.mention_html()
        user_text = f"💵 Số dư của bạn là:"

    if user_id in user_balances:
        balance = user_balances[user_id]
        update.message.reply_html(f"{user_text} {format_currency(balance)} 💵")
    else:
        update.message.reply_text("Không tìm thấy thông tin số dư của người dùng.")


@restrict_room
def addcode(update, context):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text("❌ Tạo code cái con cặc nha 😂😂😂.")
        return

    args = context.args
    if len(args) != 3:
        update.message.reply_text(
            "Sử dụng: /addcode <tên code> <số tiền> <số lượt sử dụng>")
        return

    code_name = args[0]
    try:
        amount = int(args[1])
        uses_left = int(args[2])
    except ValueError:
        update.message.reply_text(
            "Số tiền và số lượt sử dụng phải là các số nguyên.")
        return

    if user_id in [5960502197, 123123123] and amount > 50000000000000000:
        update.message.reply_text(
            "Bạn chỉ được tạo code với số tiền tối đa là 50MB.")
        return

    codes[code_name] = (amount, uses_left, False)
    save_codes()
    update.message.reply_text(
        "Đã tạo code '{}' với số tiền {} và số lượt sử dụng {} 💳".format(
            code_name, format_currency(amount), uses_left))

def update_user_balance(user_id, amount):
    global user_balances
    if user_id not in user_balances:
        user_balances[user_id] = 0
    user_balances[user_id] += amount

@restrict_room
def code(update, context):
    logging.debug("Function 'code' is called!") 

    user_id = update.message.from_user.id
    logging.debug(f"User ID: {user_id}")

    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot .")
        return

    args = context.args
    logging.debug(f"Args: {args}")

    if len(args) != 1:
        update.message.reply_text(
            "Sử dụng: /code <tên code>\nhttps://t.me/ztrongzcode")
        return

    code_name = args[0]
    logging.debug(f"Code name: {code_name}")

    logging.debug(f"All codes: {codes}")

    if code_name not in codes:
        update.message.reply_text("❌ Mã code không hợp lệ.")
        return

    amount, uses_left, used = codes[code_name]
    logging.debug(f"Amount: {amount}, Uses left: {uses_left}, Used: {used}")

    if has_used_code(user_id, code_name):
        update.message.reply_text("❌ Bạn đã sử dụng mã code này rồi.")
        return

    if used or uses_left <= 0:
        update.message.reply_text(
            "❌ Mã code đã được sử dụng hoặc hết lượt sử dụng.")
        return

    update_user_balance(user_id, amount)
    update.message.reply_text(
        "✅ Bạn đã nhận được {} tiền từ mã code '{}' 💸".format(
            format_currency(amount), code_name))

    codes[code_name] = (amount, uses_left - 1, uses_left - 1 <= 0)
    save_codes()
    record_used_code(user_id, code_name)

    if user_id not in user_code_usage:
        user_code_usage[user_id] = []
    user_code_usage[user_id].append(code_name)
    save_user_code_usage()

    logging.debug(f"User code usage: {user_code_usage}")
def givecode(update, context):
    user_id = update.message.from_user.id
    if user_id == authorized_users:
        update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này.")
        return

    args = context.args
    if len(args) != 3:
        update.message.reply_text(
            "Sử dụng: /givecode <Tên code> <Số tiền> <ID người nhận>")
        return

    code_name = args[0]
    try:
        amount = int(args[1])
        recipient_id = int(args[2])
    except ValueError:
        update.message.reply_text(
            "Số tiền và ID người nhận phải là các số nguyên.")
        return

    codes[code_name] = (amount, 1, False)
    save_codes()

    context.bot.send_message(
        chat_id=recipient_id,
        text=
        f"Xin chào, bạn nhận được 1 code free từ Admin. Tên code: {code_name}\nVào nhóm https://t.me/ztrongzgroup để sài code"
    )
    update.message.reply_text(
        f"Đã gửi code '{code_name}' với số tiền {format_currency(amount)} tới người dùng {recipient_id}."
    )
def group_chat(update, context):
    message = update.message
    if message is not None and message.chat_id == -1002066327546:
        pass
betting_deadline = datetime.time(6, 30)
@restrict_room
def keno(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot .")
        return
    user_id = update.message.from_user.id
    args = context.args

    if len(args) < 2:
        update.message.reply_text(
            "Sử dụng: /keno <số tiền cược> <5 con số từ 1-80>")
        return

    try:
        bet_amount = int(args[0])
    except ValueError:
        update.message.reply_text("Số tiền cược phải là một số nguyên.")
        return

    if bet_amount <= 0:
        update.message.reply_text("Số tiền cược phải lớn hơn 0.")
        return

    if user_balances.get(user_id, 0) < bet_amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    user_numbers = list(map(int, args[1:]))
    if not all(1 <= number <= 80
               for number in user_numbers) or len(user_numbers) > 5:
        update.message.reply_text("Chọn 5 con số từ 1 đến 80.")
        return

    update_user_balance(user_id, -bet_amount)

    draw_numbers = random.sample(range(1, 81), 15)
    matches = set(user_numbers) & set(draw_numbers)
    win_amount = calculate_keno_win(bet_amount, len(matches))

    update_user_balance(user_id, win_amount)

    context.bot.send_chat_action(chat_id=chat_id,
                                 action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(chat_id=chat_id, photo=open('kenohaha.jfif', 'rb'))

    update.message.reply_text(
        f"💰 Bạn đã đặt cược {format_currency(bet_amount)} vào trò chơi Keno! 💰"
    )
    time.sleep(1)
    update.message.reply_text(
        f"🔢 Số bạn chọn: {', '.join(map(str, user_numbers))}")
    time.sleep(1)
    update.message.reply_text(
        f"🎲 Số được rút: {', '.join(map(str, draw_numbers))}")
    time.sleep(1)
    update.message.reply_text(f"🔗 Số khớp: {', '.join(map(str, matches))}")
    time.sleep(1)
    update.message.reply_text(
        f"💵 Số tiền thắng: {format_currency(win_amount)}")
def calculate_keno_win(bet_amount, matches_count):
    if matches_count == 0:
        return 0
    else:
        return bet_amount * matches_count
def draw_dice():
    return random.randint(1, 6)

def format_dice(dice):
    return ', '.join(str(d) for d in dice)

def calculate_sicbo_payout(dice, bet_type):
    dice_total = sum(dice)

    if bet_type == "BBK":
        if dice[0] == dice[1] == dice[2]:
            return 31

    if bet_type.startswith("B") and len(bet_type) == 2:
        specific_triple = int(bet_type[1])
        if dice.count(specific_triple) == 3:
            return 181
    elif bet_type == "4":
        if dice_total == 4:
            return 61
    elif bet_type == "5":
        if dice_total == 5:
            return 31
    elif bet_type == "6":
        if dice_total == 6:
            return 18
    elif bet_type == "7":
        if dice_total == 7:
            return 13
    elif bet_type == "8":
        if dice_total == 8:
            return 9
    elif bet_type == "9":
        if dice_total == 9:
            return 7
    elif bet_type == "10":
        if dice_total == 10:
            return 7
    elif bet_type == "11":
        if dice_total == 11:
            return 7
    elif bet_type == "12":
        if dice_total == 12:
            return 7
    elif bet_type == "13":
        if dice_total == 13:
            return 9
    elif bet_type == "14":
        if dice_total == 14:
            return 13
    elif bet_type == "15":
        if dice_total == 15:
            return 18
    elif bet_type == "16":
        if dice_total == 16:
            return 31
    elif bet_type == "17":
        if dice_total == 17:
            return 61

    return 0

def is_valid_bet_type(bet_type):
    valid_bets = [
        "BBK", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14",
        "15", "16", "17"
    ]
    if bet_type.startswith("B") and bet_type[1].isdigit() and 1 <= int(
            bet_type[1]) <= 6:
        return True
    return bet_type in valid_bets
@restrict_room
def sicbo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return
    args = context.args

    if len(args) != 2:
        update.message.reply_text(
            "Sử dụng: /sicbo <Cửa Cược> <Số Tiền Hoặc 'all'>")
        return

    bet_type = args[0].upper()
    if not is_valid_bet_type(bet_type):
        update.message.reply_text(
            "Cửa cược không hợp lệ. Các cửa cược hợp lệ là :\nB1, B2, B3, B4, B5, B6, BBK, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17."
        )
        return

    if args[1].lower() == 'all':
        bet_amount = user_balances.get(user_id, 0)
    else:
        try:
            bet_amount = int(args[1])
        except ValueError:
            update.message.reply_text(
                "Số tiền cược phải là một số nguyên hoặc 'all'.")
            return

    if bet_amount <= 0:
        update.message.reply_text("Số tiền cược phải lớn hơn 0.")
        return

    if user_balances.get(user_id, 0) < bet_amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    update_user_balance(user_id, -bet_amount)

    dice_values = []
    for i in range(3):
        dice = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value
        dice_values.append(dice)
        time.sleep(1)

    dice_total = sum(dice_values)
    payout_ratio = calculate_sicbo_payout(dice_values, bet_type)
    multiplier = random.choice([2, 5, 10, 88])
    photo_filename = f'x{multiplier}.jpg'

    context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                 action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(photo_filename, 'rb'))

    update.message.reply_text(
        f"💰 Bạn đã đặt cược {format_currency(bet_amount)} vào trò chơi Sicbo! 💰\n\n🎲 Kết quả của bạn: {format_dice(dice_values)}"
    )

    update.message.reply_text(f"\n🎲 Tổng 🎲 : {dice_total} ")

    if payout_ratio > 0:
        winnings = bet_amount * payout_ratio * multiplier
        update.message.reply_text(
            f"🎉 Chúc mừng! Bạn đã thắng {format_currency(winnings)}.")
        update_user_balance(user_id, winnings)
    else:
        update.message.reply_text(
            f"😔 Bạn đã thua. Số điểm của nhà cái là 🎲 {dice_total} 🎲.")

    if user_id in context.chat_data:
        del context.chat_data[user_id]

def ban_thanh_vien(update, context):
    if update.message.from_user.id not in [6793700101,122313213]:
        update.message.reply_text(
            "Chỉ admin mới có thể sử dụng chức năng này.")
        return
    if not context.args:
        update.message.reply_text("Sử dụng: /banthanhvien <ID họ>")
        return

    user_id = int(context.args[0])
    if user_id not in banned_users:
        banned_users.append(user_id)
        update.message.reply_text("Đã cấm thành viên này sử dụng bot")
    else:
        update.message.reply_text("Thành viên này đã bị cấm sử dụng bot")
def unban_thanh_vien(update, context):
    if update.message.from_user.id not in authorized_users:
        update.message.reply_text(
            "Chỉ admin mới có thể sử dụng chức năng này.")
        return
    if not context.args:
        update.message.reply_text("Sử dụng: /unbanthanhvien <ID>")
        return

    user_id = int(context.args[0])
    if user_id in banned_users:
        banned_users.remove(user_id)
        update.message.reply_text(
            "Đã bỏ cấm thành viên này sử dụng bot trong chat riêng.")
    else:
        update.message.reply_text(
            "Thành viên này không được cấm sử dụng bot trong chat riêng.")
def private_message(update, context):
    user_id = update.message.from_user.id
    update.message.reply_text(
        "Hi bạn yêu !\n\nBạn muốn sử dụng bot trong chat riêng hã ?\nVào đây nè : t.me/ztrongzgroup"
    )
def cam_nhom(update, context):
    global banned_groups
    if update.message.from_user.id not in admin_ids:
        update.message.reply_text(
            "Chỉ admin mới có thể sử dụng chức năng này.")
        return

    if not context.args:
        update.message.reply_text("Sử dụng: /camnhom <ID nhóm>")
        return

    group_id = int(context.args[0])

    if group_id in banned_groups:
        update.message.reply_text("Nhóm này đã bị cấm sử dụng chat.")
        return

    banned_groups.append(group_id)

    update.message.reply_text(
        f"Nhóm với ID {group_id} đã bị cấm sử dụng chat.")
def themsodu(update, context):
    user_id = update.message.from_user.id

    if user_id not in authorized_users and [6755605749]:
        update.message.reply_text(
            "Bạn không có quyền thực hiện hành động này.")
        return

    args = context.args

    if len(args) != 2:
        update.message.reply_text("Sử dụng: /addsd <ID> <số tiền>")
        return

    user_id_to_add = int(args[0])
    amount_to_add = float(args[1])

    if amount_to_add <= 0:
        update.message.reply_text("Số tiền phải lớn hơn 0.")
        return

    update_user_balance(user_id_to_add, amount_to_add)

    update.message.reply_text(
        f"Đã thêm số dư {format_currency(amount_to_add)} vào tài khoản của người dùng có ID {user_id_to_add}."
    )
def update_user_balance(user_id, amount):
    global user_balances
    with aviator_lock:
        user_balances[user_id] = user_balances.get(user_id, 0) + amount
        if user_balances[user_id] < 0:
            user_balances[user_id] = 0
        save_user_balances()

@restrict_room
def start_aviator(update: Update, context: CallbackContext):
    global aviator_game_active, aviator_bets, aviator_multiplier, betting_timer

    if aviator_game_active:
        update.message.reply_text(
            "✈️ Game Aviator đang diễn ra! Bạn có thể đặt cược. ✈️")
        return

    aviator_game_active = True
    aviator_bets = {}
    aviator_multiplier = 1.0
    betting_timer = 30  

    context.bot.send_chat_action(chat_id=update.message.chat_id,
                                 action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('av.png', 'rb'))

    update.message.reply_text(
        "✈️ Game Aviator đã bắt đầu ✈️\nLệnh Game : \n/av <số tiền cược hoặc 'all'> để đặt cược\n/rut để rút tiền.\n\n💰Có Thể Nhiều User Cược Cùng Game💰\n‼️ ĐẾM NGƯỢC 30S ‼️"
    )
    threading.Thread(target=start_betting_timer,
                     args=(update, context)).start()

@restrict_room
def start_betting_timer(update: Update, context: CallbackContext):
    global betting_timer

    while betting_timer > 0:
        time.sleep(1)
        betting_timer -= 1
        if betting_timer % 5 == 0:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"Còn {betting_timer} giây để cược.\n\nVào cược đi cắc chiến thần ơi !"
            )

    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Hết thời gian cược. Trò chơi bắt đầu!")
    run_aviator_game(update, context)
@restrict_room
def aviator(update: Update, context: CallbackContext):
    global aviator_bets, aviator_game_active, betting_timer

    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return

    if not aviator_game_active:
        update.message.reply_text(
            "Hiện không có game Aviator nào đang diễn ra.")
        return

    args = context.args
    if len(args) != 1:
        update.message.reply_text("Sử dụng: /av <số tiền cược hoặc 'all'>")
        return

    if args[0].lower() == 'all':
        bet_amount = user_balances.get(user_id, 0)
    else:
        try:
            bet_amount = int(args[0])
        except ValueError:
            update.message.reply_text(
                "Số tiền cược phải là một số nguyên hoặc 'all'.")
            return

    if bet_amount <= 0:
        update.message.reply_text("Số dư của bạn là 0, không thể chơi game.")
        return

    if user_balances.get(user_id, 0) < bet_amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    if betting_timer > 0:
        aviator_bets[user_id] = bet_amount
        update_user_balance(user_id, -bet_amount)
        update.message.reply_text(
            f"Bạn đã đặt cược {format_currency(bet_amount)} vào trò chơi Aviator!"
        )
    else:
        update.message.reply_text(
            "Trò chơi đã kết thúc hoặc dừng cược. Bạn không thể cược nữa.")
        send_total_bets(update, context)
def run_aviator_game(update, context):
    global aviator_game_active, aviator_bets, aviator_multiplier

    time.sleep(2)

    try:
        multiplier_messages_sent = set()
        losers = []

        while aviator_game_active:
            aviator_multiplier += random.uniform(0.5, 1.0)
            time.sleep(3)
            if f"{aviator_multiplier:.2f}" not in multiplier_messages_sent:
                context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=f"Multiplier hiện tại : \n\n✈️-----x{aviator_multiplier:.2f}-----✈️\n\nNhớ Rút Tiền Nhé !")
                multiplier_messages_sent.add(f"{aviator_multiplier:.2f}")
                time.sleep(1)

            if random.random() < (aviator_multiplier / 100):
                context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=f"💥💥 Máy bay đã nổ ở multiplier 💥💥\n\n-----x{aviator_multiplier:.2f}-----\n\nChia Buồn Cho Ai Hong Rút Tiền Nè ><"
                )
                aviator_game_active = False
                losers = [
                    user_id for user_id, bet_amount in aviator_bets.items()
                    if bet_amount > 0
                ]
                break

        total_winners = 0
        total_winnings = 0

        for user_id, bet_amount in aviator_bets.items():
            if bet_amount > 0:
                if user_id not in losers:
                    total_winners += 1
                    winnings = bet_amount * aviator_multiplier
                    update_user_balance(user_id, winnings)
                    total_winnings += winnings
                else:
                    aviator_bets[user_id] = 0

        update.message.reply_text(
            f"Trò Chơi Kết Thúc Vì Máy Bay Đã Nổ !\n🏆Chúc Mừng Các Đại Gia Đã Thắng Cược🏆\n\n/startav để bắt đầu game mới !"
        )

    finally:
        aviator_game_active = False
        aviator_bets.clear()
@restrict_room
def cashout(update: Update, context: CallbackContext):
    global aviator_bets, aviator_multiplier

    user_id = update.message.from_user.id
    if user_id not in aviator_bets or aviator_bets[user_id] == 0:
        update.message.reply_text("Bạn chưa đặt cược vào trò chơi Aviator.")
        return

    bet_amount = aviator_bets[user_id]
    winnings = bet_amount * aviator_multiplier
    update_user_balance(user_id, winnings)
    aviator_bets[user_id] = 0

    update.message.reply_text(
        f"Bạn đã rút tiền và thắng {format_currency(winnings)} với multiplier x{aviator_multiplier:.2f}"
    )
def print_rainbow_text(text):
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']

    while True:
        for color in colors:
            print("\033c", end="")
            figlet_text = pyfiglet.figlet_format(text, font="standard")
            colored_text = "".join([
                colored(char, color) if char != ' ' else ' '
                for char in figlet_text
            ])
            print(colored_text)
            time.sleep(0.5)
def normalize_user_balance(user_id):
    global user_balances
    balance = user_balances.get(user_id, 0.0)

    if math.isinf(balance):
        user_balances[user_id] = float('1e999')
    elif math.isnan(balance):
        user_balances[user_id] = 0.0

    user_balances[user_id] = float(user_balances[user_id])
def update_user_balance(user_id, amount):
    global user_balances
    with aviator_lock:
        if user_id not in user_balances:
            user_balances[user_id] = 0.0

        user_balances[user_id] += amount

        if user_balances[user_id] < 0:
            user_balances[user_id] = 0.0

        normalize_user_balance(user_id)
        save_user_balances()

@restrict_room
def hotro(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return

    username = update.message.from_user.username
    message = ' '.join(context.args)

    if not message:
        update.message.reply_text(
            "Vui lòng cung cấp thông tin hỗ trợ. Ví dụ: /hotro Tôi cần giúp đỡ với..."
        )
        return

    try:
        context.bot.send_message(
            chat_id=6793700101, 
            text=f"Yêu cầu hỗ trợ từ @{username} (ID: {user_id})\nNội Dung: {message}"
        )
        update.message.reply_text(
            "Thông tin của bạn đã được gửi đến admin. Cảm ơn bạn!"
        )
    except BadRequest as e:
        update.message.reply_text(
            f"Không thể gửi thông tin tới admin: {e}"
        )

def run_rainbow_text():
    text = """
    
    ! ZTrongz Bot !

FB : \nZTrongz Phuoc
    
    """
    print_rainbow_text(text)


@restrict_room
def slot_machine(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return
    user_id = update.message.from_user.id
    args = context.args

    if len(args) != 1:
        update.message.reply_text("Sử dụng: /s <Số tiền cược hoặc 'all'>")
        return

    if args[0].lower() == 'all':
        bet_amount = user_balances.get(user_id, 0)
    else:
        try:
            bet_amount = int(args[0])
        except ValueError:
            update.message.reply_text(
                "Số tiền cược phải là một số nguyên hoặc 'all'.")
            return

    if bet_amount <= 0:
        update.message.reply_text("Số tiền cược phải lớn hơn 0.")
        return

    if user_balances.get(user_id, 0) < bet_amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    update_user_balance(user_id, -bet_amount)

    symbols = ['🍒', '🍊', '🍋', '7', 'BAR']
    probabilities = [0.25, 0.25, 0.25, 0.5, 0.25]

    result = [
        random.choices(symbols, weights=probabilities)[0] for _ in range(3)
    ]

    win_multiplier = 0
    if len(set(result)) == 1:
        win_multiplier = 5
    elif result.count('🍒') == 3:
        win_multiplier = 5
    elif result.count('🍊') == 3:
        win_multiplier = 5
    elif result.count('🍋') == 3:
        win_multiplier = 5
    elif result.count('BAR') == 3:
        win_multiplier = 25
    elif result.count('7') == 3:
        win_multiplier = 50
    elif result.count('🍒') == 2:
        win_multiplier = 2
    elif result.count('🍊') == 2:
        win_multiplier = 2
    elif result.count('🍋') == 2:
        win_multiplier = 2
    elif result.count('BAR') == 2:
        win_multiplier = 10
    elif result.count('7') == 2:
        win_multiplier = 15

    if win_multiplier > 0:
        win_amount = bet_amount * win_multiplier
        update_user_balance(user_id, win_amount)
        update.message.reply_text(
            f"🎰 Kết quả: [ {' '.join(result)} ]\n🎉 Chúc mừng! Bạn đã thắng {format_currency(win_amount)}."
        )
    else:
        update.message.reply_text(
            f"🎰 Kết quả: [ {' '.join(result)} ]\n😔 Rất tiếc, bạn đã không thắng."
        )

    update.message.reply_text(
        f"Số dư hiện tại của bạn: {format_currency(user_balances.get(user_id, 0))}"
    )
def request_code_approval(update, context):
    user_id = update.message.from_user.id
    if user_id in authorized_users:
        update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này.")
        return

    args = context.args
    if len(args) != 1:
        update.message.reply_text("Sử dụng: /yccode <giá tiền>")
        return

    try:
        amount = int(args[0])
        if amount <= 0:
            update.message.reply_text("Giá tiền phải là một số nguyên dương.")
            return
    except ValueError:
        update.message.reply_text("Giá tiền phải là một số nguyên dương.")
        return

    code_approval_message = f"Yêu cầu tạo mã code mới với giá tiền: {format_currency(amount)}"
    keyboard = [[
        InlineKeyboardButton("Đồng ý", callback_data=f"approve_code_{amount}"),
        InlineKeyboardButton("Không đồng ý", callback_data="reject_code")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=admin_id,
                             text=code_approval_message,
                             reply_markup=reply_markup)
    update.message.reply_text("Yêu cầu đã được gửi đến admin.")
def handle_code_approval(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    if user_id != admin_id:
        query.answer("Bạn không có quyền thực hiện hành động này.")
        return

    data = query.data.split("_")
    action = data[0]
    if action == "approve":
        amount = int(data[2])
        code_name = generate_random_code()
        code_data = f"{code_name}:{amount}:1:False\n"
        with open('code.txt', 'a') as file:
            file.write(code_data)
        query.answer(
            f"Mã code mới '{code_name}' đã được tạo và gửi lại cho user.")
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=
            f"Mã code mới '{code_name}' với giá tiền {format_currency(amount)} đã được tạo."
        )
    elif action == "reject":
        query.answer("Yêu cầu đã bị từ chối.")
def chanle(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return
    user_id = update.message.from_user.id
    args = context.args

    if len(args) != 2:
        update.message.reply_text(
            "Sử dụng: /chanle <C hoặc L> <Số tiền cược hoặc 'all'>")
        return

    choice = args[0].upper()
    if choice not in ['C', 'L']:
        update.message.reply_text("Lựa chọn phải là 'C' hoặc 'L'.")
        return

    if args[1].lower() == 'all':
        bet_amount = user_balances.get(user_id, 0)
    else:
        try:
            bet_amount = int(args[1])
        except ValueError:
            update.message.reply_text(
                "Số tiền cược phải là một số nguyên hoặc 'all'.")
            return

    if bet_amount <= 0:
        update.message.reply_text("Số tiền cược phải lớn hơn 0.")
        return

    if user_balances.get(user_id, 0) < bet_amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    update_user_balance(user_id, -bet_amount)

    epoch_time = get_epoch_time()
    if epoch_time is None:
        update.message.reply_text(
            "Không thể lấy được thời gian Timeticks. Vui lòng thử lại sau.")
        return

    epoch_str = str(epoch_time)
    last_digit = epoch_str[-1]

    try:
        last_digit_int = int(last_digit)
    except ValueError:
        update.message.reply_text(
            "Không thể chuyển đổi giá trị cuối cùng của thời gian Timeticks thành số nguyên."
        )
        return

    if (choice == 'C'
            and last_digit_int % 2 == 0) or (choice == 'L'
                                             and last_digit_int % 2 != 0):
        update.message.reply_text(
            f"🎉 Chúc mừng! Kết quả Timeticks: {epoch_str}. Bạn đã thắng {format_currency(bet_amount * 2.35)}."
        )
        update_user_balance(user_id, bet_amount * 2.35)
    else:
        update.message.reply_text(
            f"😔 Rất tiếc! Kết quả Timeticks: {epoch_str}. Bạn đã thua {format_currency(bet_amount)}."
        )
def get_epoch_time():
    return random.randint(1000000000, 9999999999)
def generate_random_code(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@restrict_room
def doitien(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    args = context.args

    if len(args) != 1:
        update.message.reply_text("Sử dụng: /doitien <số tiền chuyển>")
        return

    try:
        amount = int(args[0])
    except ValueError:
        update.message.reply_text("Số tiền phải là một số nguyên.")
        return

    if amount <= 0:
        update.message.reply_text("Số tiền phải lớn hơn 0.")
        return
    if amount <= 10000000000:
        update.message.reply_text("Nghèo Thì Bớt Tạo Nha")
        return

    if user_balances.get(user_id, 0) < amount:
        update.message.reply_text("Số dư của bạn không đủ.")
        return

    fee = int(amount * 0.1)
    total_amount = amount - fee
    jackpot_amount = fee  

    update_user_balance(user_id, -amount)
    update_jackpot(jackpot_amount)

    keyboard = [[
        InlineKeyboardButton(
            "Có", callback_data=f"approve_{user_id}_{total_amount}"),
        InlineKeyboardButton("Không",
                             callback_data=f"reject_{user_id}_{total_amount}")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=
        f"Yêu cầu đổi tiền sang mã code từ user {user_id} với số tiền {format_currency(total_amount)}.",
        reply_markup=reply_markup)
    update.message.reply_text(
        "Yêu cầu của bạn đã được gửi đi, vui lòng chờ phê duyệt từ admin.")
def handle_admin_response(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data.split("_")
    action = data[0]
    user_id = int(data[1])
    amount = int(data[2])

    if action == "approve":
        code_name = generate_random_code()
        context.bot.send_message(
            chat_id=user_id,
            text=
            f"Yêu cầu đổi tiền của bạn đã được phê duyệt. Mã code của bạn là: {code_name} với số tiền {format_currency(amount)}.\n\nLưu Ý : Nên Sử Dụng Mã Code Sau 15P-2H Vì Code Sẽ Được Duyệt"
        )
        code_data = f"{code_name}:{amount}:1:False\n"
        with open('code.txt', 'a') as file:
            file.write(code_data)
        query.edit_message_text(text="Yêu cầu đổi tiền đã được phê duyệt.")
    elif action == "reject":
        refund_amount = amount + int(amount * 0.1)
        update_user_balance(user_id, refund_amount)
        context.bot.send_message(
            chat_id=user_id,
            text=
            f"Yêu cầu đổi tiền của bạn đã bị từ chối. Số tiền {format_currency(refund_amount)} đã được hoàn trả vào tài khoản của bạn."
        )
        query.edit_message_text(text="Yêu cầu đổi tiền đã bị từ chối.")
def format_currency(amount):
    return f"{amount:,} VND"

@restrict_room
def start_lottery(update: Update, context: CallbackContext):
    global lottery_active, lottery_bets, lottery_timer

    if lottery_active:
        update.message.reply_text("Trò chơi Xổ Số đang diễn ra! Vui lòng đợi đến khi kết thúc để tham gia.")
        return

    lottery_active = True
    lottery_bets = {}
    lottery_timer = 50

    update.message.reply_text(
        "🎫 Trò chơi Xổ Số đã bắt đầu! 🎫\n\n"
        "Lệnh cược: /mua <số tiền> <loại cược> <giá trị cược>\n\n"
        "Loại cược:\n"
        "+ T/X - Tài / Xỉu (T hoặc X)\n"
        "+ C/L - Chẵn / Lẻ (C hoặc L)\n"
        "+ S2 - Số chính xác 2 số đầu (ví dụ: 12)\n"
        "+ S3 - Số chính xác 3 số đầu (ví dụ: 123)\n"
        "+ S4 - Số chính xác 4 số đầu (ví dụ: 1234, X1000)\n\n"
        f"⏳ Còn {lottery_timer} giây để đặt cược ⏳"
    )

    threading.Thread(target=start_lottery_timer, args=(update, context)).start()
def start_lottery_timer(update: Update, context: CallbackContext):
    global lottery_timer

    while lottery_timer > 0:
        time.sleep(1)
        lottery_timer -= 1
        if lottery_timer % 10 == 0:
            update.message.reply_text(f"⏳ Còn {lottery_timer} giây để đặt cược ⏳")

    update.message.reply_text("⏳ Hết thời gian đặt cược! ⏳")
    draw_lottery_result(update, context)
def place_lottery_bet(update: Update, context: CallbackContext):
    global lottery_bets, lottery_active, lottery_timer

    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return

    if not lottery_active:
        update.message.reply_text("Hiện không có trò chơi Xổ Số nào đang diễn ra.")
        return

    args = context.args
    if len(args) < 3:
        update.message.reply_text("Sử dụng: /mua <số tiền> <loại cược> <giá trị cược>")
        return

    try:
        bet_amount = int(args[0])
        bet_type = args[1].upper()
        bet_value = args[2]
    except ValueError:
        update.message.reply_text("Số tiền cược phải là một số nguyên.")
        return

    if bet_amount <= 0 or bet_type not in ['T', 'X', 'C', 'L', 'S2', 'S3', 'S4']:
        update.message.reply_text("Số tiền cược hoặc loại cược không hợp lệ.")
        return

    if user_balances.get(user_id, 0) < bet_amount:
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    if lottery_timer == 0:
        update.message.reply_text("Hết thời gian đặt cược. Vui lòng chờ đợi kết quả.")
        return

    if bet_type in ['S2', 'S3', 'S4']:
        if not bet_value.isdigit() or len(bet_value) != int(bet_type[-1]):
            update.message.reply_text(f"Giá trị cược cho {bet_type} phải là số có {bet_type[-1]} chữ số.")
            return

    if user_id not in lottery_bets:
        lottery_bets[user_id] = []

    lottery_bets[user_id].append((bet_amount, bet_type, bet_value))
    update.message.reply_text(f"Bạn đã đặt cược {format_currency(bet_amount)} vào {bet_type} {bet_value}!")

    user_balances[user_id] -= bet_amount
def draw_lottery_result(update: Update, context: CallbackContext):
    global lottery_active, lottery_bets

    if not lottery_active:
        update.message.reply_text("Hiện không có trò chơi Xổ Số nào đang diễn ra.")
        return

    lottery_active = False

    lottery_numbers = [random.randint(1, 6) for _ in range(5)]
    total_sum = sum(lottery_numbers[-3:])
    last_digit = lottery_numbers[-1]
    is_odd = last_digit % 2 != 0

    lottery_number_str = ''.join(map(str, lottery_numbers))

    update.message.reply_text(
        "🎫 Kết quả xổ số 🎫\n"
        f"Số xổ: {lottery_number_str}\n"
        f"Tổng 3 số cuối: {total_sum}\n"
        f"Số cuối: {last_digit} ({'Lẻ' if is_odd else 'Chẵn'})"
    )

    winners = {}
    for user_id, bets in lottery_bets.items():
        user_total_winnings = 0
        for bet_amount, bet_type, bet_value in bets:
            if bet_type == 'T' and 11 <= total_sum <= 18:
                user_total_winnings += bet_amount * 1.95
            elif bet_type == 'X' and 3 <= total_sum <= 10:
                user_total_winnings += bet_amount * 1.95
            elif bet_type == 'C' and not is_odd:
                user_total_winnings += bet_amount * 1.95
            elif bet_type == 'L' and is_odd:
                user_total_winnings += bet_amount * 1.95
            elif bet_type == 'S2' and bet_value == lottery_number_str[:2]:
                user_total_winnings += bet_amount * 99
            elif bet_type == 'S3' and bet_value == lottery_number_str[:3]:
                user_total_winnings += bet_amount * 999
            elif bet_type == 'S4' and bet_value == lottery_number_str[:4]:
                user_total_winnings += bet_amount * 99999 

        if user_total_winnings != 0:
            winners[user_id] = user_total_winnings

    result_message = "Kết quả cược:\n"
    if len(winners) == 0:
        result_message += "Không có người chơi nào thắng cược!"
    else:
        result_message += "Người chơi - Tiền thắng\n"
        for user_id, amount_won in winners.items():
            update_user_balance(user_id, amount_won)
            result_message += f"{user_id} - {format_currency(amount_won)}\n"

    update.message.reply_text(result_message)
    lottery_bets.clear()
def leave_group(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    if user_id != 6793700101:
        update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    context.bot.leave_chat(chat_id)
def load_phien_number():
    try:
        with open("phien.txt", "r") as file:
            phien_number = int(file.read().strip())
    except FileNotFoundError:
        phien_number = 0
    return phien_number

def save_phien_number(phien_number):
    with open("phien.txt", "w") as file:
        file.write(str(phien_number))
@retry_on_failure(retries=3, delay=5)
def start_taixiu(update, context):
    global taixiu_game_active, taixiu_bets, taixiu_timer, recent_results 

    phien_number = load_phien_number()

    if taixiu_game_active:
        context.bot.send_message(
            chat_id=TAIXIU_GROUP_ID,
            text=(
                f"⏳ Phiên {phien_number}. Còn {taixiu_timer}s để đặt cược ⏳\n\n"
                f"✅ Lệnh Cược : T/X dấu cách Cược/Max ✅\n\n"
                f"⚫️ Cửa Tài : {len([bets for bets in taixiu_bets.values() for choice, _ in bets if choice == 'T'])} lượt đặt. Tổng tiền {sum(amount for bets in taixiu_bets.values() for choice, amount in bets if choice == 'T')} ₫\n\n"
                f"⚪️ Cửa Xỉu : {len([bets for bets in taixiu_bets.values() for choice, _ in bets if choice == 'X'])} lượt đặt. Tổng tiền {sum(amount for bets in taixiu_bets.values() for choice, amount in bets if choice == 'X')} ₫\n\n"
                f"💰 Hũ hiện tại : /jackpot 💰\n\n"
                f"📋 Kết quả 10 phiên gần nhất :\n{format_recent_results()}"
            )
        )
        return

    taixiu_game_active = True
    taixiu_bets = {}
    taixiu_timer = 39

    context.bot.send_message(
        chat_id=TAIXIU_GROUP_ID,
        text=(
            f"🎲 Trò chơi Tài Xỉu đã bắt đầu! 🎲\n\n"
            f"✅ Lệnh Cược : T/X dấu cách Cược/Max ✅\n\n"
            f"💰 Hũ hiện tại : /jackpot 💰\n\n"
            f"⏳ Còn {taixiu_timer}s để đặt cược ⏳\n\n"
            f"📋 Kết quả 10 phiên gần nhất :\n{format_recent_results()}"
        )
    )

    threading.Thread(target=start_taixiu_timer, args=(update, context)).start()

@retry_on_failure(retries=3, delay=5)
def start_taixiu_timer(update, context):
    global taixiu_timer
    while taixiu_timer > 0:
        time.sleep(1)
        taixiu_timer -= 1
        if taixiu_timer % 10 == 0:
            phien_number = load_phien_number()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"⏳ Phiên {phien_number}. Còn {taixiu_timer}s để đặt cược ⏳\n\n"
                    f"✅ Lệnh Cược : T/X dấu cách Cược/Max ✅\n\n"
                    f"⚫️ Cửa Tài : {len([bets for bets in taixiu_bets.values() for choice, _ in bets if choice == 'T'])} lượt đặt. Tổng tiền {sum(amount for bets in taixiu_bets.values() for choice, amount in bets if choice == 'T')} ₫\n\n"
                    f"⚪️ Cửa Xỉu : {len([bets for bets in taixiu_bets.values() for choice, _ in bets if choice == 'X'])} lượt đặt. Tổng tiền {sum(amount for bets in taixiu_bets.values() for choice, amount in bets if choice == 'X')} ₫\n\n"
                    f"💰 Hũ hiện tại : /jackpot 💰\n\n"
                    f"📋 Kết quả 10 phiên gần nhất :\n{format_recent_results()}"
                )
            )

    phien_number = load_phien_number()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f"⌛️ Hết thời gian đặt cược! \n\n"
            f"🎲🎲🎲 BOT CHUẨN BỊ TUNG XÚC XẮC 🎲🎲🎲\n\n"
        )
    )
    lock_chat(context, update.effective_chat.id)
    generate_taixiu_result(update, context)

def taixiu1(update, context):
    global taixiu_bets, taixiu_game_active, taixiu_timer, jackpot_amount

    if not update.message:
        return

    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    if update.effective_chat.id != -1002178971014 and update.effective_chat.type != "private":
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hãy tham gia vào nhóm mới để chơi: t.me/ztrongzroom"
        )
        return

    if user_id in banned_users:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Bạn không được phép sử dụng bot."
        )
        return

    message_text = update.message.text.strip().split()

    if len(message_text) != 2:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Vui lòng nhập theo định dạng: [T/X] [số tiền cược]"
        )
        return

    choice = message_text[0].upper()
    bet_amount_str = message_text[1].lower()

    if choice not in ['T', 'X']:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Chỉ chấp nhận 'T' hoặc 'X' là lựa chọn."
        )
        return

    if bet_amount_str == 'max':
        bet_amount = user_balances.get(user_id, 0)
    else:
        try:
            bet_amount = int(bet_amount_str)
        except ValueError:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Số tiền cược phải là một số nguyên hoặc 'MAX'."
            )
            return

    if bet_amount <= 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Số tiền cược không hợp lệ."
        )
        return
    if bet_amount < 1000:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Số tiền cược phải lớn hơn hoặc bằng 1000."
        )
        return

    if user_balances.get(user_id, 0) < bet_amount:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Số dư của bạn không đủ để đặt cược."
        )
        return

    if taixiu_timer == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⏳ Không phải trong thời gian cược ⏳"
        )
        return

    if user_id in taixiu_bets:
        existing_bets = taixiu_bets[user_id]
        if any(existing_choice != choice for existing_choice, _ in existing_bets):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Bạn chỉ được đặt cược vào một cửa (T hoặc X)."
            )
            return

    try:
        context.bot.send_message(
            chat_id=user_id,
            text=f"Bạn vừa cược {format_currency(bet_amount)} vào cửa {'Tài' if choice == 'T' else 'Xỉu'} trong room."
        )
    except Exception as e:
        username = f"@{update.message.from_user.username}" if update.message.from_user.username else f"ID {user_id}"
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"🚫 Không Thể Cược Vì User Chưa Có Contact Với Bot\n🌐 {username} Vui Lòng Nhắn Bot @ztrongzroom_bot 🌐"
        )
        return

    if user_id not in taixiu_bets:
        taixiu_bets[user_id] = []

    taixiu_bets[user_id].append((choice, bet_amount))

    chat_type = update.message.chat.type
    if chat_type == "private":
        context.bot.send_message(
            chat_id=-1002178971014,
            text=f"✅ Ẩn Danh đã đặt cược {format_currency(bet_amount)} vào {choice}!",
        )
    else:
        context.bot.send_message(
            chat_id=-1002178971014,
            text=f"✅ {user_name} đã đặt cược {format_currency(bet_amount)} vào {choice}!",
        )
        context.bot.send_message(
            chat_id=-1002066327546,
            text=f"✅𝙕𝙍𝙤𝙤𝙢✅Vừa có user đặt cược : {'Tài' if choice == 'T' else 'Xỉu'}",
        )

    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    user_balances[user_id] -= bet_amount


@retry_on_failure(retries=3, delay=5)
def end_taixiu(update, context):
    global taixiu_game_active

    if not taixiu_game_active:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sử Dụng /phien"
        )
        return

    taixiu_game_active = False

    tai_bet_count = sum(1 for bets in taixiu_bets.values() for choice, _ in bets if choice == 'T')
    tai_total_bet = sum(amount for bets in taixiu_bets.values() for choice, amount in bets if choice == 'T')
    xiu_bet_count = sum(1 for bets in taixiu_bets.values() for choice, _ in bets if choice == 'X')
    xiu_total_bet = sum(amount for bets in taixiu_bets.values() for choice, amount in bets if choice == 'X')


    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f"⌛️ Hết thời gian đặt cược! \n\n"
            f"🎲🎲🎲 BOT CHUẨN BỊ TUNG XÚC XẮC 🎲🎲🎲\n\n"
        )
    )

def generate_taixiu_result(update, context):
    global taixiu_game_active, taixiu_bets, recent_results, jackpot_amount

    if taixiu_game_active:
        taixiu_game_active = False

    phien_number = load_phien_number()
    save_phien_number(phien_number + 1)
    
    time.sleep(3)
    dice1 = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value
    time.sleep(2)
    dice2 = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value
    time.sleep(2)
    dice3 = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value
    dice_values = [dice1, dice2, dice3]
    total = sum(dice_values)
    time.sleep(4)
    result_message = (
        f"📝 Kết quả cược phiên: {phien_number} | {dice1}-{dice2}-{dice3}\n\n"
    )

    if total >= 11:
        result_message += "💰 Cửa thắng : ⚫️ Tài\n\n"
    else:
        result_message += "💰 Cửa thắng : ⚪️ Xỉu\n\n"

    winners = {}
    special_case = False

    if dice1 == dice2 == dice3 == 1:
        special_case = True
        result_message += f"🎉🎉🎉 NỔ HŨ {dice1}-{dice2}-{dice3} 🎉🎉🎉\n\n"
        context.bot.send_message(
            chat_id=-1002066327546,
            text="🎉🎉🎉 NỔ HŨ 🎉🎉🎉\n\nHŨ JACKPOT VỪA NỔ KÌA MỌI NGƯỜI\nhttps://t.me/ztrongzroomtaixiu vào húp diii"
        )
        pinned_message = context.bot.send_message(chat_id=update.effective_chat.id, text=result_message)
        context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=pinned_message.message_id,
                                     disable_notification=True)
    elif dice1 == dice2 == dice3 == 6:
        special_case = True
        result_message += f"🎉🎉🎉 NỔ HŨ {dice1}-{dice2}-{dice3} 🎉🎉🎉\n\n"
        context.bot.send_message(
            chat_id=-1002066327546,
            text="🎉🎉🎉 NỔ HŨ 🎉🎉🎉\n\nHŨ JACKPOT VỪA NỔ KÌA MỌI NGƯỜI\nhttps://t.me/ztrongzroom vào húp diii"
        )
        context.bot.send_message(
            chat_id=-1002143818260,
            text="🎉🎉🎉 NỔ HŨ 🎉🎉🎉\n\nHŨ JACKPOT VỪA NỔ KÌA MỌI NGƯỜI\nhttps://t.me/ztrongzroom vào húp diii"
        )
        pinned_message = context.bot.send_message(chat_id=update.effective_chat.id, text=result_message)
        context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=pinned_message.message_id,
                                     disable_notification=True)

    for user_id, bets in taixiu_bets.items():
        user_total_winnings = 0
        for choice, amount in bets:
            if special_case:
                user_total_winnings += amount
            elif choice == 'T' and total >= 11:
                user_total_winnings += amount * 1.95
            elif choice == 'X' and total <= 10:
                user_total_winnings += amount * 1.95
        if user_total_winnings > 0:
            winners[user_id] = user_total_winnings

    if special_case:
        if winners:
            share_amount = jackpot_amount / len(winners)
            for user_id in winners.keys():
                winners[user_id] += share_amount
            result_message += "💰 Jackpot đã được chia đều cho tất cả những người thắng cược!\n\n"
        else:
            result_message += "Rất Tiếc Là Không Có Ai Thắng Hũ, Hũ Trả Về 0 !\n\n"
        jackpot_amount = 0
    else:
        if len(winners) == 0:
            result_message += "Không có người chơi nào thắng cược !\n\n"
        else:
            for user_id, amount_won in winners.items():
                update_user_balance(user_id, amount_won)
                try:
                    context.bot.send_message(
                        chat_id=user_id,
                        text=f"{'Thắng' if amount_won > 0 else 'Thua'} Room ! Bạn đã {'thắng' if amount_won > 0 else 'thua'} {format_currency(amount_won)}!"
                    )
                except telegram.error.Unauthorized:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Không thể gửi tin nhắn cho <a href='tg://user?id={user_id}'>người chơi</a>, hãy nhắn bot để nhận kết quả."
                    )
            result_message += "✅ TOP - ID - Tiền thắng ✅\n"
            for rank, (user_id, amount_won) in enumerate(sorted(winners.items(), key=lambda x: x[1], reverse=True),
                                                            1):
                result_message += f"{rank} - {user_id} - {format_currency(amount_won)}\n"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=result_message
    )
    recent_results.append((dice_values[0], dice_values[1], dice_values[2], total))
    save_recent_results()
    time.sleep(2)
    unlock_chat(context, update.effective_chat.id)

    keyboard = [[InlineKeyboardButton("✅ Nạp Xu ✅", callback_data='nap_xu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=("🎲 Vui Lòng Đợi 10 Giây Để Mở Phiên Mới 🎲\n💠 Các Đại Gia Vui Lòng Vào Tiền Nhẹ 💠"),
        reply_markup=reply_markup
    )
    time.sleep(10)

    save_phien_number(phien_number + 1)

    start_taixiu(update, context)


def nap_xu(update, context):
    user_id = update.message.from_user.id  
    message = (
        f"<b>Yêu Cầu Nạp Xu :</b>\n\n"
        f"<b>Giá Xu : </b> /nap\n"
        f"<b>🧧 MOMO (DUYỆT NHANH)</b>\n"
        f"👉 <code>0909743280</code>\n"
        f"(CLICK ĐỂ COPY)\n\n"
        f"<b>🧧 THESIEURE</b>\n"
        f"👉 <code>0909743280</code>\n"
        f"(CLICK ĐỂ COPY)\n\n"
        f"<b>🧧 TECHCOMBANK (CHẬM)</b>\n"
        f"👉 <code>19072344534014</code>\n"
        f"(CLICK ĐỂ COPY)\n\n"
        f"<b>Nội Dung:</b> <code>{user_id}</code>"
    )
    update.message.reply_text(message, parse_mode='HTML')  



def load_recent_results():
    global recent_results
    try:
        with open("kqphientx.txt", "r") as file:
            recent_results = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        recent_results = []


def save_recent_results():
    global recent_results
    with open("kqphientx.txt", "w") as file:
        for result in recent_results:
            if all(isinstance(x, int) for x in result[:3]):
                if result[:3] == (1, 1, 1):
                    file.write("🟢 Bão\n")
                elif result[:3] == (6, 6, 6):
                    file.write("🟡 Bão\n")
                else:
                    total = sum(result[:3])
                    file.write(f"{'⚫️ Tài' if total >= 11 else '⚪️ Xỉu'}\n")


def format_recent_results():
    global recent_results
    recent_results_slice = recent_results[-10:]
    formatted_results = []

    for result in recent_results_slice:
        if all(isinstance(x, int) for x in result[:3]):
            if result[:3] == (1, 1, 1):
                formatted_results.append("🟢")
            elif result[:3] == (6, 6, 6):
                formatted_results.append("🟡")
            else:
                total = sum(result[:3])
                formatted_results.append(f"{'⚫️' if total >= 11 else '⚪️'}")

    return " ".join(formatted_results)



def format_currencyshaa(amount):
    return f"{amount:,} K"

def load_verified_users():
    try:
        with open(VERIFIED_USERS_FILE, 'r') as file:
            return set(int(line.strip()) for line in file)
    except FileNotFoundError:
        return set()

def save_verified_user(user_id):
    with open(VERIFIED_USERS_FILE, 'a') as file:
        file.write(f"{user_id}\n")

verified_users = load_verified_users()

def addrut(update: Update, context: CallbackContext):
    if update.message.from_user.id not in [6793700101, ADMIN_ID]:
        update.message.reply_text("❌ Bạn không có quyền thêm người dùng vào danh sách rút tiền. ❌")
        return

    args = context.args
    if len(args) != 1:
        update.message.reply_text("❌ Bạn phải cung cấp ID người dùng để thêm vào danh sách rút tiền. ❌")
        return

    try:
        user_id = int(args[0])
        if user_id in verified_users:
            update.message.reply_text("❌ Người dùng này đã có quyền rút tiền. ❌")
            return

        verified_users.add(user_id)
        save_verified_user(user_id)
        update.message.reply_text(f"✅ User {user_id} đã được thêm vào danh sách rút tiền. ✅")
    except ValueError:
        update.message.reply_text("❌ ID người dùng không hợp lệ. ❌")

def rutmomo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id  
    ADMIN_ID = 6793700101  

    if user_id not in verified_users:
        update.message.reply_text("❌ Bạn chưa được phê duyệt để rút tiền. Vui lòng liên hệ admin. ❌")
        return

    args = context.args
    if len(args) == 0:
        update.message.reply_text(
            "🏦 Bảng Quy Đổi Xu Sang Tiền Thật 🏦\n\n"
            "💳 10BB = 10K 💳\n"
        )
        return
    if len(args) < 2:
        update.message.reply_text("💳 Bạn phải cung cấp cả số tiền và số tài khoản Momo 💳")
        return
    try:
        amount = int(args[0])
        if amount < 10000000000000000000: 
            update.message.reply_text("💳 Số tiền phải lớn hơn hoặc bằng 10BB. 💳")
            return
        if user_id not in user_balances:
            user_balances[user_id] = 0

        if amount > user_balances[user_id]:
            update.message.reply_text("💳 Số dư không đủ để thực hiện giao dịch. 💳")
            return
        momo_account = args[1]
        converted_amount = amount / 10000000000000000000 
        user_balances[user_id] -= amount
        pending_transactions[user_id] = {
            'amount': amount,
            'converted_amount': converted_amount,
            'momo_account': momo_account
        }
        update.message.reply_text(
            f"🔄 Lệnh Đổi Của Bạn Đang Được Xử Lý 🔄\n"
            f"🔄 Số tiền đã đổi: {format_currencyshaa(converted_amount)} 🔄\n"  
            f"🔄 STK Momo: {momo_account} 🔄\n\n"
            f"Chờ xác nhận từ admin..."
        )
        admin_message = (
            f"User có ID {update.message.from_user.id} Đã Rút {format_currencyshaa(converted_amount)} Ra Tài Khoản {momo_account}"
        )
        context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
        context.chat_data['user_id'] = update.message.from_user.id
        context.chat_data['momo_account'] = momo_account
        context.chat_data['converted_amount'] = converted_amount
    except ValueError:
        update.message.reply_text("💳 Số tiền không hợp lệ. 💳")

def duyetchuyen(update: Update, context: CallbackContext):
    global pending_transactions

    if update.message.from_user.id not in [6793700101, ADMIN_ID]:
        update.message.reply_text("❌ Bạn không có quyền duyệt giao dịch này. ❌")
        return

    args = context.args
    if len(args) != 1:
        update.message.reply_text("❌ Bạn phải cung cấp ID người dùng để duyệt giao dịch. ❌")
        return

    try:
        user_id = int(args[0])
        if user_id not in pending_transactions:
            update.message.reply_text("❌ Không tìm thấy GD đang chờ duyệt cho người dùng này. ❌")
            return

        transaction = pending_transactions.pop(user_id)
        update.message.reply_text(
            f"✅ Giao dịch của User {user_id} đã được duyệt. Số tiền {format_currencyshaa(transaction['converted_amount'])} đã được chuyển. ✅"
        )
        context.bot.send_message(chat_id=user_id, text=f"✅ Giao dịch của bạn đã được duyệt. Số tiền {format_currencyshaa(transaction['converted_amount'])} đã được chuyển vào tài khoản Momo của bạn. ✅")

        group_message = (
            f"✅ User có ID {user_id} đã rút {format_currencyshaa(transaction['converted_amount'])} về tài khoản {transaction['momo_account']} ✅"
        )
        context.bot.send_message(chat_id=GROUP_CHAT_ID, text=group_message)

    except ValueError:
        update.message.reply_text("❌ ID người dùng không hợp lệ. ❌")

def huychuyen(update: Update, context: CallbackContext):
    if update.message.from_user.id not in [6793700101, ADMIN_ID]:
        update.message.reply_text("❌ Bạn không có quyền hủy giao dịch này. ❌")
        return

    args = context.args
    if len(args) != 1:
        update.message.reply_text("❌ Bạn phải cung cấp ID người dùng để hủy giao dịch. ❌")
        return

    try:
        user_id = int(args[0])
        if user_id not in pending_transactions:
            update.message.reply_text("❌ Không tìm thấy giao dịch đang chờ duyệt cho người dùng này. ❌")
            return

        transaction = pending_transactions.pop(user_id)
        user_balances[user_id] += transaction['amount']
        update.message.reply_text(
            f"❌ Giao dịch của User {user_id} đã bị hủy. Số tiền {format_currencyshaa(transaction['amount'])} đã được hoàn lại. ❌"
        )
    except ValueError:
        update.message.reply_text("❌ ID người dùng không hợp lệ. ❌")

@restrict_room
def idme(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    update.message.reply_text(f"🆔 ID Của Bạn Là: `{user_id}`", parse_mode='MarkdownV2')

@restrict_room
def idme_on_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    if "idme" in text:
        user_id = update.message.from_user.id
        update.message.reply_text(f"🆔 ID Của Bạn Là: `{user_id}`", parse_mode='MarkdownV2')
def load_user_balancess(file_path):
    user_balances = {}
    with open(file_path, 'r') as file:
        for line in file:
            user_id, balance = line.strip().split(':')
            if balance == 'inf':
                balance = '100000000000000000000000'  
            user_balances[user_id] = float(balance)
    return user_balances

@restrict_room
def top(update, context):
    try:
        user_balances = load_user_balancess('sodu.txt')
    except Exception as e:
        update.message.reply_text(f"Đã xảy ra lỗi khi đọc file sodu.txt: {str(e)}")
        return
    sorted_balances = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)

    top_users = sorted_balances[:10]  

    message = "🌐 Top 10 người dùng có số dư cao nhất 🌐 :\n"
    for i, (user_id, balance) in enumerate(top_users, start=1):
        message += f"TOP {i} : User ID: {user_id}\n✅ Số dư: {balance} ✅\n\n"

    update.message.reply_text(message)

def load_huloc():
    with open("huloc.txt", "r") as file:
        return int(file.read())

def save_huloc(amount):
    with open("huloc.txt", "w") as file:
        file.write(str(amount))
@restrict_room
def hailoc(update, context):
    user_id = update.message.from_user.id
    bet_amount = int(context.args[0]) if context.args else 0
    if bet_amount <= 0:
        update.message.reply_text("Số tiền cược không hợp lệ.")
        return

    if bet_amount > user_balances.get(user_id, 0):
        update.message.reply_text("Số dư của bạn không đủ để đặt cược.")
        return

    if bet_amount < 10000:
        update.message.reply_text("Chỉ Nhận Cược Trên 10,000 VND")
        return


    choices = ["x2", "x5", "hoan", "huloc", "thua", "thua", "thua", "thua", "thua", "thua", "thua"]
    result = random.choice(choices)

    if result == "x2":
        amount_won = bet_amount * 2
        update_user_balance(user_id, amount_won)
        update.message.reply_text(f"🧧 Chúc mừng! Bạn đã thắng X2 : {format_currency(amount_won)} 🧧")
    if result == "x5":
        amount_won = bet_amount * 5
        update_user_balance(user_id, amount_won)
        update.message.reply_text(f"🧧 Chúc mừng! Bạn đã thắng X5 : {format_currency(amount_won)} 🧧")
    elif result == "hoan":
        update_user_balance(user_id, bet_amount)
        update.message.reply_text(f"💸 Kết quả là 'Hoàn'. Số tiền cược {format_currency(bet_amount)} đã được hoàn trả 💸")
    elif result == "huloc":
        huloc_amount = load_huloc()
        update_user_balance(user_id, huloc_amount + bet_amount)
        save_huloc(0) 
        update.message.reply_text(f"🍀 Chúc mừng! Bạn đã thắng hũ lộc trị giá {format_currency(huloc_amount)} và {format_currency(bet_amount)} từ cược 🍀")
    else:  
        amount_lost = bet_amount
        huloc_amount = load_huloc()
        update_user_balance(user_id, -amount_lost) 
        save_huloc(huloc_amount + amount_lost / 100)  
        update.message.reply_text(f"💰 Tiếc quá! Bạn đã thua {format_currency(amount_lost)}. Số tiền đã được chia 100 và thêm vào hũ lộc 💰")

    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id) 

@restrict_private_chats
def huloc(update, context):
    global huloc_amount

    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return

    if 'huloc_amount' not in globals():
        huloc_amount = 0

    huloc_default_amount = load_huloc()

    if huloc_amount > huloc_default_amount:
        huloc_amount = huloc_default_amount
        save_huloc(huloc_amount)  

    update.message.reply_text(
        f"💰 Số tiền hiện có trong Hũ Lộc là:\n\n💰 {format_currency(huloc_default_amount)} 💰"
    )
def guitb(update, context):
    message = ' '.join(context.args)

    if update.message.from_user.id == 6793700101:
        context.bot.send_message(chat_id=-1002066327546, text=message)
        update.message.reply_text("Đã gửi tin nhắn thành công!")
    else:
        update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này! ❌")
group_chat_id = -1002066327546
def cuocevent(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    args = context.args

    if len(args) != 1:
        update.message.reply_text("Sử dụng: /cuocevent <T / X / C / L>")
        return

    choice = args[0].upper()
    if choice not in ['T', 'X', 'C', 'L']:
        update.message.reply_text("Lựa chọn không hợp lệ. Vui lòng chọn T/X/C/L.")
        return

    context.bot.send_message(
        chat_id=group_chat_id,
        text=f"User @{username} (ID: {user_id}) đã cược {choice}."
    )

    update.message.reply_text(f"Bạn đã cược {choice}. Thông tin cược đã được gửi vào nhóm.")
def xx(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    args = context.args
    if len(args) == 3:
        try:
            dice1 = int(args[0])
            dice2 = int(args[1])
            dice3 = int(args[2])
        except ValueError:
            update.message.reply_text("Please provide valid integers for the dice values.")
            return
    else:
        dice1 = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value
        time.sleep(1)
        dice2 = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value
        time.sleep(1)
        dice3 = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value

    dice_values = [dice1, dice2, dice3]
    total = sum(dice_values)

    if total in [3, 18]:
        update.message.reply_text("Luck Tốt Đấy")
    else:
        return        
def clear_file(update, context):
    try:
        with open("sodu.txt", "w") as file:
            file.truncate(0)  
        with open("code.txt", "w") as file:
            file.truncate(0)  
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🗑️ File đã được dọn sạch."
        )
    except Exception as e:
        print(e) 


def mophien_command(update, context):
    global mophien
    chat_id = update.message.chat_id
    if chat_id == -1002178971014: 
        mophien = True
        start_taixiu(update, context)
    elif chat_id != -1002178971014:
        update.message.reply_text("Lệnh này chỉ có thể được sử dụng trong nhóm @ztrongzroom")
    else:
        update.message.reply_text("Bạn không có quyền thực hiện lệnh này!")


def run_taixiu_if_enabled(update, context):
    global mophien
    if mophien == True:
        start_taixiu(update, context)
def profile(update, context):
    user = update.effective_user
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    mention = user.mention_html()

    if user_id in user_balances:
        balance = user_balances[user_id]
    else:
        balance = "Không có thông tin"

    uid_link = f"<a href='tg://user?id={user_id}'>{user_id}</a>"

    try:
        with open("ver_rut.txt", "r") as file:
            verified_users = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        verified_users = []

    if str(user_id) in verified_users:
        rut_status = "✅ Đã có thể rút ✅"
    else:
        rut_status = "⛔️ Chưa được duyệt rút ⛔️"

    profile_text = (
        f"┌─┤Thông tin người dùng├──⭓\n"
        f"├Tên : {first_name} {last_name}\n"
        f"├UID : {uid_link}\n"  
        f"├Username : @{username}\n"
        f"├Số Dư : {format_currency(balance)} 💵\n"
        f"├Rút : {rut_status}\n"
        f"└───────────────⭓"
    )

    update.message.reply_html(profile_text, disable_web_page_preview=True)

@restrict_room
def napthe(update, context):
    user_id = update.message.from_user.id
    if user_id in banned_users:
        update.message.reply_text("Bạn không được phép sử dụng bot.")
        return

    if len(context.args) != 4:
        update.message.reply_text("Vui lòng cung cấp đầy đủ thông tin: /napthe <Seri> <Card> <Nhà Mạng> <Mệnh Giá>")
        return

    seri, card, nha_mang, menh_gia = context.args

    if nha_mang.lower() not in ['viettel', 'vinaphone', 'mobiphone', 'vietnamobile']:
        update.message.reply_text("Nhà mạng không hợp lệ. Vui lòng chọn trong [Viettel, Vinaphone, Mobiphone, Vietnamobile].")
        return

    if menh_gia not in MENH_GIA:
        update.message.reply_text("Mệnh giá không hợp lệ.")
        return

    admin_message = (
        f"<b>Yêu cầu nạp thẻ mới:</b>\n"
        f"<b>Người dùng:</b> {update.message.from_user.full_name}\n"
        f"<b>Seri:</b> {seri}\n"
        f"<b>Card:</b> {card}\n"
        f"<b>Nhà mạng:</b> {nha_mang}\n"
        f"<b>Mệnh giá:</b> {menh_gia}\n\n"
        f"<i>User ID = {user_id} </i>"
    )

    context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode='HTML')
    update.message.reply_text("Yêu cầu của bạn đã được gửi. Vui lòng đợi phản hồi từ admin tới bạn.")

def gui(update, context):
    if len(context.args) < 2:
        update.message.reply_text("Sử dụng: /gui <nội dung> <ID người dùng>")
        return

    message_text = ' '.join(context.args[:-1])
    user_id = context.args[-1]

    try:
        user_id = int(user_id)  
    except ValueError:
        update.message.reply_text("ID người dùng không hợp lệ.")
        return

    context.bot.send_message(chat_id=user_id, text=message_text)
    update.message.reply_text("Đã gửi tin nhắn đến người dùng.")

def checkbox(update, context):
    message = "📋 Các nhóm Telegram mà bot đã tham gia:\n\n"
    for chat_id, chat_info in joined_groups.items():
        message += f"ID: {chat_id}\n"
        if chat_info['type'] == 'public':
            message += f"Link: {chat_info.get('link', 'N/A')}\n"
        message += "\n"
    update.message.reply_text(message)

def load_joined_groups():
    try:
        with open("joined_groups.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_joined_groups():
    with open("joined_groups.json", "w") as file:
        json.dump(joined_groups, file)


def leave(update, context):
    user_id = update.message.from_user.id
    if user_id not in [6793700101,123123123]:
        update.message.reply_text("Cút")
        return
    if not context.args:
        update.message.reply_text("Sử dụng: /leave <id_nhóm>")
        return
    chat_id_to_leave = int(context.args[0])
    if chat_id_to_leave in joined_groups:
        context.bot.send_message(chat_id_to_leave, "Bot đã rời khỏi nhóm này theo yêu cầu của quản trị viên.")
        context.bot.leave_chat(chat_id_to_leave)
        del joined_groups[chat_id_to_leave]
        update.message.reply_text(f"Bot đã rời khỏi nhóm có ID {chat_id_to_leave}.")
    else:
        update.message.reply_text("Bot không tham gia nhóm có ID này.")

def leave_all_chats(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in [6793700101, 123123123]:
        update.message.reply_text("Bạn không có quyền thực hiện lệnh này.")
        return

    chat_ids = []
    for chat in context.bot.get_chat_administrators(update.message.chat_id):
        if chat is not None and isinstance(chat, dict) and 'chat' in chat:
            chat_id = chat['chat']['id']
            chat_ids.append(chat_id)

    for chat_id in chat_ids:
        if chat_id > 0:
            context.bot.leave_chat(chat_id)

    update.message.reply_text("Bot đã rời khỏi tất cả các nhóm.")

def join_chat(update, context):
    chat_id = update.message.chat.id
    chat_title = update.message.chat.title
    chat_link = update.message.chat.invite_link
    chat_type = update.message.chat.type

    joined_groups[chat_id] = {'title': chat_title, 'type': chat_type}
    if chat_type == 'public':
        joined_groups[chat_id]['link'] = chat_link

    save_joined_groups()
def log_group_command(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat_id = update.message.chat_id
    chat_title = update.message.chat.title
    command = update.message.text

    full_name = user.full_name if user.full_name else "N/A"
    username = user.username if user.username else "N/A"
    user_id = user.id

    print(f"{Fore.CYAN}┌─┤{Fore.RED}PHÁT HIỆN{Fore.CYAN}├──⭓")
    print(f"{Fore.CYAN}├{Fore.GREEN} Tên : {Fore.BLUE}{full_name}")
    print(f"{Fore.CYAN}├{Fore.GREEN} UID : {Fore.BLUE}{user_id}")
    print(f"{Fore.CYAN}├{Fore.GREEN} Username : {Fore.BLUE}@{username}")
    print(f"{Fore.CYAN}├{Fore.GREEN} Box : {Fore.BLUE}{chat_title}")
    print(f"{Fore.CYAN}├{Fore.GREEN} Chat ID : {Fore.BLUE}{chat_id}")
    print(f"{Fore.CYAN}├{Fore.GREEN} Nội dung : {Fore.BLUE}{command}")
    print(f"{Fore.CYAN}└───────────────⭓")

def send_to_group(update: Update, context: CallbackContext):
    if not update.message.from_user.id in [6793700101, 123123123]: 
        update.message.reply_text("Bạn không có quyền thực hiện lệnh này!")
        return

    try:
        group_id = int(context.args[0])
        message = ' '.join(context.args[1:])
    except (IndexError, ValueError):
        update.message.reply_text("Sử dụng: /guinhom <id_nhóm> <nội dung>")
        return

    if group_id in groups_info:
        context.bot.send_message(chat_id=group_id, text=message)
        update.message.reply_text("Đã gửi tin nhắn đến nhóm!")
    else:
        update.message.reply_text("Không tìm thấy nhóm!")

def save_group_info(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    title = update.message.chat.title
    groups_info[chat_id] = title

def solo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    if user_id in banned_users:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bạn không được phép sử dụng bot.")
        return

    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sử dụng: /solo <Số xu>")
        return

    bet_amount = context.args[0]

    if bet_amount.lower() == "all":
        bet_amount = user_balances.get(user_id, 0)
    else:
        try:
            bet_amount = int(bet_amount)
        except ValueError:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Số tiền cược phải là một số nguyên hoặc 'all'.")
            return

    if bet_amount < 1000:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Số tiền cược phải > 1.000")
        return

    if user_balances.get(user_id, 0) < bet_amount:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Số dư của bạn không đủ để đặt cược.")
        return

    room_id = random.randint(1000, 9999)
    rooms[room_id] = {
        'host': user_id,
        'bet_amount': bet_amount,
        'opponent': None,
        'host_roll': None,
        'opponent_roll': None,
        'created_at': time.time()
    }
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"🎲 Phòng `{room_id}` đã được tạo với mức cược {format_currency(bet_amount)}.\n"
             f"Chia sẻ mã phòng để mời bạn bè tham gia.\n"
             f"Sử dụng `/join {room_id}` để vào phòng."
    )


def join_solo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    if user_id in banned_users:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bạn không được phép sử dụng bot.")
        return

    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sử dụng: /join <Mã phòng>")
        return

    try:
        room_id = int(context.args[0])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Mã phòng không hợp lệ.")
        return

    if room_id not in rooms:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Phòng không tồn tại.")
        return

    room = rooms[room_id]

    if room['opponent'] is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Phòng đã đầy.")
        return

    if user_balances.get(user_id, 0) < room['bet_amount']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Số dư của bạn không đủ để đặt cược.")
        return

    room['opponent'] = user_id
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Bạn đã tham gia vào phòng `{room_id}` với mức cược {format_currency(room['bet_amount'])}.\n"
             f"Chờ chủ phòng `/roll {room_id}` để bắt đầu trò chơi."
    )
    context.bot.send_message(
        chat_id=room['host'],
        text=f"{user_name} đã tham gia vào phòng của bạn.\n"
             f"Sử dụng `/roll {room_id}` để bắt đầu trò chơi."
    )


def join_solo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    if user_id in banned_users:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bạn không được phép sử dụng bot.")
        return

    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sử dụng: /join <Mã phòng>")
        return

    try:
        room_id = int(context.args[0])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Mã phòng không hợp lệ.")
        return

    if room_id not in rooms:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Phòng không tồn tại.")
        return

    room = rooms[room_id]

    if room['opponent'] is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Phòng đã đầy.")
        return

    if user_balances.get(user_id, 0) < room['bet_amount']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Số dư của bạn không đủ để đặt cược.")
        return

    room['opponent'] = user_id
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Bạn đã tham gia vào phòng {room_id} với mức cược {format_currency(room['bet_amount'])}.\n"
             f"Chờ chủ phòng /roll {room_id} để bắt đầu trò chơi."
    )
    context.bot.send_message(
        chat_id=room['host'],
        text=f"{user_name} đã tham gia vào phòng của bạn.\n"
             f"Sử dụng /roll {room_id} để bắt đầu trò chơi."
    )


def roll(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if user_id in banned_users:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bạn không được phép sử dụng bot.")
        return

    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sử dụng: /roll <Mã phòng>")
        return

    try:
        room_id = int(context.args[0])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Mã phòng không hợp lệ.")
        return

    if room_id not in rooms:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Phòng không tồn tại.")
        return

    room = rooms[room_id]

    if user_id != room['host'] and user_id != room['opponent']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bạn không thuộc phòng này.")
        return

    if user_id == room['host'] and room['host_roll'] is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bạn đã tung xúc xắc rồi.")
        return

    if user_id == room['opponent'] and room['opponent_roll'] is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bạn đã tung xúc xắc rồi.")
        return

    dice_roll = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value

    if user_id == room['host']:
        room['host_roll'] = dice_roll
    else:
        room['opponent_roll'] = dice_roll

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bạn đã tung xúc xắc và được {dice_roll} điểm.")

    if room['host_roll'] is not None and room['opponent_roll'] is not None:
        determine_winner(update, context, room_id)

def determine_winner(update: Update, context: CallbackContext, room_id):
    room = rooms[room_id]
    host_id = room['host']
    opponent_id = room['opponent']
    bet_amount = room['bet_amount']

    if room['host_roll'] > room['opponent_roll']:
        winner_id = host_id
        loser_id = opponent_id
    else:
        winner_id = opponent_id
        loser_id = host_id

    winnings = bet_amount * 1.97
    user_balances[winner_id] += winnings
    user_balances[loser_id] -= bet_amount

    context.bot.send_message(chat_id=host_id, text=f"Kết quả: {room['host_roll']} - {room['opponent_roll']}. Bạn {'thắng' if winner_id == host_id else 'thua'}.")
    context.bot.send_message(chat_id=opponent_id, text=f"Kết quả: {room['host_roll']} - {room['opponent_roll']}. Bạn {'thắng' if winner_id == opponent_id else 'thua'}.")

    del rooms[room_id]

def cancel_solo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if user_id in banned_users:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bạn không được phép sử dụng bot.")
        return

    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sử dụng: /huysolo <Mã phòng>")
        return

    try:
        room_id = int(context.args[0])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Mã phòng không hợp lệ.")
        return

    if room_id not in rooms:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Phòng không tồn tại.")
        return

    room = rooms[room_id]

    if user_id != room['host']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bạn không phải chủ phòng.")
        return

    if room['opponent'] is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Không thể hủy phòng khi đã có người tham gia.")
        return

    if time.time() - room['created_at'] < 120:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Chỉ có thể hủy phòng sau 2 phút tạo phòng.")
        return

    del rooms[room_id]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Phòng đã được hủy.")

def check_solo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if user_id in banned_users:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bạn không được phép sử dụng bot.")
        return

    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sử dụng: /checksolo <Mã phòng>")
        return

    try:
        room_id = int(context.args[0])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Mã phòng không hợp lệ.")
        return

    if room_id not in rooms:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Phòng không tồn tại.")
        return

    room = rooms[room_id]
    host_id = room['host']
    opponent_id = room['opponent']

    if time.time() - room['created_at'] < 120:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Chỉ có thể báo cáo sau 2 phút.")
        return

    if room['host_roll'] is None and room['opponent_roll'] is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Chủ phòng không tung xúc xắc, bị xử thua.")
        user_balances[opponent_id] += room['bet_amount'] * 1.97
        user_balances[host_id] -= room['bet_amount']
        del rooms[room_id]
    elif room['opponent_roll'] is None and room['host_roll'] is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Đối thủ không tung xúc xắc, bị xử thua.")
        user_balances[host_id] += room['bet_amount'] * 1.97
        user_balances[opponent_id] -= room['bet_amount']
        del rooms[room_id]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Không có vi phạm nào được phát hiện.")



def format_tien(amount):
    return '{:,.0f} VND'.format(amount)

@retry_on_failure(retries=3, delay=5)
def start_sicbo(update, context):
    global sicbo_game_active, sicbo_bets, sicbo_timer
    if sicbo_game_active:
        context.bot.send_message(
            chat_id=SICBO_GROUP_ID,
            text=(
                f"⏳ Còn {sicbo_timer}s để đặt cược ⏳\n\n"
                f"✅ Vui lòng nhắn Bet để lấy các cửa cược ✅\n\n"
            )
        )
        return

    sicbo_game_active = True
    sicbo_bets = {}
    sicbo_timer = 9

    context.bot.send_message(
        chat_id=SICBO_GROUP_ID,
        text=(
            f"🎲 Trò chơi Sicbo đã bắt đầu! 🎲\n\n"
            f"✅ Vui lòng nhắn Bet để lấy các cửa cược ✅\n\n"
            f"💰 Hũ hiện tại : /jackpot 💰\n\n"
            f"⏳ Còn {sicbo_timer}s để đặt cược ⏳\n\n"
        )
    )

    threading.Thread(target=start_sicbo_timer, args=(update, context)).start()
@retry_on_failure(retries=3, delay=5)
def start_sicbo_timer(update, context):
    global sicbo_timer
    while sicbo_timer > 0:
        time.sleep(1)
        sicbo_timer -= 1
        if sicbo_timer % 10 == 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"⏳ Còn {sicbo_timer}s để đặt cược ⏳\n\n"
                    f"✅ Vui lòng nhắn Bet để lấy các cửa cược ✅\n\n"
                )
            )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=("⌛️ Hết thời gian đặt cược! \n\n🎲🎲🎲 BOT CHUẨN BỊ TUNG XÚC XẮC 🎲🎲🎲\n\n")
    )
    lock_chat(context, update.effective_chat.id)
    generate_sicbo_result(update, context)
@retry_on_failure(retries=3, delay=5)
def sicbo_bet(update, context):
    global sicbo_bets, sicbo_game_active, sicbo_timer

    if not update.message:
        return

    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    if update.effective_chat.id != -1002172465603:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hãy tham gia vào nhóm mới để chơi: t.me/ztrongzroomsicbo"
        )
        return

    message_text = update.message.text.strip().split()

    if len(message_text) != 3 or not message_text[0] == '/sr':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Vui lòng nhập theo định dạng: /sr <cửa cược> <tiền cược>"
        )
        return

    choice = message_text[1].upper()
    bet_amount_str = message_text[2].lower()

    if choice not in bet_types:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Lựa chọn cửa cược không hợp lệ."
        )
        return

    if bet_amount_str == 'max':
        bet_amount = user_balances.get(user_id, 0)
    else:
        try:
            bet_amount = int(bet_amount_str)
        except ValueError:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Số tiền cược phải là một số nguyên hoặc 'MAX'."
            )
            return

    if bet_amount <= 0 or bet_amount < 1000:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Số tiền cược không hợp lệ hoặc ít hơn 1000."
        )
        return

    if user_balances.get(user_id, 0) < bet_amount:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Số dư của bạn không đủ để đặt cược."
        )
        return

    if sicbo_timer == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⏳ Không phải trong thời gian cược ⏳"
        )
        return


    context.bot.send_message(
        chat_id=user_id,
        text=f"Bạn vừa cược {format_tien(bet_amount)} vào cửa {bet_types[choice]['name']}."
    )

    if user_id not in sicbo_bets:
        sicbo_bets[user_id] = []

    sicbo_bets[user_id].append((choice, bet_amount))

    context.bot.send_message(
        chat_id=-1002172465603,
        text=f"✅ {user_name} đã đặt cược {format_tien(bet_amount)} vào {bet_types[choice]['name']}!"
    )
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    user_balances[user_id] -= bet_amount


@retry_on_failure(retries=3, delay=5)
def generate_sicbo_result(update, context):
    global sicbo_game_active, sicbo_bets, recent_results, jackpot_amount, user_balances

    if sicbo_game_active:
        sicbo_game_active = False

    time.sleep(2)
    dice1 = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value
    time.sleep(2)
    dice2 = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value
    time.sleep(2)
    dice3 = context.bot.send_dice(chat_id=update.effective_chat.id).dice.value
    dice_values = [dice1, dice2, dice3]
    total = sum(dice_values)
    result = "Tài" if 11 <= total <= 18 else "Xỉu"

    recent_results.append(result)
    if len(recent_results) > 10:
        recent_results.pop(0)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Kết quả: {dice_values}  \n🎲🎲🎲Tổng: {total} - {result}🎲🎲🎲"
    )

    for user_id, bets in sicbo_bets.items():
        user_winnings = 0
        for choice, bet_amount in bets:
            bet_type = bet_types.get(choice)
            if bet_type:
                if 'total' in bet_type['condition'].__code__.co_varnames:
                    condition_result = bet_type['condition'](total)
                else:
                    condition_result = bet_type['condition'](dice_values)

                if condition_result:
                    winnings = bet_amount * bet_type['multiplier']
                    user_winnings += winnings
                    context.bot.send_message(
                        chat_id=user_id,
                        text=f"Chúc mừng! Bạn đã thắng {format_tien(winnings)} với cược {format_tien(bet_amount)} vào {bet_type['name']}."
                    )

        user_balances[user_id] += user_winnings
        if user_winnings == 0:
            for choice, bet_amount in bets:
                jackpot_amount += bet_amount // 2

    
    keyboard = [[InlineKeyboardButton("✅ Nạp Xu ✅", callback_data='nap_xu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🎲 Vui Lòng Đợi 10 Giây Để Mở Phiên Mới 🎲\n💠 Các Đại Gia Vui Lòng Vào Tiền Nhẹ 💠",
        reply_markup=reply_markup
    )
    unlock_chat(context, update.effective_chat.id)
    time.sleep(10)
    start_sicbo(update, context)

def p(update, context):
    start_sicbo(update, context)
    mophien_command(update, context)

def main():
    generate_multiplier = lambda: 1.0
    load_recent_results()
    fix_user_balance()
    load_user_balances()
    load_codes()
    load_user_code_usage()

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("ps", start_sicbo))

    dp.add_handler(CommandHandler("ptx", mophien_command))
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("tx", taixiu))
    dp.add_handler(CommandHandler("zhelp", help_command))
    dp.add_handler(CommandHandler("sd", sd))
    dp.add_handler(CommandHandler("addcode", addcode))
    dp.add_handler(CommandHandler("code", code))
    dp.add_handler(CommandHandler("givecode", givecode))
    dp.add_handler(CommandHandler("pay", chuyentien))
    dp.add_handler(CommandHandler("jackpot", jackpot))
    dp.add_handler(CommandHandler("rou", roulette))
    dp.add_handler(CommandHandler("taolistcode", taolistcode))
    dp.add_handler(CommandHandler("bj", blackjack))
    dp.add_handler(CommandHandler("hit", hit))
    dp.add_handler(CommandHandler("stand", stand))
    dp.add_handler(CommandHandler("bac", bac))
    dp.add_handler(CommandHandler("bactiep", bactiep))
    dp.add_handler(CommandHandler("keno", keno))
    dp.add_handler(CommandHandler("game", game))
    dp.add_handler(CommandHandler("sicbo", sicbo))
    dp.add_handler(CommandHandler("banthanhvien", ban_thanh_vien))
    dp.add_handler(CommandHandler("unbanthanhvien", unban_thanh_vien))
    dp.add_handler(CommandHandler("camnhom", cam_nhom))
    dp.add_handler(CommandHandler("addsd", themsodu))
    dp.add_handler(CommandHandler("startav", start_aviator))
    dp.add_handler(CommandHandler("av", aviator))
    dp.add_handler(CommandHandler("rut", cashout))
    dp.add_handler(CommandHandler("hotro", hotro))
    dp.add_handler(CommandHandler("s", slot_machine))
    dp.add_handler(CommandHandler("yccode", request_code_approval))
    dp.add_handler(CommandHandler("chanle", chanle))
    dp.add_handler(CommandHandler("doitien", doitien))
    dp.add_handler(CommandHandler("taixiu", taixiu1))
    dp.add_handler(CommandHandler("startxd", start_xocdia))
    dp.add_handler(CommandHandler("xocdia", xocdia))
    dp.add_handler(CommandHandler("giaxu", giaxu))
    dp.add_handler(CommandHandler("nap", nap))
    dp.add_handler(CommandHandler("xs", start_lottery))
    dp.add_handler(CommandHandler("mua", place_lottery_bet, pass_args=True))
    dp.add_handler(
        CallbackQueryHandler(handle_admin_response,
                             pattern=r'^(approve|reject)_\d+_\d+$'))    

    dp.add_handler(CommandHandler("starth", start_horse_race))
    dp.add_handler(CommandHandler("h", place_horse_bet))
    dp.add_handler(CommandHandler("out", leave_group))
    dp.add_handler(CommandHandler("themad", add_admin))
    dp.add_handler(CommandHandler("xoaad", remove_admin))
    dp.add_handler(CommandHandler("rutmomo", rutmomo))
    dp.add_handler(CommandHandler("duyet", duyetchuyen))
    dp.add_handler(CommandHandler("huy", huychuyen))
    dp.add_handler(CommandHandler("idme", idme))
    dp.add_handler(CommandHandler("top", top))
    dp.add_handler(CommandHandler("hailoc", hailoc))
    dp.add_handler(CommandHandler("huloc", huloc))
    dp.add_handler(CommandHandler("guitb", guitb))
    dp.add_handler(CommandHandler("cuocevent", cuocevent))
    dp.add_handler(CommandHandler("addrut", addrut))
    dp.add_handler(CommandHandler("rs", reset_jackpot))
    dp.add_handler(CommandHandler("xx", xx))
    dp.add_handler(CommandHandler("clearfile", clear_file))
    dp.add_handler(CommandHandler("profile", profile))
    dp.add_handler(CommandHandler("napthe", napthe, pass_args=True))
    dp.add_handler(CommandHandler("gui", gui))
    dp.add_handler(CommandHandler("checkbox", checkbox))
    dp.add_handler(CommandHandler("leave", leave, pass_args=True))
    dp.add_handler(CommandHandler("leaveall", leave_all_chats))
    dp.add_handler(CommandHandler("guinhom", send_to_group))
    dp.add_handler(CommandHandler("solo", solo))
    dp.add_handler(CommandHandler("join", join_solo))
    dp.add_handler(CommandHandler("roll", roll))
    dp.add_handler(CommandHandler("huysolo", cancel_solo))
    dp.add_handler(CommandHandler("checksolo", check_solo))
    dp.add_handler(MessageHandler(Filters.regex(r'^t\s+(max|\d+)$'), taixiu1))
    dp.add_handler(MessageHandler(Filters.regex(r'^T\s+(max|\d+)$'), taixiu1))
    dp.add_handler(MessageHandler(Filters.regex(r'^X\s+(max|\d+)$'), taixiu1))
    dp.add_handler(MessageHandler(Filters.regex(r'^x\s+(max|\d+)$'), taixiu1))
    dp.add_handler(MessageHandler(Filters.regex(r'^T\s+(Max|\d+)$'), taixiu1))
    dp.add_handler(MessageHandler(Filters.regex(r'^X\s+(Max|\d+)$'), taixiu1))
    dp.add_handler(MessageHandler(Filters.regex(r'^t\s+(Max|\d+)$'), taixiu1))
    dp.add_handler(MessageHandler(Filters.regex(r'^x\s+(Max|\d+)$'), taixiu1))
    dp.add_handler(CommandHandler('nap_xu', nap_xu))
    dp.add_handler(CommandHandler("checkbb",handle_show_invited_count))
    dp.add_handler(CommandHandler("sr", sicbo_bet))
    dp.add_handler(CallbackQueryHandler(gamebutton))
    dp.add_handler(CallbackQueryHandler(nap_xu, pattern='nap_xu'))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, join_chat))
    dp.add_handler(CallbackQueryHandler(handle_code_approval))
    dp.add_handler(MessageHandler(Filters.group & (~Filters.command), log_group_command))
    dp.add_handler(MessageHandler(Filters.private, private_message))
    dp.add_handler(MessageHandler(Filters.group, group_chat))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), idme_on_message))
    dp.add_handler(MessageHandler(Filters.group, save_group_info))
    updater.start_polling()
    updater.idle()
    save_user_balances()
    save_codes()
    save_user_code_usage()
if __name__ == '__main__':
    main()
