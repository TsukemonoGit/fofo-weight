import RPi.GPIO as GPIO
import sys
import os

# GPIOピン番号
led_pin = 17

# GPIOのセットアップ
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

# LEDをオンにする関数
def turn_on():
    GPIO.output(led_pin, GPIO.HIGH)

# LEDをオフにする関数
def turn_off():
    GPIO.output(led_pin, GPIO.LOW)

# 外部からの引数を受け取り、LEDを制御する
if __name__ == "__main__":
    # ロックファイルが存在する場合は、前回の実行がまだ終了していないとして終了する
    if os.path.exists("lockfile"):
        print("Previous execution is still in progress. Exiting...")
        sys.exit(1)
    
    # ロックファイルを作成して処理を開始
    with open("led_lockfile", "w") as lockfile:
        lockfile.write("locked")
    
    if len(sys.argv) < 2:
        print("Usage: python led_control.py [on/off]")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "on":
        turn_on()
        print("LED turned on.")
    elif command == "off":
        turn_off()
        print("LED turned off.")
    else:
        print("Invalid command. Please use 'on' or 'off'.")
        sys.exit(1)
    
    # ロックファイルを削除して処理を終了
    os.remove("led_lockfile")