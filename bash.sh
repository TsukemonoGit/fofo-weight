#!/bin/bash
cd `dirname $0`

# 仮想環境をアクティブにする
source env/bin/activate

# Pythonスクリプトをバックグラウンドで実行する
nohup python test.py  &

# 仮想環境を非アクティブにする
deactivate