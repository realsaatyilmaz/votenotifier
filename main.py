from datetime import datetime
import os
import threading
import time
from zoneinfo import ZoneInfo
from flask import Flask
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1574710382050811907/OVF1SjXFOihF-UNzunozZuKjahUICgcGHa8iqRiIJ8YKQpqeNaXX8Www6acVrM7MgiSo")
VOTE_URL = "https://minecraft-mp.com/server/345097/vote/"
USERNAME = os.getenv("MC_USERNAME", "Hamyapan918")
TZ = ZoneInfo("Asia/Tbilisi")

TARGET_HOUR = 12
TARGET_MINUTE = 50
last_sent_date = None


def send_discord_message():
  if not DISCORD_WEBHOOK_URL:
    print("Hata: DISCORD_WEBHOOK_URL ayarlanmamis.")
    return False

  message = {
      "content": (
          f"⏰ **Oy Zamanı (12:50)!** `{USERNAME}` kullanıcı adıyla oy vermek"
          f" için tıkla:\n{VOTE_URL}"
      )
  }

  try:
    response = requests.post(DISCORD_WEBHOOK_URL, json=message, timeout=15)
    response.raise_for_status()
    print("Discord bildirimi gönderildi.")
    return True
  except Exception as e:
    print(f"Gönderim hatası: {e}")
    return False


def clock_loop():
  global last_sent_date
  while True:
    now = datetime.now(TZ)
    today_str = now.strftime("%Y-%m-%d")

    if (
        now.hour == TARGET_HOUR
        and now.minute == TARGET_MINUTE
        and last_sent_date != today_str
    ):
      if send_discord_message():
        last_sent_date = today_str

    time.sleep(20)


# Arka plan saat kontrol döngüsünü başlat
threading.Thread(target=clock_loop, daemon=True).start()


@app.route("/")
def home():
  now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
  return f"Servis aktif. Gürcistan saati: {now} | Hedef: 12:50", 200


@app.route("/test")
def test_send():
  ok = send_discord_message()
  if ok:
    return "Test bildirimi gönderildi!", 200
  return "Test bildirimi gönderilemedi!", 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
