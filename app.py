import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = 5095867558

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


@app.route("/")
def home():
    return "Bot is running!"


@app.route("/test")
def test():
    if not TOKEN:
        return "BOT_TOKEN is not set"

    text = ""
    entities = []

    for name, emoji_id in EMOJIS:
        text += f"{name}: ⬜\n"

        # Telegram offsets are UTF-16
        offset = len(text[:-2].encode("utf-16-le")) // 2
        emoji_offset = offset + len(f"{name}: ".encode("utf-16-le")) // 2

        entities.append({
            "type": "custom_emoji",
            "offset": emoji_offset,
            "length": 1,
            "custom_emoji_id": emoji_id
        })

    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "entities": entities
        },
        timeout=30
    )

    return response.text


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
