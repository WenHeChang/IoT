# IoT
Lab monitor &amp; air conditioner control.
##   需求：
能夠在各處透過手機開啟實驗室冷氣，讓自己到達實驗室時，享受非常舒適的環境。並且能夠知道實驗室溫濕度＆是否有人進出實驗室。

##   達成：
我們可以透過Line bot 利用DTH22，查看我們實驗室的溫濕度，並且可以遠端開啟實驗室的冷氣（開：turn on；關：turn off）；透過鏡頭，搭配Motion套件，當實驗室有人進出時，我們將拍下進出實驗室的人，透過Line Notify發送到我們的Line裡面。
（Line是我們生活中相當普及的軟體，透過Line bot可以快速地對我們的系統操作與推播資訊。 一方面只是單純因為我還沒玩過Line bot 所以想玩玩看。 另外也可以玩玩看Line Notify，若我們Device沒有架設Web service 也能很方便使用Line所提供的服務）

##   所需材料：
樹莓派B3+ * 1 </br> 
麵包板 * 1 </br> 
杜邦線 *N條，看你想怎接 </br> 
鏡頭 * 1 </br> 
DTH22溫濕度感測器 *1 </br> 
紅外線接收模組1340 *1 </br> 
紅外線發射模組1341 *1 </br> 
電阻(2k) *3 </br> 


我們將分為以下步驟進行：
1. 測試執行溫濕度感測元件
2. 測試執行鏡頭搭配Motion套件，偵測物體移動，並串聯Line Notify
3. 透過lirc測試使用紅外線接收模組，記錄冷氣遙控器控制訊號，利用紅外線發送模組發送收集來的訊號來操控冷氣。
4. 利用Line bot 、 Line Notify 串接所有功能。

##   步驟一(測試執行溫濕度感測元件）：
Adafruit_Python_DHT 套件

1. 下載 Adafruit_Python_DHT 套件
`
$ git clone https://github.com/adafruit/Adafruit_Python_DHT.git
`
2. 進入下載的目錄
`
$ cd Adafruit_Python_DHT/
`
3. 安裝 Adafruit_Python_DHT 套件
`
$ python setup.py install
`
4. 離開下載的目錄
`
$ python setup.py install
`
5. 刪除下載的目錄
`
$ python setup.py install
`
6. 確認 Adafruit_Python_DHT 已經正確安裝
`
$ pip list
`
7. 接好感測設備 DHT22 我們使用 GPIO
8. 在此我們接的是 3.3V電源 GPIO4訊號輸出
9. 簡單小程式測試
```python
#!/location
import Adafruit_DHT
sensor = Adafruit_DHT.DHT22
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('temp:{0:0.1f} humidity:{1:0.1f}'.format(temperature, humidity))
```

##   步驟二(測試執行鏡頭搭配Motion套件，偵測物體移動，並串聯Line Notify）：
參考資料：
> 1. https://blog.gtwang.org/iot/raspberry-pi/how-to-diy-home-alarm-system-with-raspberry-pi-and-webcam/
> 2. 

1. 先將鏡頭裝上（記得金屬接頭要對準）
2. 測試是否可以拍照
```shell
$ raspistill -o "folder_location"/"picture_name".jpg
```
3. 安裝與設定motion.config(以下參考網路參數設定)
```shell
#motion 是最主要的核心工具，使用 apt 即可安裝。安專之前新更新系統套件資訊：

#安裝 motion 套件：
sudo apt-get update

#motion 在安裝完成之後，預設是不會自動啟動的，要讓它能夠開機自動啟動，就要修改 /etc/default/motion 設定檔，啟用 motion 的 daemon：
sudo apt-get install motion

#接著修改 /etc/motion/motion.conf 設定檔，調整各種 motion 的參數，這裡的參數非常多，這裡只是列出一些我個人感覺比較需要調整的部份。
start_motion_daemon=yes

stream_localhost off
webcontrol_localhost off

width 480
height 360

quality 90

framerate 4

noise_level 64

threshold 3000

ffmpeg_output_movies off

locate_motion_mode on

locate_motion_style redbox

output_pictures center

event_gap 2

picture_filename %Y%m%d%H%M%S

on_picture_save 輸入你想要進行的動作，這裡我們結合line notify

```
4. 參數概略整理介紹
- videodevice：webcam #裝置所在系統位置，預設為/dev/video0
- width：拍攝影像寬度
- height：拍攝影像高度
- framerate：每秒擷取畫面數
- threshold：異動像素到達該門檻值時，判斷為移動事件
- threshold_tune：自動調降 threshold 數值，提高移動事件頻率
- noise_level：移動偵測中可以被忽略的雜訊門檻值
- noise_tune：自動調整雜訊門檻值
- despeckle_filter：去除斑點過濾器，以侵蝕
- lightswitch：可忽略光線變化佔影像大小的百分比
- event_gap：每個移動事件為一系列的連續移動影像，在 event_gap 設定的秒數內若無偵測到移動，則該移動事件結束，並從上述連續的暫存影像中輸出一張最符合 output_pictures 參數的圖片。
- output_pictures：偵測到移動時，輸出圖片，有 on，off，first，best，center 等 5 種參數可調整；預設為 on-每張符合 threshold 的影像都輸出、off-關閉影像輸出、first-輸出該移動事件的第一個影像、best-輸出該移動事件中像素異動量最大的影像、center-輸出該移動事件中像素異動最接近中心點的影像
- output_debug_pictures：輸出移動事件中的所有移動影像為二值化黑底圖片，可做為調整設定的參考依據
- quality：數值愈高，jpeg 壓縮率愈低，圖片品質愈高
- locate_motion_mode：於圖片上標示像素異動區域，可設為 on，off，preview
- locate_motion_style：標示像素異動區域的形狀，可設為 box，redbox，cross，redcross
- target_dir：輸出影像儲存目錄位置
- picture_filename：圖片檔案名稱，可利用內建變數自行組合，例如：%Y%m%d%H%M%S即是以年月日時分秒做為檔案名稱，%v 可顯
----
5. 結合Line Notify  (此處當然也可以結合Line bot 隨個人喜好 概念是相同的)
- 申請Line notify 建立聊天室tocken
- Line notify 利用command 發送圖片
$ curl -X POST https://notify-api.line.me/api/notify 
       -H 'Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN' \
       -F 'message=test' \
       -F 'imageFile=@/PATH/TO/IMAGE/cony.jpg'

