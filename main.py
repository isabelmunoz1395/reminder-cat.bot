import os
import threading
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

app = App(token=os.environ["SLACK_BOT_TOKEN"],
          signing_secret=os.environ["SLACK_SIGNING_SECRET"])

IMAGE_PATH = "reminder_cat.jpg"

def send_reminder(client, channel_id, mensaje):
    with open(IMAGE_PATH, "rb") as f:
        image_data = f.read()
    client.files_upload_v2(
        channel=channel_id,
        filename="reminder_cat.jpg",
        file=image_data,
        initial_comment=f"🐱 *REMINDER CAT TE RECUERDA:*\n{mensaje}"
    )

@app.command("/reminder")
def handle_reminder(ack, client, command):
    ack()
    mensaje = command["text"]
    if not mensaje:
        client.chat_postMessage(
            channel=command["channel_id"],
            text="Usá: `/reminder [tu mensaje]`"
        )
        return
    thread = threading.Thread(
        target=send_reminder,
        args=(client, command["channel_id"], mensaje)
    )
    thread.start()

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(port=3000)
