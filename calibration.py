# https://zenn.dev/kotaproj/books/raspberrypi-tips/viewer/270_kiso_hx711
import time
import sys
import RPi.GPIO as GPIO
from hx711py.hx711 import HX711

PIN_DAT = 5
PIN_CLK = 6

referenceUnit = 415 # <=これを決めたい

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

    while True:
        try:
            # Prints the weight.
            val = hx.get_weight(5)
            print(val)

            hx.power_down()
            hx.power_up()
            time.sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            panel.display_clear()
            cleanAndExit()


if __name__ == "__main__":
    main()