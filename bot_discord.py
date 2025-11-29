import requests
import os

# --- CẤU HÌNH ---
# Lấy Webhook từ "két sắt" Secret của GitHub
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
FILE_DATA = "tuvung.txt"
# ----------------

def gui_tin_nhan(noi_dung):
    if not WEBHOOK_URL:
        print("❌ Lỗi: Chưa cấu hình Webhook trong Secrets!")
        return False
        
    data = {
        "content": f"🌟 **Thông điệp hôm nay:**\n\n>>> {noi_dung}"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print(f"✅ Đã gửi thành công: {noi_dung}")
            return True
        else:
            print(f"❌ Lỗi khi gửi: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return False

# --- PHẦN CHẠY CHÍNH ---
print("--- Bot bắt đầu làm việc ---")

if not os.path.exists(FILE_DATA):
    print("⚠️ Không tìm thấy file dữ liệu tuvung.txt")
    exit()

# Đọc file
with open(FILE_DATA, "r", encoding="utf-8") as f:
    danh_sach = f.readlines()

if len(danh_sach) == 0:
    print("📭 Hết từ để gửi rồi!")
    exit()

# Lấy dòng đầu tiên
tu_hom_nay = danh_sach[0].strip()

# Gửi và cập nhật lại file
if tu_hom_nay:
    thanh_cong = gui_tin_nhan(tu_hom_nay)
    if thanh_cong:
        with open(FILE_DATA, "w", encoding="utf-8") as f:
            f.writelines(danh_sach[1:])
        print("💾 Đã cập nhật danh sách từ vựng.")

print("--- Xong nhiệm vụ ---")
