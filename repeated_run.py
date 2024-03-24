
import os
from dotenv import load_dotenv
import subprocess
import time
import sys
import RPi.GPIO as GPIO
from hx711py.hx711 import HX711

load_dotenv('.env')

NSEC=os.getenv("NSEC_HEX")
character ="🍫"

referenceUnit = 414.5
tare=598.8#かご込み　　654.9 #かごなし

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()    
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")


hx.set_reference_unit(referenceUnit)

hx.reset()


# hx.tare()# 初期化後にオフセットを設定する 起動時にものを乗せてても0になる

print("Tare done! Add weight now...")
val = hx.get_weight(5) + tare
preCount = int(val / 10.5) # 直前の個数を格納する変数
while True:
    try:
        val = hx.get_weight(5) + tare
        #  val = round(hx.get_weight(5) + tare, 4)  
        # (5)のぶぶんは読み取りの試行回数を示しています。読み取りを安定させるために複数回試行し、その平均値を返します。このようにして、ノイズや不安定な値を軽減し、より正確な重量を取得します。
        nowCount = round(val / 10.5)  # 1個あたりの重さで割って個数を計算し、整数に変換

        #print("Weight:", round(val, 2), "Count:", nowCount)
         # 前回の個数が存在し個数変化があった場合にその値を表示
        if preCount is not None and preCount > nowCount:
            print("🍫:", preCount-nowCount)
            MSG=character * (preCount-nowCount)
            command = f"nostr-tool -r wss://yabu.me -r wss://nos.lol -r wss://r.kojira.io -r wss://relay-jp.nostr.wirednet.jp -r wss://relay-jp.nostr.moctane.com -p {NSEC} text-note -c {MSG}"
            
            subprocess.run(command, shell=True)


        # 直前の個数を更新
        preCount = nowCount

        hx.power_down()
        hx.power_up()
        time.sleep(60)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()