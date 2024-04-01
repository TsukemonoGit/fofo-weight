#!/bin/bash
cd `dirname $0`
# .envファイルから環境変数を読み込む
source ./.env
# 仮想環境をアクティブにする
source env/bin/activate


# Pythonスクリプトを実行する
python single_run.py $NSEC_HEX

# 仮想環境を非アクティブにする
deactivate

# Pythonスクリプトをバックグラウンドで実行する
#nohup python single_run.py  & # nohup.outにログが出力される
# nohup python test.py > /dev/null 2>&1 & # > /dev/null を使って標準出力を /dev/null にリダイレクトし、2>&1 を使って標準エラー出力を標準出力にリダイレクトしています。これにより、どちらの出力もファイルに保存されずに破棄されます。
# 仮想環境を非アクティブにする
# deactivate