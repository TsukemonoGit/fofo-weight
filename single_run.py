
import os
import statistics
#from dotenv import load_dotenv # ModuleNotFoundError: No module named 'dotenv'
import subprocess
import time
import sys
import RPi.GPIO as GPIO
from hx711py.hx711 import HX711


NSEC = sys.argv[1]
NOSTR_TOOL = sys.argv[2]
print(NSEC)
print(NOSTR_TOOL)
character ="🍫"

# preCount.txt ファイルの存在を確認し、存在しない場合はファイルを作成する
if not os.path.exists("preCount.txt"):
    with open("preCount.txt", "w") as file:
        file.write("0")  # 初期値を書き込む

# ファイルから preCount を読み込む
with open("preCount.txt", "r") as file:
    preCount = int(file.read().strip())



referenceUnit = 414.5
if not os.path.exists("offset.txt"):
    offset=0.0
else:
    # ファイルから preCount を読み込む
    with open("offset.txt", "r") as file:
        offset = float(file.read().strip())
        
print("offset:",offset)
def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()    
    print("Bye!")
    sys.exit()

# 前回の実行が終了しているかどうかを確認し、終了していない場合は終了する
if os.path.exists("lockfile"):
    print("Previous execution is still in progress. Exiting...")
    print("Bye!")
    sys.exit() #GPIO設定する前だからいらないのかも 

# 数字モニタ　74HC595
dataPin=25
latchPin=24
clockPin=23

# LED
GPIO.setmode(GPIO.BCM)
#GPIO.setup(17,GPIO.OUT)
GPIO.setup(dataPin,GPIO.OUT)
GPIO.setup(latchPin,GPIO.OUT)
GPIO.setup(clockPin,GPIO.OUT)
# 各数字に対応する7セグメントLEDのパターン
# 数字0から9までのパターンを表す
# [A, B, C, D, E, F, G,DP]の順で各セグメントが点灯するかどうかをためすにはdigit_test.pyで確認

digit_patterns = [
    [1, 1, 1, 1, 1, 1, 0,0], # 0
    [0, 1, 1, 0, 0, 0, 0,0], # 1
    [1, 1, 0, 1, 1, 0, 1,0], # 2
    [1, 1, 1, 1, 0, 0, 1,0], # 3
    [0, 1, 1, 0, 0, 1, 1,0], # 4
    [1, 0, 1, 1, 0, 1, 1,0], # 5
    [1, 0, 1, 1, 1, 1, 1,0], # 6
    [1, 1, 1, 0, 0, 0, 0,0], # 7
    [1, 1, 1, 1, 1, 1, 1,0], # 8
    [1, 1, 1, 1, 0, 1, 1,0]  # 9
]

# シフトレジスタにパターンを送信する関数
def shift_out(dataPin, clockPin, latchPin, data):
    
    GPIO.output(latchPin, GPIO.LOW)
    for bit in range(0, 8): 
        GPIO.output(clockPin, GPIO.LOW)
        bit_value = (data >> bit) & 1
        GPIO.output(dataPin, bit_value)
        GPIO.output(clockPin, GPIO.HIGH)
    GPIO.output(latchPin, GPIO.HIGH)

def display_digit(digit):
    if digit < 0 or digit > 9:
        raise ValueError("Invalid digit")
    pattern = digit_patterns[digit]
    shift_out(dataPin, clockPin, latchPin, int("".join(map(str, pattern)), 2))

# 消灯させる関数
def turn_off():
    shift_out(dataPin, clockPin, latchPin, 0)

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")


hx.set_reference_unit(referenceUnit)

hx.reset()


# hx.tare()# 初期化後にオフセットを設定する 起動時にものを乗せてても0になる


print("Tare done! Add weight now...")
#GPIO.output(17,1)
# LEDをオンにする
subprocess.run(["python", "led_control.py", "on"])

# ロックファイルを作成して処理を開始
with open("lockfile", "w") as lockfile:
    lockfile.write("locked")

try:
    weight_readings = []

    # 値がぶれているときは測定しないようにする ちょうどものを載せようとしてるときとか取ろうとしてるときとかを避けられる？
    # 次実行するまであんていしてなかったらどうするの
    while True:
        val = hx.get_weight(5) - offset
        print(val)
        weight_readings.append(val)
        time.sleep(0.1)  # 0.5秒ごとに重量を測定
        if len(weight_readings) >= 10:  # 10回の測定を行ったら判定
            stddev = statistics.stdev(weight_readings)
            if stddev < 0.5:  # 標準偏差が1以下であれば安定とみなす
                break
            else:
                weight_readings = []

    nowCount = round(sum(weight_readings) / (len(weight_readings) * 10.5))  # 平均値を計算し、個数に変換
    display_digit(nowCount)
    # 前回の個数が存在し個数変化があった場合にその値を表示
    if preCount is not None and preCount > nowCount and nowCount >=0:
        print("🍫:", preCount - nowCount)
        MSG = character * (preCount - nowCount)
        # MSG+=f"（残り:{nowCount}）"
        # if nowCount<=0:
        #     MSG+=f"（残り:{nowCount}）"

        command = f" {NOSTR_TOOL} -r wss://yabu.me -r wss://nos.lol -r wss://r.kojira.io -r wss://relay-jp.nostr.wirednet.jp -r wss://relay-jp.nostr.moctane.com -p {NSEC} text-note -c {MSG}"
        subprocess.run(command, shell=True)

    # ファイルにpreCountを書き込む
    with open("preCount.txt", "w") as file:
        file.write(str(nowCount))
    time.sleep(3)
    turn_off()

finally:
    # ロックファイルを削除して処理を終了
    os.remove("lockfile")
  
    hx.power_down()
    #GPIO.output(17,0)
    # LEDをoffにする
    subprocess.run(["python", "led_control.py", "off"])
    cleanAndExit()