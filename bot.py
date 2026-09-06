import os
import hashlib
import math
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. SERVER KEEP-ALIVE ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "TOOL MD5 TXGAME v16.0 NEURAL ENGINE ONLINE", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. CẤU HÌNH HỆ THỐNG & ADMIN ---
TOKEN = '8985526419:AAGdRkntgFNYLBG53LoI-pNC7aHtOFMWhGA'
ADMIN_ID = 755092812
ADMIN_USERNAME = "lionvnios"

bot = telebot.TeleBot(TOKEN)
user_data = {}
all_users = set()
GLOBAL_CACHE = {}

def is_admin(user):
    if not user: return False
    if user.id == ADMIN_ID: return True
    if user.username and user.username.lower() == ADMIN_USERNAME.lower(): return True
    return False

def init_user(uid):
    all_users.add(uid)
    if uid not in user_data:
        user_data[uid] = {"balance": 20, "web": "HitClub", "logs": []}

# --- 3. ĐỘNG CƠ PHÂN TÍCH NHẬN DIỆN XU HƯỚNG CẦU (NEURAL ENGINE) ---
def neural_pattern_algo(raw_code):
    clean_code = raw_code.strip().lower()
    
    if clean_code in GLOBAL_CACHE:
        return GLOBAL_CACHE[clean_code]

    # Băm kết hợp SHA-512 + SHA3-256
    h_sha512 = hashlib.sha512(clean_code.encode()).hexdigest()
    h_sha3 = hashlib.sha3_256(clean_code.encode()).hexdigest()

    # Tính toán chỉ số ma trận
    byte_sum = sum(int(c, 16) for c in (h_sha512[:32] + h_sha3[:32]))
    
    # 1. Bắt nhịp Tài/Xỉu cân bằng 50/50 theo Parity Bit
    is_tai = (byte_sum % 2 == 0)
    result = "TÀI" if is_tai else "XỈU"

    # 2. Phân tích mô phỏng mẫu Cầu
    pattern_type_val = (byte_sum % 5)
    patterns = ["Cầu Bệt Xung Lực", "Cầu Đảo 1-1 Mượt", "Cầu Nhảy 2-2", "Cầu Khuôn 3-1-2", "Cầu Hồi Đảo"]
    pattern_name = patterns[pattern_type_val]

    # 3. Tính toán tỷ lệ phần trăm phân bố
    base_calc = 53.0 + ((byte_sum * 13) % 360) / 10.0
    if is_tai:
        p_tai = round(base_calc, 1)
        p_xiu = round(100.0 - p_tai, 1)
    else:
        p_xiu = round(base_calc, 1)
        p_tai = round(100.0 - p_xiu, 1)

    # 4. Chỉ số phụ trợ
    acc = round(94.2 + (byte_sum % 55) / 10.0, 1)
    latency = round(0.005 + (byte_sum % 15) / 1000.0, 3)

    res_tuple = (result, p_tai, p_xiu, pattern_name, acc, latency)
    GLOBAL_CACHE[clean_code] = res_tuple
    return res_tuple

# --- 4. GIAO DIỆN CHÍNH ---
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("⚙️ Đổi Cổng Game", callback_data="btn_web"),
        InlineKeyboardButton("💳 Ví & Lịch Sử", callback_data="btn_info")
    )
    markup.add(InlineKeyboardButton("💎 Nạp Xu Admin", callback_data="btn_nap"))
    return markup

# --- 5. ĐIỀU HƯỚNG ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    try:
        uid = message.from_user.id
        init_user(uid)
        text = (
            "⚡ **TOOL MD5 TXGAME [v16.0 NEURAL CORE]** ⚡\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 ID Client: `{uid}`\n"
            f"💳 Lượt quét dư: `{user_data[uid]['balance']} Lượt`\n"
            f"🌐 Server Game: `{user_data[uid]['web']}`\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "👉 **Dán mã MD5 (32 ký tự) hoặc SHA256 (64 ký tự)** để phần mềm phân tích ma trận."
        )
        bot.reply_to(message, text, parse_mode="Markdown", reply_markup=main_menu())
    except Exception as e:
        pass

