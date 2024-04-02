import RPi.GPIO as GPIO
import time

COUNTRESET_PIN=27
LED_PIN=17
GPIO.setmode(GPIO.BCM)  #GPIOへアクセスする番号をBCMの番号で指定することを宣言します。

GPIO.setup(LED_PIN,GPIO.OUT) #LED
GPIO.setup(COUNTRESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    # スイッチ押下待ち
    GPIO.wait_for_edge(COUNTRESET_PIN,GPIO.FALLING)
    GPIO.output(LED_PIN,1)
       # ファイルにpreCountを書き込む
    with open("preCount.txt", "w") as file:
        file.write(str(0))
    #チャタリング対策
    time.sleep(0.3)
    GPIO.output(LED_PIN,0)