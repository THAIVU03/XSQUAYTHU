import requests

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
            print(f"✅ Đăng nhập thành công: {user} | Số dư: {balance} xu")
            return user, balance
        else:
            print(f"❌ Token {access_token[:5]}*** bị lỗi!")
    else:
        print(f"⚠️ Lỗi kết nối API với token {access_token[:5]}***")
    
    return None, None

# Chạy kiểm tra danh sách tài khoản
if __name__ == "__main__":
    tokens = load_tokens()
    
    if not tokens:
        print("⚠️ Không tìm thấy token nào trong file `ttc_accounts.txt`!")
    else:
        print(f"📌 Kiểm tra {len(tokens)} tài khoản TuongTacCheo...")
        for token in tokens:
            login_ttc(token)
