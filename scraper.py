import requests
import json
import os
from datetime import datetime, timedelta, timezone

API_URL = "https://eventista-platform-api.1vote.vn/v1/internal/tenants/TODa16/products?eventId=EVENT_bA8rc"

def get_votes_from_api():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    }
    try:
        response = requests.get(API_URL, headers=headers)
        json_res = response.json()
        
        # Truy cập vào data -> products theo cấu trúc bạn gửi
        products = json_res.get('data', {}).get('products', [])
        
        results = {}
        # Lấy Top 3 người dẫn đầu
        for item in products[:3]:
            # Rút gọn tên cho dễ nhìn trên biểu đồ (ví dụ: lấy chữ sau dấu /)
            full_name = item.get('name', 'Unknown')
            display_name = full_name.split('/')[-1].strip() if '/' in full_name else full_name
            
            results[display_name] = int(item.get('points', 0))
        return results
    except Exception as e:
        print(f"Lỗi API: {e}")
        return {}

def main():
    file_path = 'data.json'
    history = []
    
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as f:
            try: history = json.load(f)
            except: history = []

    current_votes = get_votes_from_api()
    if not current_votes: return

    # Tạo múi giờ Việt Nam
    vn_tz = timezone(timedelta(hours=7))

    # Lấy thời gian hiện tại chính xác theo múi giờ VN
    vietnam_now = datetime.now(vn_tz)

    # Định dạng chuỗi
    timestamp = vietnam_now.strftime("%H:%M %d/%m")
    
    # Tính lượng tăng (Delta)
    increase = {}
    if history:
        last_entry = history[-1]['votes']
        for name, points in current_votes.items():
            # Lấy điểm cũ, nếu là người mới thì coi như cũ là 0
            old_points = last_entry.get(name, points) 
            increase[name] = points - old_points
    else:
        increase = {name: 0 for name in current_votes}

    history.append({
        "time": timestamp,
        "votes": current_votes,
        "increase": increase
    })

    # Chỉ giữ 100 bản ghi (khoảng 25 tiếng nếu 15p cào 1 lần)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history[-100:], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()