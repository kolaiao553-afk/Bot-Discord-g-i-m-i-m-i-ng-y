import requests
import os

# --- CẤU HÌNH ---
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
FILE_DATA = "tuvung.txt"

# Tên Bot và Ảnh đại diện Bot (Bạn thay link ảnh logo của bạn vào đây)
BOT_NAME = "Tiếng Trung Hoa Thư"
BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/330/330459.png" 
# ----------------

def gui_tin_nhan_dep(data_list):
    if not WEBHOOK_URL:
        print("❌ Lỗi: Chưa có Webhook!")
        return False

    # Tách dữ liệu từ dòng văn bản (dựa vào dấu gạch đứng |)
    # Cấu trúc: Chữ | Pinyin | Nghĩa | Ví dụ Hán | Ví dụ Pinyin | Ví dụ Dịch | Link Ảnh
    try:
        tu_vung = data_list[0].strip()
        phien_am = data_list[1].strip()
        nghia = data_list[2].strip()
        vi_du_han = data_list[3].strip()
        vi_du_pinyin = data_list[4].strip()
        vi_du_dich = data_list[5].strip()
        link_anh = data_list[6].strip()
    except IndexError:
        print("❌ Lỗi: Dòng dữ liệu trong file tuvung.txt bị thiếu thông tin!")
        return False

    # Cấu trúc tin nhắn Embed (Giao diện đẹp)
    payload = {
        "username": BOT_NAME,
        "avatar_url": BOT_AVATAR,
        "embeds": [
            {
                "title": "📝 TỪ MỚI",
                "description": "----------------------------------------",
                "color": 15158332, # Mã màu đỏ (bạn có thể đổi màu khác)
                "fields": [
                    {
                        "name": "🔤 Từ",
                        "value": f"**{tu_vung}**",
                        "inline": True
                    },
                    {
                        "name": "📢 Phiên âm",
                        "value": phien_am,
                        "inline": True
                    },
                    {
                        "name": "💡 Nghĩa",
                        "value": f"**{nghia}**",
                        "inline": False # Xuống dòng
                    },
                    {
                        "name": "📌 Ví dụ",
                        "value": f"**{vi_du_han}**\n*Phiên âm:* {vi_du_pinyin}\n*Dịch:* {vi_du_dich}",
                        "inline": False
                    }
                ],
                "image": {
                    "url": link_anh
                },
                "footer": {
                    "text": "Chúc bạn học tốt mỗi ngày! ❤️"
                }
            }
        ]
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print(f"✅ Đã gửi thành công từ: {tu_vung}")
            return True
        else:
            print(f"❌ Lỗi gửi Discord: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return False

# --- PHẦN CHẠY CHÍNH ---
print("--- Bot Embed bắt đầu chạy ---")

if not os.path.exists(FILE_DATA):
    print(f"⚠️ Không tìm thấy file {FILE_DATA}")
    exit()

with open(FILE_DATA, "r", encoding="utf-8") as f:
    danh_sach = f.readlines()

if not danh_sach:
    print("📭 Hết từ vựng rồi!")
    exit()

# Lấy dòng đầu tiên và tách các phần
dong_dau_tien = danh_sach[0].strip()

if dong_dau_tien:
    # Tách dòng chữ thành các phần nhỏ bằng dấu |
    cac_phan = dong_dau_tien.split("|")
    
    # Gửi tin nhắn
    thanh_cong = gui_tin_nhan_dep(cac_phan)
    
    # Nếu gửi thành công thì xóa dòng đó đi
    if thanh_cong:
        with open(FILE_DATA, "w", encoding="utf-8") as f:
            f.writelines(danh_sach[1:])
        print("💾 Đã cập nhật file từ vựng.")

print("--- Hoàn thành ---")