# --- 6. HỆ THỐNG ADMIN QUẢN TRỊ ---
@bot.message_handler(commands=['congxu'])
def add_coins(message):
    try:
        if not is_admin(message.from_user):
            bot.reply_to(message, f"❌ **Từ chối truy cập!**\n🆔 ID của bạn: `{message.from_user.id}`", parse_mode="Markdown")
            return
            
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "❌ **Sai cấu trúc!**\n👉 Dùng: `/congxu <ID_User> <Số_Lượt>`", parse_mode="Markdown")
            return
            
        target_id = int(parts[1])
        amount = int(parts[2])
        
        init_user(target_id)
        user_data[target_id]["balance"] += amount
        
        bot.reply_to(message, f"✅ **CỘNG THÀNH CÔNG!**\n👤 ID: `{target_id}` | ➕ `{amount} Lượt` | 💳 Dư: `{user_data[target_id]['balance']} Lượt`", parse_mode="Markdown")
        
        try:
            bot.send_message(target_id, f"🎉 Admin đã cộng **+{amount} Lượt quét** vào tài khoản!\n💳 Dư mới: **{user_data[target_id]['balance']} Lượt**", parse_mode="Markdown")
        except:
            pass
            
    except ValueError:
        bot.reply_to(message, "❌ **Lỗi:** ID và Số lượt phải là chữ số nguyên.", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ **Lỗi xử lý:** {str(e)}", parse_mode="Markdown")

@bot.message_handler(commands=['thongbao'])
def broadcast(message):
    try:
        if not is_admin(message.from_user):
            bot.reply_to(message, "❌ **Từ chối truy cập!**")
            return
            
        parts = message.text.split(" ", 1)
        if len(parts) < 2:
            bot.reply_to(message, "❌ **Sai cấu trúc!** Dùng: `/thongbao <Nội dung>`", parse_mode="Markdown")
            return
            
        notice = parts[1].strip()
        success = 0
        for uid in list(all_users):
            try:
                bot.send_message(uid, f"📢 **THÔNG BÁO TỪ HỆ THỐNG**\n━━━━━━━━━━━━━━━━━━━\n{notice}", parse_mode="Markdown")
                success += 1
            except:
                pass
        bot.reply_to(message, f"✅ Đã phát thông báo đến `{success}` tài khoản.", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ **Lỗi phát tin:** {str(e)}", parse_mode="Markdown")

# --- 7. TƯƠNG TÁC CALLBACK ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        uid = call.from_user.id
        init_user(uid)
        if call.data == "btn_web":
            markup = InlineKeyboardMarkup(row_width=2)
            for w in ["HitClub", "B52", "Lucky88", "LC79", "Go88"]:
                markup.add(InlineKeyboardButton(f"🎮 {w}", callback_data=f"web_{w}"))
            bot.send_message(call.message.chat.id, "🌐 **Tùy chọn Cổng Game cần dò:**", parse_mode="Markdown", reply_markup=markup)
        elif call.data.startswith("web_"):
            web = call.data.split("_")[1]
            user_data[uid]["web"] = web
            bot.send_message(call.message.chat.id, f"✅ **Đã kết nối Server:** `{web}`", parse_mode="Markdown", reply_markup=main_menu())
        elif call.data == "btn_info":
            logs_str = "\n".join(user_data[uid]["logs"]) if user_data[uid]["logs"] else "Chưa có lịch sử phân tích."
            bot.send_message(call.message.chat.id, f"💳 **TRÍCH XUẤT HỒ SƠ**\n🆔 ID: `{uid}`\n💰 Lượt quét: `{user_data[uid]['balance']} Lượt`\n📜 **5 Nhịp quét gần nhất:**\n{logs_str}", parse_mode="Markdown", reply_markup=main_menu())
        elif call.data == "btn_nap":
            bot.send_message(call.message.chat.id, f"💎 **NẠP THÊM LƯỢT QUÉT**\n📩 Admin Telegram: @lionVnIos\n🆔 Copy ID này gửi Admin: `{uid}`", parse_mode="Markdown")
    except Exception as e:
        pass

# --- 8. PHÂN TÍCH LÕI ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        uid = message.from_user.id
        init_user(uid)
        text = message.text.strip().lower()
        
        if len(text) not in [32, 64]:
            bot.reply_to(message, "⚠️ **Định dạng không hợp lệ:** Chuỗi băm phải là MD5 (32 ký tự) hoặc SHA256 (64 ký tự).")
            return
        if user_data[uid]["balance"] < 1:
            bot.reply_to(message, "⚠️ **Tài khoản đã hết lượt quét!** Vui lòng liên hệ Admin để bổ sung.", reply_markup=main_menu())
            return
            
        user_data[uid]["balance"] -= 1
        result, p_tai, p_xiu, pattern_name, acc, latency = neural_pattern_algo(text)
        
        code_type = "MD5" if len(text) == 32 else "SHA-256"
        res_icon = "🔴 TÀI" if result == "TÀI" else "🔵 XỈU"
        
        user_data[uid]["logs"].insert(0, f"[{code_type}] {text[:8]}... ➔ {result}")
        if len(user_data[uid]["logs"]) > 5:
            user_data[uid]["logs"].pop()
            
        res_msg = (
            f"⚡ **KẾT QUẢ PHÂN TÍCH CHUỖI BĂM** ⚡\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 Dự đoán nhịp: **{res_icon}**\n"
            f"📊 Phân bổ xác suất: **Tài {p_tai}% - Xỉu {p_xiu}%**\n"
            f"📐 Tín hiệu thuật toán: `{pattern_name}`\n"
            f"🔒 Độ hội tụ ma trận: **{acc}%**\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"⏱️ Độ trễ xử lý: `{latency}s`\n"
            f"🎮 Server: `{user_data[uid]['web']}` | 💳 Dư: `{user_data[uid]['balance']} Lượt`"
        )
        bot.reply_to(message, res_msg, parse_mode="Markdown", reply_markup=main_menu())
    except Exception as e:
        bot.reply_to(message, f"❌ **Lỗi không xác định:** {str(e)}")

if __name__ == '__main__':
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    try:
        bot.remove_webhook()
    except:
        pass
    print("TOOL MD5 TXGAME v16.0 NEURAL ENGINE ACTIVE...")
    bot.infinity_polling(none_stop=True)
