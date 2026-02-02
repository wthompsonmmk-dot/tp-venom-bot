import json
import requests

JSON_URL = "https://fixr.co/organiser/timepiece?format=json"

TELEGRAM_BOT_TOKEN = "PASTE_YOUR_TOKEN_HERE"
TELEGRAM_CHAT_ID = "PASTE_YOUR_CHAT_ID_HERE"

SEEN_FILE = "seen_events.json"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)

def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def get_events():
    resp = requests.get(JSON_URL)
    data = resp.json()
    events = {}
    for ev in data.get("events", []):
        title = ev.get("title")
        link = "https://fixr.co/event/" + str(ev.get("id"))
        events[title] = link
    return events

def main():
    seen = load_seen()
    events = get_events()
    new_events = []
    for title, link in events.items():
        if title not in seen:
            new_events.append((title, link))
            seen.add(title)
    if new_events:
        for title, link in new_events:
            send_telegram(f"🎟 NEW FIXR EVENT\n\n{title}\n{link}")
        save_seen(seen)

if __name__ == "__main__":
    main()

