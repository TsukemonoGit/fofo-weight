
import os
import statistics
#from dotenv import load_dotenv # ModuleNotFoundError: No module named 'dotenv'
import subprocess
import time
import sys
import RPi.GPIO as GPIO
from hx711py.hx711 import HX711


# 数字モニタ　74HC595
dataPin=25
latchPin=24
clockPin=23

# LED
GPIO.setmode(GPIO.BCM)

GPIO.setup(dataPin,GPIO.OUT)
GPIO.setup(latchPin,GPIO.OUT)
GPIO.setup(clockPin,GPIO.OUT)
# 各数字に対応する7セグメントLEDのパターン
# 数字0から9までのパターンを表す
# [A, B, C, D, E, F, G]の順で各セグメントが点灯するかどうかを表す
digit_patterns = [
    [1, 1, 1, 1, 1, 1, 0], # 0
    [0, 1, 1, 0, 0, 0, 0], # 1
    [1, 1, 0, 1, 1, 0, 1], # 2
    [1, 1, 1, 1, 0, 0, 1], # 3
    [0, 1, 1, 0, 0, 1, 1], # 4
    [1, 0, 1, 1, 0, 1, 1], # 5
    [1, 0, 1, 1, 1, 1, 1], # 6
    [1, 1, 1, 0, 0, 0, 0], # 7
    [1, 1, 1, 1, 1, 1, 1], # 8
    [1, 1, 1, 1, 0, 1, 1]  # 9
]
def shift_out(dataPin, clockPin, latchPin, data):
    for bit in range(7, -1, -1):
        GPIO.output(clockPin, GPIO.LOW)
        GPIO.output(dataPin, data & (1 << bit))
        GPIO.output(clockPin, GPIO.HIGH)
    GPIO.output(latchPin, GPIO.HIGH)
    GPIO.output(latchPin, GPIO.LOW)

def display_digit(digit):
    if digit < 0 or digit > 9:
        raise ValueError("Invalid digit")
    pattern = digit_patterns[digit]
    shift_out(dataPin, clockPin, latchPin, int("".join(map(str, pattern)), 2))

# 消灯させる関数
def turn_off():
    shift_out(dataPin, clockPin, latchPin, 0)


# 一つのセグメントのみ点灯させる関数
def test_segment(segment_index):
    if segment_index < 0 or segment_index > 6:
        raise ValueError("Invalid segment index")
    
    # 一旦全てのセグメントを消灯
    turn_off()
    
    # 指定されたセグメントを点灯
    pattern = [0, 0, 0, 0, 0, 0, 0]  # 全てのセグメントを消灯
    pattern[segment_index] = 1  # 指定されたセグメントを点灯
    shift_out(dataPin, clockPin, latchPin, int("".join(map(str, pattern)), 2))

# 消灯させる関数
def turn_off():
    shift_out(dataPin, clockPin, latchPin, 0)

# テスト実行
for segment_index in range(7):
    print(f"Testing segment {segment_index}")
    test_segment(segment_index)
    time.sleep(1)

# 全てのセグメントを消灯
turn_off()