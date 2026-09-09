import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ["BOT_TOKEN"]

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


def send_test(chat_id):
    text = ""
    entities = []

    for name, emoji_id in EMOJIS:
        prefix = name + ": "
        start = len(text.encode("utf-16-le")) // 2

        text += prefix + "⬜\n"

        entities.append({
            "type": "custom_emoji",
            "offset": start + len(prefix.encode("utf-16-le")) // 2,
            "length": 1,
            "custom_emoji_id": emoji_id
        })

    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "entities": entities
        },
        timeout=30
    )

    print(r.text)


@app.route("/", methods=["GET"])
def index():
    return "OK"


@app.route("/telegram", methods=["POST"])
def telegram():
    update = request.json or {}

    message = update.get("message", {})
    text = message.get("text", "")
    chat = message.get("chat", {})

    if text == "/start" and chat.get("id"):
        send_test(chat["id"])

    return "OK"


def setup_webhook():
    url = os.environ.get("RENDER_EXTERNAL_URL")

    if not url:
        print("RENDER_EXTERNAL_URL not found")
        return

    webhook = url + "/telegram"

    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook",
        json={"url": webhook},
        timeout=30
    )

    print("Webhook:", r.text)


if __name__ == "__main__":
    setup_webhook()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
