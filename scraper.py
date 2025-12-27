import requests
from bs4 import BeautifulSoup
import json
import datetime
import os

# Giả sử đây là các URL hoặc trang web chứa số vote
URL = "https://luxuoasiaawards2025.1vote.vn/bang-xep-hang"

def get_votes():
    # Trong thực tế, bạn sẽ dùng BeautifulSoup để tìm đúng thẻ chứa số vote
    # Ví dụ:
    # response = requests.get(URL)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # vote1 = int(soup.find(id="nktt").text)
    
    # Giả lập dữ liệu để bạn dễ hình dung
    import random
    return {
        "nktt": random.randint(100, 200),
        "nckd": random.randint(100, 200),
        "ndln": random.randint(100, 200)
    }

def update_data():
    file_path = 'data.json'
    
    # Đọc dữ liệu cũ
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            history = json.load(f)
    else:
        history = []

    current_votes = get_votes()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Tính toán lượng tăng (delta) so với lần cuối cùng
    increase = {"nktt": 0, "nckd": 0, "ndln": 0}
    if history:
        last_entry = history[-1]
        for p in ["nktt", "nckd", "ndln"]:
            increase[p] = current_votes[p] - last_entry["votes"][p]

    # Lưu bản ghi mới
    new_entry = {
        "timestamp": timestamp,
        "votes": current_votes,
        "increase": increase
    }
    
    history.append(new_entry)
    # Chỉ giữ lại 100 bản ghi gần nhất để file không quá nặng
    history = history[-100:]

    with open(file_path, 'w') as f:
        json.dump(history, f, indent=4)

if __name__ == "__main__":
    update_data()