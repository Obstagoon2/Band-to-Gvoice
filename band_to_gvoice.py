import os
import time
import requests
from gvoice_api import GoogleVoice

BAND_ACCESS_TOKEN = os.environ.get("BAND_ACCESS_TOKEN")
BAND_BAND_KEY = os.environ.get("BAND_BAND_KEY")  # Your Band group key
GV_EMAIL = os.environ.get("GV_EMAIL")
GV_PASSWORD = os.environ.get("GV_PASSWORD")
PHONE_NUMBER = os.environ.get("SMS_TARGET_NUMBER")  # Number to send SMS to

PERSIST_FILE = "sent_notifications.txt"

def get_band_notifications():
    url = f"https://openapi.band.us/v2/band/post/list"
    params = {
        "access_token": BAND_ACCESS_TOKEN,
        "band_key": BAND_BAND_KEY,
        "limit": 5
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    notifications = []
    for post in data.get("result_data", {}).get("items", []):
        # Use post_id for persistence (unique & short), fallback to content summary if missing
        post_id = post.get('post_key') or post.get('created_at')
        content = f"{post.get('author', {}).get('name', 'Unknown')}: {post.get('content', '')}"
        notifications.append((str(post_id), content))
    return notifications

def send_gvoice_sms(text):
    voice = GoogleVoice()
    voice.login(GV_EMAIL, GV_PASSWORD)
    voice.send_sms(PHONE_NUMBER, text)
    voice.logout()

def load_sent():
    if not os.path.exists(PERSIST_FILE):
        return set()
    with open(PERSIST_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())

def save_sent(sent):
    with open(PERSIST_FILE, "w", encoding="utf-8") as f:
        for nid in sent:
            f.write(nid + "\n")

def main():
    sent = load_sent()
    while True:
        notes = get_band_notifications()
        updated = False
        for nid, ntext in notes:
            if nid not in sent:
                print(f"Sending: {ntext}")
                send_gvoice_sms(ntext[:160])  # SMS length limit
                sent.add(nid)
                updated = True
        if updated:
            save_sent(sent)
        time.sleep(300)  # Check every 5 mins

if __name__ == "__main__":
    main()