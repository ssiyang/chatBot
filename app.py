from __future__ import unicode_literals
import os
import requests
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('NuU/O3Gakontmd+VP+lWJIXtcRTV/AWoi8VQ2Lo8YXFUzROmJkv3NnxoAl6Gb4nsU50Vy2aHUGbKBiaoORR6ypbEURivY/cxr4uUqEmSDW64zEUOgdQp7grvDHAlcipdQnCCYYUeGv+cGpom3qnApgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('353503ef0dcd61cf1f2988ac7f371f8b')

# 接收 LINE 的資訊
@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'

# # 學你說話


@handler.add(MessageEvent, message=TextMessage)
def doEvent(event):
    actionText = event.message.text[0:2]
    if actionText == '登入':
        mesArray = event.message.text.split(',')
        apiUrl = 'http://10.8.96.8:6080/api/ddb/mvpuser/appLogin'
        userName = mesArray[1]
        userPassword = mesArray[2]
        print('userName'+userName)
        print('userPassword'+userPassword)
        data = {'username': userName, 'password': userPassword}

        response = requests.post(apiUrl, json=data)
        res = json.loads(response.text)
        # res = response.json()
        print('Login Success response: '+ response.text)
        print('Login Success userid: '+ res['userid'])
        userId=res['userid']
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=userId)
        )
    # replyArr = []
    # replyArr.append(TextSendMessage(userName))
    # replyArr.append(TextSendMessage(userPassword))
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     replyArr
    # )

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=replyArr)
    # )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='輸入 說明 查看相關指令')
        )

if __name__ == '__main__':
    app.run()
