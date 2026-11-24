import os
import requests

DISCORD_WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1574710382050811907/OVF1SjXFOihF-UNzunozZuKjahUICgcGHa8iqRiIJ8YKQpqeNaXX8Www6acVrM7MgiSo")
VOTE_URL = "https://minecraft-mp.com/server/345097/vote/"
USERNAME = os.getenv("MC_USERNAME", "Hamyapan918")
REMINDER_TIME = os.getenv("REMINDER_TIME", "12:50")


def send_vote_reminder():
  if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL ayarlanmamis.")

  message = {
      "content": (
          f"⏰ **Oy Zamanı ({REMINDER_TIME})!** `{USERNAME}` kullanıcı adıyla"
          f" oy vermek için tıkla:\n{VOTE_URL}"
      )
  }

  response = requests.post(DISCORD_WEBHOOK_URL, json=message, timeout=15)
  response.raise_for_status()
  print("Hatırlatıcı başarıyla gönderildi.")


if __name__ == "__main__":
  send_vote_reminder()
