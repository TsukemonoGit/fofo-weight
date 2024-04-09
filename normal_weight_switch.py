import RPi.GPIO as GPIO
import subprocess
import time

BUTTON_PIN=23
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    # スイッチ押下待ち
    GPIO.wait_for_edge(BUTTON_PIN,GPIO.FALLING)

    #
   
    subprocess.run(["python", "./normal_weight.py"])
    #チャタリング対策
    time.sleep(0.3)
