# なにこれ

raspberry pi 4B で定期的に（またはスイッチで）アルフォートの重量を測って、
前回測定したときより個数が減っていたら減った分をNostrに投稿する。

nostrへの投稿に使用 : https://github.com/0xtrr/nostr-tool 


10分毎に自動で図るようにしてるけどスイッチでも測定できるので、
乗せるごとにスイッチ押して、食べたらスイッチ押して、という使い方でもいいかも

個数リセットボタンは減った分をなかったことにできるので、食べずに再冷蔵するときとかに押す。


<img alt="image" src="https://share.yabu.me/84b0c46ab699ac35eb2ca286470b85e081db2087cdef63932236c397417782f5/70685a0a56daeed0cb1fe4e11ba9117654672af1a75682ca4a50f79309a94381.webp" width="300px">


# 使用したもの 作ったもの
 - raspberry pi 4B
 - 電子スケール（ロードセル+HX711）
 - LED（作動中に点灯）
 - ボタンスイッチ（手動実行用）
 - スケールに乗せるカゴ（エコクラフトで手作り）
 - かごがちょっと小さいのでもっといっぱい乗せるための袋（手作り）
 - 1 Digit 7-Segment Display
 - 74HC595IC

## 参考 
 - HX711ロードセルモジュールを使って、重さを測る - https://zenn.dev/kotaproj/books/raspberrypi-tips/viewer/270_kiso_hx711

 - Arduinoのスターターキット(https://amzn.asia/d/4Nc8rW5)に入ってたCDの中の Elegoo Super Starter Kit for UNO V1.0.19.09.17-日本語.pdf　
## 手動スイッチ用の監視設定supervisor
#### 手動計測用
/etc/supervisor/conf.d/wSwitch.conf
```
[program:wSwitch]
command=python weight_switch.py
autostart=true
autorestart=true
stopsignal=QUIT
directory={weight_switchまでの絶対パス}
stdout_logfile=/var/log/supervisor/wSwitch-err.log
stderr_logfile=/var/log/supervisor/wSwitch-err.log
```

supervisorから起動すると、pythonモジュールがうまく読み込めなかったため、bash.shの方で環境変数を読み込んで、引数で渡すことにした。

#### preCountリセット用
溶けたアルフォートを再冷蔵するときとかに食べてないのに減った判定されるのを防止するため。

```
[program:w_countReset_switch]
command=python countReset_switch.py
autostart=true
autorestart=true
stopsignal=QUIT
directory={weight_switchまでの絶対パス}
stdout_logfile=/var/log/supervisor/w_cr_switch-err.log
stderr_logfile=/var/log/supervisor/w_cr_switch-err.log

```
## crontabで定期重量監視用設定
```
*/10 * * * * bash /path/to/your/bash.sh
```

### ファイルについて
 - cal_ref.py calibratyion.py - ロードセルの設定用
 - digit_test.py - 7セグ1桁ディスプレイのテスト用
 - countReset_switch.py - カウントリセットスイッチ監視用
 - weight_switch.py - 測定スイッチ監視用
 - single_run.py - bash.shを通して引数にNOSTRの秘密鍵とNOSTR-TOOLのパスを指定して実行する
 - .env
    ```
    NSEC_HEX=nostrseckethexkey
    NOSTR_TOOL_PATH=/path/to/nostr-tool
    ```