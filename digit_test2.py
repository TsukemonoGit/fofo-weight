#python digit_test2.py 1 0 0 0 0 0 0
import RPi.GPIO as GPIO
import time
import sys

# 74HC595を制御するピンの設定
dataPin = 25
latchPin = 24
clockPin = 23

# GPIOの初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(dataPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT)
GPIO.setup(clockPin, GPIO.OUT)

# シフトレジスタにパターンを送信する関数
def shift_out(dataPin, clockPin, latchPin, data):
    for bit in range(0, 8):  # ビットを順番に送信する
        GPIO.output(clockPin, GPIO.LOW)
        # 10進数を2進数にして左から順に（bit）なんかしてるデータからビットを抽出して送信する
        bit_value = (data >> bit) & 1
        #print(bit_value)
        GPIO.output(dataPin, bit_value)
        GPIO.output(clockPin, GPIO.HIGH)
    GPIO.output(latchPin, GPIO.HIGH)
    GPIO.output(latchPin, GPIO.LOW)

# LEDを消灯させる関数
def turn_off():
    shift_out(dataPin, clockPin, latchPin, 0)

# テストするLEDパターンを指定してテストを行う関数
def test_led_pattern(pattern):
    if len(pattern) != 8:
        raise ValueError("Invalid pattern: length must be 8")
    shift_out(dataPin, clockPin, latchPin, int("".join(map(str, pattern)), 2))
    #print(int("".join(map(str, pattern)), 2))


try:
    pattern = [int(x) for x in sys.argv[1:]]
    test_led_pattern(pattern)
    time.sleep(5)  # テストを実行した後、LEDを5秒間点灯させる
    turn_off()  # LEDを消灯させる
except ValueError:
    print("Invalid pattern: each digit in the pattern must be 0 or 1")
    sys.exit(1)
except Exception as e:
    print("An error occurred:", str(e))
    sys.exit(1)

GPIO.cleanup()  # GPIOピンを解放する