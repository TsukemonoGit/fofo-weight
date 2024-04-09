# python display_4.py 123.001
import RPi.GPIO as GPIO
import time
import sys

# PIN設定
PIN_MAPPING = {
    "data": 11,
    "latch": 9,
    "clock": 10,
    "digits": [25, 8, 7, 1],  # one, two, three, four
}

# 7セグメントLEDのパターン
DIGIT_PATTERNS = [
    [1, 1, 1, 1, 1, 1, 0, 0],  # 0
    [0, 1, 1, 0, 0, 0, 0, 0],  # 1
    [1, 1, 0, 1, 1, 0, 1, 0],  # 2
    [1, 1, 1, 1, 0, 0, 1, 0],  # 3
    [0, 1, 1, 0, 0, 1, 1, 0],  # 4
    [1, 0, 1, 1, 0, 1, 1, 0],  # 5
    [1, 0, 1, 1, 1, 1, 1, 0],  # 6
    [1, 1, 1, 0, 0, 0, 0, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1, 0],  # 8
    [1, 1, 1, 1, 0, 1, 1, 0],   # 9
    [0,0,0,0,0,0,0,0],#無
]
GPIO.setwarnings(False)
def initialize_pins():
    GPIO.setmode(GPIO.BCM)
    for pin in PIN_MAPPING.values():
        GPIO.setup(pin, GPIO.OUT)

# シフトレジスタにパターンを送信する関数
def shift_out(dataPin, clockPin, latchPin, data):
    
    GPIO.output(latchPin, GPIO.LOW)
    for bit in range(0, 8): 
        GPIO.output(clockPin, GPIO.LOW)
        bit_value = (data >> bit) & 1
        GPIO.output(dataPin, bit_value)
        GPIO.output(clockPin, GPIO.HIGH)
    GPIO.output(latchPin, GPIO.HIGH)

def display_digit(digit,num):
    if  digit > 9:
        raise ValueError("Invalid digit")
   
    pattern = DIGIT_PATTERNS[digit]
    if num==1:
        pattern[7]=1
        
    shift_out(PIN_MAPPING["data"], PIN_MAPPING["clock"], PIN_MAPPING["latch"], int("".join(map(str, pattern)), 2))

def turn_off():
    shift_out(PIN_MAPPING["data"], PIN_MAPPING["clock"], PIN_MAPPING["latch"], 0)

def clean_and_exit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

def main():
    initialize_pins()
    if len(sys.argv) < 2:
        print("Usage: python script.py <number> <number>")
        sys.exit(1)
    number = float(sys.argv[1])
    if len(sys.argv) > 2:
      display_time=float(sys.argv[2])
    else:
        # 表示時間
      display_time=3.0
    if  number > 999:
        print("Number must be between 0 and 999")
        sys.exit(1)
    
    number=int(round(number, 1)*10)
    print(number)
    if number>=0:
      digits = [int(d) for d in str(number).zfill(4)]
    else:
      digits=[0,0,0,0] 
    #print(digits)
    #0のばあい10倍しても0になってしまうので0.0にするために
    
    num_digits = len(str(number))

    print("num_digits:",num_digits)
    start_time = time.time()  # 開始時間を記録
    while True:  # 無限ループを追加してLEDの表示を繰り返す
        current_time = time.time()  # 現在の時間を取得
        if current_time - start_time >= display_time:  # 3秒経過したらループを抜ける
            break
        
      
        for i in range(num_digits):  # 4桁分のLEDを制御する
              
                
            GPIO.output(PIN_MAPPING["digits"][i], GPIO.LOW)  # 入力された桁数のみ点灯
            
            display_digit(digits[::-1][i],i)  # 桁ごとに数字を表示
            time.sleep(0.002)
            GPIO.output(PIN_MAPPING["digits"][i], GPIO.HIGH)
             
            time.sleep(0.002)
   
    turn_off()  # LEDを消灯する
    clean_and_exit()
if __name__ == "__main__":
    
    main()