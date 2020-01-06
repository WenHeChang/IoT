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
import Adafruit_DHT as AD
import os

app = Flask(__name__)

line_bot_api = LineBotApi('$Channel access token')
handler = WebhookHandler('$Channel Secret')

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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    sensor = AD.DHT22
    pin = 4
    humidity, temperature = AD.read_retry(sensor, pin)

    #if humidity is not None and temperature is not None:
     #   print('temp:{0:0.1f} humidity:{1:0.1f}'.format(temperature, humidity))	
	#check user input
    if(event.message.text=='temperature'):
       res=round(temperature,5)
    elif(event.message.text=='humidity'):
       res=round(humidity,5)
    elif(event.message.text==‘turn on’):
       os.system(‘irsend SEND_ONCE $your_controller_name your_namespace’)
       res="opened already"
    elif(event.message.text==‘turn off’):
       os.system(‘irsend SEND_ONCE $your_controller_name your_namespace’)
       res="closed already"
    else:
       res="Without This Service"


    line_bot_api.reply_message(
        event.reply_token,
       	TextSendMessage(text=res))



if __name__ == "__main__":
    app.run()
