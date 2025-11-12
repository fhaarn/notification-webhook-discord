import requests
import time
from datetime import datetime, timedelta
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

EVENT_NAME = "test-notification"
REMINDER_INTERVAL = 1  # minutes
EVENT_DELAY = 5        # minutes from now

def send_message(content):
    if not WEBHOOK_URL:
        print("Missing webhook URL")
        return
    payload = {
        "embeds": [
            {
                "title": f"🔔 {EVENT_NAME}",
                "description": content,
                "color": 3447003
            }
        ]
    }
    requests.post(WEBHOOK_URL, json=payload)

def reminder_loop():
    event_time = datetime.now() + timedelta(minutes=EVENT_DELAY)
    start_time = datetime.now()
    print(f"Starting reminders at {start_time.strftime('%H:%M:%S')} "
          f"for event at {event_time.strftime('%H:%M:%S')}")

    while datetime.now() < event_time:
        minutes_left = int((event_time - datetime.now()).total_seconds() // 60)
        send_message(f"⏰ {minutes_left} minutes left until {EVENT_NAME}!")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent reminder.")
        time.sleep(REMINDER_INTERVAL * 60)

    send_message(f"🎉 It's time for **{EVENT_NAME}**!")
    print("All reminders sent!")

if __name__ == "__main__":
    reminder_loop()
