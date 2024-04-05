
# オフセットを設定する
import os
import statistics
#from dotenv import load_dotenv # ModuleNotFoundError: No module named 'dotenv'
import subprocess
import time
import sys
import RPi.GPIO as GPIO
from hx711py.hx711 import HX711


#LED_PIN=17
#GPIO.setmode(GPIO.BCM)  #GPIOへアクセスする番号をBCMの番号で指定することを宣言します。
#GPIO.setup(LED_PIN,GPIO.OUT) #LED

referenceUnit = 414.5


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



try:
    #GPIO.output(LED_PIN,1)
    # LEDをオンにする
    subprocess.run(["python", "led_control.py", "on"])
    weight_readings2 = []
    while True:
        weight_readings = []

        # 値がぶれているときは測定しないようにする ちょうどものを載せようとしてるときとか取ろうとしてるときとかを避けられる？
        # 次実行するまであんていしてなかったらどうするの
        while True:
            val = hx.get_weight(5)
            weight_readings.append(val)
            time.sleep(0.1)  # 0.5秒ごとに重量を測定
            if len(weight_readings) >= 5:  # 10回の測定を行ったら判定
                stddev = statistics.stdev(weight_readings)
                if stddev < 0.5:  # 標準偏差が1以下であれば安定とみなす
                    val2=statistics.mean(weight_readings)
                    break
                else:
                    weight_readings = []

        weight_readings2.append(val2)
        print(val2)
        time.sleep(0.1)
        if len(weight_readings2) >= 3:  # 10回の測定を行ったら平均を取って保存
            stddev2 = statistics.mean(weight_readings2)
            # ファイルにtareを書き込む
            print("offset:",stddev2)
            with open("offset.txt", "w") as file:
                file.write(str(stddev2))
            break
finally:
    #GPIO.output(LED_PIN,0)
    # LEDをoffにする
    subprocess.run(["python", "led_control.py", "off"])
    hx.power_down()

    cleanAndExit()