# https://zenn.dev/kotaproj/books/raspberrypi-tips/viewer/270_kiso_hx711
import subprocess
import time
import sys
import RPi.GPIO as GPIO
from hx711py.hx711 import HX711

PIN_DAT = 5
PIN_CLK = 6
display_time=15
referenceUnit = 414.5 

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

def main():
    hx = HX711(PIN_DAT, PIN_CLK)

    # データの並び順を指定
    hx.set_reading_format("MSB", "MSB")

    # キャリブレーション値を設定
    hx.set_reference_unit(referenceUnit)

    hx.reset()

    hx.tare()

    print("Tare done! Add weight now...")
    subprocess.run(["python", "led_control.py", "on"])

    start_time = time.time()  # 開始時間を記録

    while True:
        try:
            # Prints the weight.
            val = hx.get_weight(5)
            print(val)

            hx.power_down()
            hx.power_up()
            subprocess.run(["python", "display_4.py", str(val), str(1)])

            current_time = time.time()  # 現在の時間を取得
            if current_time - start_time >= display_time:  # 表示時間を過ぎたら
                break  # ループを抜ける

        except (KeyboardInterrupt, SystemExit):
            subprocess.run(["python", "led_control.py", "off"])
            cleanAndExit()

    subprocess.run(["python", "led_control.py", "off"])
    cleanAndExit()


if __name__ == "__main__":
    main()