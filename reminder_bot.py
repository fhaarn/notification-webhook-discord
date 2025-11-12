import requests
import time
import random
import os
from datetime import datetime, timedelta, timezone

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

EVENT_NAME = "PURPLE BLOODMOON"
EVENT_HOUR = 21  # 9 PM
TIMEZONE_OFFSET = 7  # GMT+7

def send_message(content):
    if not WEBHOOK_URL:
        print("Missing webhook URL")
        return
    payload = {
        "username": "jokowski",
        "avatar_url": "https://assets.bwbx.io/images/users/iqjWHBFdfxIU/i_kM.wM1lYnc/v0/2000x1429.webp",
        "embeds": [
            {
                "title": f"🔔 {EVENT_NAME}",
                "description": content,
                "color": 3447003
            }
        ]
    }
    requests.post(WEBHOOK_URL, json=payload)

def reminder_text(minutes_left):
    templates = [
        f"{EVENT_NAME} in {minutes_left} minutes! Get ready!",
        f"{minutes_left} minutes left until **{EVENT_NAME}**!",
        f"⏳ Counting down: {minutes_left} minutes to go!",
        f"Reminder: only {minutes_left} minutes left before {EVENT_NAME}!",
    ]
    return random.choice(templates)

def main():
    tz = timezone(timedelta(hours=TIMEZONE_OFFSET))
    now = datetime.now(tz)

    # Event time = today at 9 PM GMT+7
    event_time = now.replace(hour=EVENT_HOUR, minute=0, second=0, microsecond=0)
    if now > event_time:
        # If it’s already past 9 PM, schedule for tomorrow
        event_time += timedelta(days=1)

    # Start time of "last-hour reminders"
    last_hour_start = event_time - timedelta(hours=1)

    print(f"Event time: {event_time}")
    print(f"Now: {now}")

    # Generate all reminder times
    reminders = []
    t = now

    while t < last_hour_start:
        # Random delay 2–45 min
        delay = random.randint(2, 45)
        t += timedelta(minutes=delay)
        if t < last_hour_start:
            reminders.append(t)

    # Add fixed 10-minute reminders in the final hour
    t = last_hour_start
    while t < event_time:
        reminders.append(t)
        t += timedelta(minutes=10)

    reminders.sort()
    print(f"Planned {len(reminders)} reminders:")
    for r in reminders:
        print("  ", r)

    # Wait and send
    for reminder_time in reminders:
        while datetime.now(tz) < reminder_time:
            time.sleep(5)
        minutes_left = int((event_time - datetime.now(tz)).total_seconds() / 60)
        send_message(reminder_text(minutes_left))

if __name__ == "__main__":
    main()