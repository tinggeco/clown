# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 23:15:11 2024

@author: ting
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 00:02:12 2024

@author: ting
"""

from flask import Flask, request, abort
import random

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='u+MhGca7dwgT4urxE0ak0Wi0mr87herJ8UF6FyT8X5t6zdPrjFLf4LxfPOEwatnnNu2dkUznRZ+SQeLCI9aReryIYX2WlhGixSUtQxw4w7j/lHJE4axtsHMYQITwDJX44N+ZQ45GGIDI20SUcpQKpAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('62bab4d94678447257b32200ffa254b4')

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    if isinstance(event.message, TextMessageContent):
        mtext = event.message.text
        if mtext == '乾你啥事':
            reply_options = [
                "如你能活到100歲，一共36500多天，87萬個小時，5235萬分鐘，差不多31億秒左右\n\n這10秒你在看我貼文\n\n這10秒，你只屬於我\n\n我愛你，吳小豬",
                "國際告白日給小豬八條建議：\n1.談戀愛首先要找你愛的，如果結婚就要找愛你的\n2.千萬別輸在“等”這個字身上\n3.永遠把家人放在第一位\n4.不要放棄自己的生活\n5.別把沒教養當做有性格\n6.談戀愛可以窮，結婚不可以\n7.談戀愛一定要找我\n8.牢記第7條，前6條沒什麼用",
                "吳小豬我給你寫了首藏頭詩\n\n吳\n小\n豬\n我\n愛\n你\n\n詩呢？哦，原來我對你的愛藏不住啊"
            ]
            reply_text = random.choice(reply_options)
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=reply_text)]
                    )
                )
        elif mtext == '博士好':
            reply_image_url = 'https://drive.google.com/uc?id=10bUG2SF48F4L5M_5X6p2cwiZpi4J-e2N'  # 替換為實際的圖片 URL
            reply_image_preview_url = 'https://drive.google.com/uc?id=10bUG2SF48F4L5M_5X6p2cwiZpi4J-e2N'  # 替換為實際的預覽圖片 URL
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[
                            ImageMessage(
                                original_content_url=reply_image_url,
                                preview_image_url=reply_image_preview_url
                            )
                        ]
                    )
                )

if __name__ == "__main__":
    app.run()
