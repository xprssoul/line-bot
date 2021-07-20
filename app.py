from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('Kiwta+lDGa08R2TLZpwgxcRxFZTdnt2nKr4ZZ3rLLVtvLdDwGNWijSvwWo20n/fpsyiwFMw03hVkK12gQJFUKO+igmjMXN07eFApj6kTWJcjsapSqxEuvs640HjihfNwS9KaWh34Fx53Ibb8FeVF/gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f7bc9366c2103e6d5e444fc4977fea1f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()