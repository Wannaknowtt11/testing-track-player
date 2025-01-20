import requests
import time

# กำหนดค่า Webhook URL ของคุณ
WEBHOOK_URL = 'https://discord.com/api/webhooks/1321422848539234345/GYlkEJxUSmUr5Y6seK1mEMQufFiZmKH2Gf8SSJIhokkQfK0eg0BrGTnf2U2tDuoafzRH'

# UserID ของผู้เล่น
user_id = '7320155385'

# ฟังก์ชันเพื่อตรวจสอบสถานะออนไลน์ของผู้เล่นจาก API presence
def is_user_online(user_id):
    url = f"https://presence.roblox.com/v1/presence/users"
    response = requests.post(url, json={"userIds": [user_id]})
    
    if response.status_code == 200:
        presence_data = response.json()
        # ตรวจสอบสถานะออนไลน์ของผู้เล่น
        if presence_data['data'][0]['userId'] == int(user_id):
            return presence_data['data'][0]['isOnline']
    else:
        print(f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก API: {response.status_code}")
    return False

# ฟังก์ชันเพื่อตรวจสอบว่าอยู่ในเกมไหน
def get_user_game_info(user_id):
    url = f"https://api.roblox.com/users/{user_id}/current-game"
    response = requests.get(url)
    
    if response.status_code == 200:
        game_data = response.json()
        if 'game' in game_data:
            game_name = game_data['game']['name']
            place_id = game_data['game']['placeId']
            job_id = game_data['jobId']
            return game_name, place_id, job_id
    return None, None, None

# ฟังก์ชันเพื่อติดตามสถานะและแจ้งเตือน
def track_user_status(user_id):
    # ส่งข้อความแจ้งเตือนว่า "พร้อมทำงาน"
    hello_message = "พร้อมทำงาน! กำลังเริ่มติดตามสถานะผู้เล่น..."
    payload = {
        "content": hello_message
    }
    requests.post(WEBHOOK_URL, json=payload)
    
    # รอ 5 วินาที (หรือเวลาที่ต้องการ) ก่อนเริ่มทำงานต่อ
    time.sleep(5)
    
    # ตรวจสอบสถานะออนไลน์จาก API presence
    if is_user_online(user_id):
        game_name, place_id, job_id = get_user_game_info(user_id)
        if game_name and place_id and job_id:
            game_link = f"https://www.roblox.com/games/{place_id}/JobId={job_id}"
            message = f"ผู้เล่น {user_id} ออนไลน์อยู่ในเกม {game_name} (JobId: {job_id})\nลิงค์เข้าร่วมเกม: {game_link}"
        else:
            message = f"ผู้เล่น {user_id} ออนไลน์แต่ไม่สามารถดึงข้อมูลเกมได้"
    else:
        message = f"ผู้เล่น {user_id} ไม่ออนไลน์"

    # ส่งข้อความแจ้งเตือนสถานะผู้เล่นผ่าน Webhook
    payload = {
        "content": message
    }
    requests.post(WEBHOOK_URL, json=payload)

# ตรวจสอบสถานะทุกๆ 60 วินาที
while True:
    track_user_status(user_id)
    time.sleep(60)
