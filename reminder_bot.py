import requests
import time
import random
import os
from datetime import datetime, timedelta, timezone

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

EVENT_NAME = "🌕 PURPLE BLOODMOON"
EVENT_HOUR = 21  # 9 PM
TIMEZONE_OFFSET = 7  # GMT+7

def send_message(content):
    """Send a Discord webhook message with embed and username/avatar."""
    if not WEBHOOK_URL:
        print("Missing webhook URL")
        return
    payload = {
        "username": "Talon",
        "avatar_url": "https://media.discordapp.net/attachments/1436709184409440270/1438108798299668510/IMG_20251112_170959.jpg?ex=6915aeb0&is=69145d30&hm=450b98199654bc4b61a802699d7f93cf0f9c92ce34eee7b2a3164a5a5570e6c0&=&format=webp&width=1456&height=1744",
        "content": reminder_text(),
        "embeds": [
            {
                "title": f"🔔 {EVENT_NAME}",
                "description": content,
                "color": 16729344  # gold tone
            }
        ]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print(f"[{datetime.now()}] Sent: {content}")
    except Exception as e:
        print(f"[ERROR] {e}")

# 🧠 Different message vibes based on how close it is
def hype_text(minutes_left):
    if minutes_left > 60:
        return f"🕖 The {EVENT_NAME} is coming tonight! Still {int(minutes_left / 60)} hour(s) left — mark your calendar!"
    elif minutes_left > 10:
        return f"⚡ {EVENT_NAME} approaches... only {minutes_left} minutes left! Prepare your snacks 🍿"
    elif minutes_left > 1:
        return f"🔥 We're almost there — just {minutes_left} minutes to the {EVENT_NAME}! The sky trembles 👀"
    else:
        return f"🚀 Final minute before {EVENT_NAME}! Get outside and look up!"

def countdown_text(seconds_left):
    if seconds_left > 5:
        return f"⏳ {seconds_left} seconds left..."
    elif seconds_left > 0:
        return f"⚡ {seconds_left}..."
    else:
        return f"🌕 {EVENT_NAME} IS HAPPENING NOW!!! LOOK UP!!! 🌕🎉🔥"

def reminder_text():
    templates = [
        "Selamat Malam @everyone",
        "Mau ngingetin nih anak - anak ku @everyone",
        "Indonesia negara hukum, asslamualaikum @everyone",
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

    print(f"Event time: {event_time}")
    print(f"Now: {now}")

    # Generate schedule
    reminders = []
    t = now

    # 1️⃣ Every hour until the last hour
    hour_time = event_time.replace(minute=0, second=0, microsecond=0)
    t = hour_time - timedelta(hours=2)
    while t < event_time - timedelta(hours=1):
        if t > now:
            reminders.append(t)
        t += timedelta(hours=1)

    # 2️⃣ Every 10 minutes in the last hour
    t = event_time - timedelta(hours=1)
    while t < event_time - timedelta(minutes=10):
        if t > now:
            reminders.append(t)
        t += timedelta(minutes=10)

    # 3️⃣ Every minute in the last 10 minutes
    t = event_time - timedelta(minutes=10)
    while t < event_time - timedelta(seconds=15):
        if t > now:
            reminders.append(t)
        t += timedelta(minutes=1)

    # 4️⃣ Every second in the last 15 seconds
    t = event_time - timedelta(seconds=15)
    while t <= event_time:
        if t > now:
            reminders.append(t)
        t += timedelta(seconds=1)

    reminders.sort()
    print(f"Planned {len(reminders)} reminders:")
    for r in reminders:
        print("  ", r)

    # 🚀 Run reminders
    for reminder_time in reminders:
        while datetime.now(tz) < reminder_time:
            time.sleep(0.5)

        diff = event_time - datetime.now(tz)
        seconds_left = int(diff.total_seconds())
        minutes_left = max(1, int(seconds_left / 60))

        if seconds_left <= 15:
            message = countdown_text(seconds_left)
        else:
            message = hype_text(minutes_left)

        send_message(message)

if __name__ == "__main__":
    main()
