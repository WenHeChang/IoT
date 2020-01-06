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

line_bot_api = LineBotApi('ce8OcKW0gwznMocIjxGNV5Yo9PxjffGcx9MnbMOoj8wo/vh+gfuwR6Ir6zYJqN7erg0d62DzY+AxU9f2tN+RUNM2rwKKya2LwXFqTCE3dKSpRNAp4BaOPB8BYigOUcZt+EV088UAJidGZeAG5638IgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f0c1aaae4d8227196b872224f147400b')

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
    elif(event.message.text==‘open’):
       os.system(‘irsend SEND_ONCE sampo1 KEY_1’)
       res="opened already"
    elif(event.message.text==‘close’):
       os.system(‘irsend SEND_ONCE sampo1 KEY_1’)
       res="closed already"
    else:
       res="Without This Service"


    line_bot_api.reply_message(
        event.reply_token,
       	TextSendMessage(text=res))



if __name__ == "__main__":
    app.run()
