import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import requests
import base64

app = App(token=os.environ["SLACK_BOT_TOKEN"],
          signing_secret=os.environ["SLACK_SIGNING_SECRET"])

IMAGE_PATH = "reminder_cat.jpg"

@app.command("/reminder")
def handle_reminder(ack, say, command):
    ack()
    mensaje = command["text"]
    if not mensaje:
        say("Usá: `/reminder [tu mensaje]`")
        return

    channel_id = command["channel_id"]

    with open(IMAGE_PATH, "rb") as f:
        image_data = f.read()

    result = app.client.files_upload_v2(
        channel=channel_id,
        filename="reminder_cat.jpg",
        file=image_data,
        initial_comment=f"🐱 *REMINDER CAT TE RECUERDA:*\n{mensaje}"
    )

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(port=3000)
