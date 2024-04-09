import os
import statistics
import subprocess
import time
import sys
import RPi.GPIO as GPIO
from hx711py.hx711 import HX711


WEIGHT_PINS = [5, 6]
FOFO_WEIGHT=10.5
display_duration=5.0# 7seg4桁に表示させる秒数
NSEC, NOSTR_TOOL = sys.argv[1], sys.argv[2]
print(NSEC)
print(NOSTR_TOOL)
character = "🍫"

# ファイルパス
PRE_COUNT_FILE = "preCount.txt"
OFFSET_FILE = "offset.txt"
LOCK_FILE = "lockfile"






def clean_and_exit():
    print("Cleaning...")
    subprocess.run(["python", "led_control.py", "off"])
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def read_file(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return file.read().strip()
    return None


def write_file(filename, data):
    with open(filename, "w") as file:
        file.write(str(data))


def main():
  
    pre_count = int(read_file(PRE_COUNT_FILE) or 0)
    offset = float(read_file(OFFSET_FILE) or 0.0)

    print("offset:", offset)

    if os.path.exists(LOCK_FILE):
        print("Previous execution is still in progress. Exiting...")
        print("Bye!")
        sys.exit()

    hx = HX711(*WEIGHT_PINS)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(414.5)
    hx.reset()

    print("Tare done! Add weight now...")
    subprocess.run(["python", "led_control.py", "on"])

    with open(LOCK_FILE, "w") as lockfile:
        lockfile.write("locked")

    try:
        weight_readings = []
        while True:
            val = hx.get_weight(5) - offset
            print(val)
            weight_readings.append(val)
            
            time.sleep(0.1)
            if len(weight_readings) >= 10:
                stddev = statistics.stdev(weight_readings)
                if stddev < 0.5:
                    break
                else:
                    weight_readings = []

        now_count = round(sum(weight_readings) / (len(weight_readings) * FOFO_WEIGHT))
        subprocess.run(["python", "display_4.py", str(now_count),str(display_duration)])
        digits = [int(d) for d in str(int(min(now_count, 9999))).zfill(4)]
        print(digits)
        

        if pre_count is not None and pre_count > now_count >= 0:
            print("🍫:", pre_count - now_count)
            msg = character * (pre_count - now_count)
            command = f" {NOSTR_TOOL} -r wss://yabu.me -r wss://nos.lol -r wss://r.kojira.io -r wss://relay-jp.nostr.wirednet.jp -r wss://relay-jp.nostr.moctane.com -p {NSEC} text-note -c {msg}"
            subprocess.run(command, shell=True)

        write_file(PRE_COUNT_FILE, now_count)
        #time.sleep(3)
     

    except Exception as e:
        print("An error occurred in the try block:", e)

    finally:
        os.remove(LOCK_FILE)
        hx.power_down()
        subprocess.run(["python", "led_control.py", "off"])
        clean_and_exit()
    

if __name__ == "__main__":
    main()