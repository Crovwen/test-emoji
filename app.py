import os
import time
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")

EMOJIS = [
    ("24h", "5803392202998551545"),
    ("Green Check", "5431478387698852009"),
    ("Channel", "5431376596973938467"),
    ("Link", "6269304938099118422"),
    ("Red X", "6332221746514501331"),
    ("Soon", "6332515848695063565"),
    ("Swag Bag", "5436023090163253817"),
    ("Snoop Cigar", "5438642075321003231"),
    ("Low Rider", "5438564134549486110"),
    ("Lol Pop", "5265077765375286666"),
    ("Snoop Dogg", "5436006606078769970"),
    ("Ice Cream", "5323507733125692367"),
]


def send_emojis(chat_id):
    text = ""
    entities = []

    for name, emoji_id in EMOJIS:
        prefix = f"{name}: "
        start = len(text.encode("utf-16-le")) // 2

        text += prefix + "⬜\n"

        emoji_offset = start + len(prefix.encode("utf-16-le")) // 2

        entities.append({
            "type": "custom_emoji",
            "offset": emoji_offset,
            "length": 1,
            "custom_emoji_id": emoji_id
        })

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "entities": entities
        },
        timeout=30
    )


def bot_loop():
    offset = 0

    while True:
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{TOKEN}/getUpdates",
                params={
                    "offset": offset,
                    "timeout": 30
                },
                timeout=40
            )

            updates = response.json().get("result", [])

            for update in updates:
                offset = update["update_id"] + 1

                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")

                if text == "/start" and chat_id:
                    send_emojis(chat_id)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


@app.route("/")
def home():
    return "Bot is running"


if __name__ == "__main__":
    import threading

    port = int(os.environ.get("PORT", 10000))

    threading.Thread(
        target=bot_loop,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=port
    )    
