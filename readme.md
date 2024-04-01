# なにこれ

raspberry pi 4B で定期的に（またはスイッチで）アルフォートの重量を測って、
前回測定したときより個数が減っていたら減った分をNostrに投稿する。
<img alt="image" src="![image_path](https://share.yabu.me/84b0c46ab699ac35eb2ca286470b85e081db2087cdef63932236c397417782f5/dd0e8bb0c742f7966c71ed430671f984a93e55bb436ef976e2c9602b7d35cc99.webp)" width="300px">

# 使用したもの 作ったもの
 - raspberry pi 4B
 - 電子スケール（ロードセル+HX711）
 - LED（作動中に点灯）
 - ボタンスイッチ（手動実行用）
 - スケールに乗せるカゴ（エコクラフトで手作り）
 - かごがちょっと小さいのでもっといっぱい乗せるための袋（手作り）

## 参考 HX711ロードセルモジュールを使って、重さを測る
https://zenn.dev/kotaproj/books/raspberrypi-tips/viewer/270_kiso_hx711


## supervisorで常時スイッチ監視用設定

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

## crontabで定期重量監視用設定
```
*/10 * * * * bash /path/to/your/bash.sh
```

### ほか
アルフォートは夏は常温で溶けるのでずっと図りに乗せっぱなしにすることはできない
食べる分だけ冷蔵庫から出して、かごに入れたらスイッチを押して重量記録して使う？