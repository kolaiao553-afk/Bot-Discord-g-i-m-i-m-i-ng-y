import requests
import schedule
import time
import os

# ================= C H =================
# 1. Dán link Webhook bạn vừa copy ở Bước 1 vào đây:
WEBHOOK_URL = "https://discord.com/api/webhooks/1444357872459714630/rllj36_L-gYl8agcmGSOCawihoM-dNVp4OKutpsJNByeuunWbAQB9ZTfPWQF8_5dWTw-"

# 2. Tên file chứa từ vựng
FILE_DATA = "tuvung.txt"

# 3. Giờ gửi tin nhắn hàng ngày (Định dạng 24h)
GIO_GUI = "08:00" 
# ============================================

def gui_tin_nhan(noi_dung):
    """Hàm gửi tin nhắn lên Discord"""
    data = {
        "content": f"🔔 **Từ vựng hôm nay:**\n>>> {noi_dung}"
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

def cong_viec_hang_ngay():
    print("--- Bắt đầu xử lý gửi tin ---")
    
    # Kiểm tra file có tồn tại không
    if not os.path.exists(FILE_DATA):
        print("⚠️ Không tìm thấy file dữ liệu!")
        return

    # Đọc dữ liệu từ file
    with open(FILE_DATA, "r", encoding="utf-8") as f:
        danh_sach = f.readlines()

    # Kiểm tra xem còn từ nào không
    if len(danh_sach) == 0:
        print("📭 Hết từ để gửi rồi!")
        gui_tin_nhan("⚠️ Thông báo: Đã hết từ vựng trong kho!")
        return

    # Lấy dòng đầu tiên và làm sạch (xóa dấu xuống dòng thừa)
    tu_hom_nay = danh_sach[0].strip()

    # Gửi tin nhắn
    if tu_hom_nay:
        thanh_cong = gui_tin_nhan(tu_hom_nay)
        
        # Nếu gửi thành công thì xóa dòng đó khỏi file để mai không gửi lại
        if thanh_cong:
            with open(FILE_DATA, "w", encoding="utf-8") as f:
                f.writelines(danh_sach[1:]) # Ghi lại từ dòng thứ 2 trở đi
            print("💾 Đã xóa từ vừa gửi khỏi danh sách.")

# --- LÊN LỊCH CHẠY ---
print(f"🤖 Bot đang chạy! Sẽ gửi tin vào lúc {GIO_GUI} hàng ngày.")

# Lên lịch
schedule.every().day.at(GIO_GUI).do(cong_viec_hang_ngay)

# Chạy thử 1 lần ngay lập tức để bạn kiểm tra (Nếu không thích thì xóa dòng dưới đi)
cong_viec_hang_ngay()

# Vòng lặp để duy trì bot chạy mãi mãi
while True:
    schedule.run_pending()
    time.sleep(60) # Nghỉ 60 giây để tiết kiệm CPU