- 在motion.conf檔案內的參數on_picture_save 後面接入指令啟動Line Notify ，也就是把上面的command加入即可。


##   步驟三(透過lirc測試使用紅外線接收模組，記錄冷氣遙控器控制訊號，利用紅外線發送模組發送收集來的訊號來操控冷氣。）：

## ==此處有重大彩蛋，若在Linux內核v4.19之前的作業系統，也就是NOOB3.0.1以前，不用理會，否則你會跟我一樣痛苦。==

## 因為lirc套件在該版以後的內核不再支援。

## ==Sol1:== 作業系統降版
## ==sol2:== 下載補丁（自行上網搜索看得懂的，記得先備份，超容易壞）

### 1. 安裝lirc套件並測試  接收採用GPIO.pin17 發射採用GPIO.pin18
```shell=
#下載安裝套件
sudo apt update
sudo apt install lirc

#新增模組套件 
sudo nano /etc/modules   
# 把lirc_dev打進去

#修改系統config
sudo nano /boot/config.txt
# 找到 ＃dtoverlay = lirc-rpi 在下面打入dtoverlay = lirc - rpi ，gpio_in_pin = 17 ，gpio_out_pin = 18

#文件顯示到 /etc/lirc/hardware.conf 去修改
#但該檔案已經不存在，所以到 /etc/lirc/lirc_options.conf 修改
#注意如果安裝的時候發現錯誤代表新版增加.dist檔案，記得改名字
#可以稍微google關鍵字 解法是將.conf.dist 改成.conf即可

sudo nano  /etc/lirc/lirc_options.conf 

#找到 
#    driver          = devinput
#    device          = auto
#改成 
#    driver          = default
#    device          = /dev/lirc0
##################################################

#有多餘檔案將它改掉
cd /etc/lirc/lircd.conf.d/
sudo mv devinput.lircd.conf devinput.lircd.conf.dist

# NOOBS 2.4.3開始，LIRC正在運行 所以將其停止
sudo service lircd stop


```


### 2. 透過lirc套件讀取自己冷氣遙控器的訊號 設定遙控器名稱 遙控器按鍵名稱(按鍵名稱命名有規則，可使用command查詢: irrecord --list-namespace|grep KEY)

- 開始錄製～～～～跟著操螢幕操作做。多嘗試幾次，保持耐心。熟悉後成功率就高了～～
> irrecord -n -d /dev/lirc0


### 3. 用紅外線發射器，發射訊號
- 所產生的訊號檔案（副檔名為.conf) 傳送到 /etc/lirc/lircd.conf.d/
> sudo mv your_controller_name.lircd.conf /etc/lirc/lircd.conf.d/

- 將訊號發出去 ～～～ 
> irsend SEND_ONCE your_controller_name your_namespace
> 


##   步驟四(串接Line bot）：
1. 架設web service 在此我們使用flask
> pip install flask
> 創建一個 .py 照flask框架寫法
2. 將web service tunnel從http加密成https（因應line bot需求）在此我們使用Ngrok 取得的https網址將用於Line bot webhook
> 去Ngrok官網創會員並登入，下載ngrok並解壓縮 然後照上面步驟操作
> 安裝完成後輸入
> ./ngrok http port_number  #port_number與flask所用同
3. 申請Line bot develop帳號 並且創建一個Messaging API 記錄下Channel Access Token 和 Channel Secret 並將Callback URL 設定成"自己的Web_service網址/callback" 
4. 安裝Line bot 套件
> pip install line-bot-sdk
5. 透過web service 開設API service 回應line bot
（可以參考：https://missterhao.me/2017/08/15/line-bot-dev-1/）
6. 比對字串，了解使用者需求，將各個功能寫回來～～～～
7. 若使用者想知道溫度or濕度，則執行溫濕度的程式碼，並回傳結果
8. 若使用者想開關冷氣，則執行程式碼os.system搭配開關冷氣指令。

參考資料：</br> 
[1] https://developers.line.biz/zh-hant/docs/messaging-api/overview/ </br> 
[2] https://xiaosean.github.io/server/2018-04-18-Flask_Ngrok/ </br>
[3] https://missterhao.me/2017/08/15/line-bot-dev-1 </br>
[4] https://github.com/adafruit/Adafruit_Python_DHT </br>
[5] https://kingfff.blogspot.com/2018/05/raspberry-pi-cacti-weather-dht22-temperature-humidity.html </br>
[6] https://motion-project.github.io/ </br>
[7] https://blog.gtwang.org/iot/raspberry-pi/how-to-diy-home-alarm-system-with-raspberry-pi-and-webcam/ </br>
[8] https://engineering.linecorp.com/en/blog/using-line-notify-to-send-stickers-and-upload-images/ </br>
[9] https://www.instructables.com/id/Setup-IR-Remote-Control-Using-LIRC-for-the-Raspber/ </br>
[10] http://yoshiesk.blogspot.com/2017/09/lirc.html </br>


