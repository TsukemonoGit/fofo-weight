referenceUnit = 415

カゴ：56.5~57g
カゴ＋袋＝93.9


```python3 -m venv env```仮想環境を作成することで、プロジェクトごとに独立したPythonの実行環境を用意します。これにより、プロジェクトごとに異なるライブラリのバージョンを使用したり、プロジェクトの依存関係を隔離したりすることができます。また、システム全体のPython環境に影響を与えることなく、プロジェクトごとに管理された環境を作成できます。

`` source env/bin/activate``仮想環境をアクティブにすることで、その環境でPythonコマンドやその他のプロジェクト固有のツールを使用できるようになります。これにより、プロジェクトに必要なパッケージやツールをインストールし、それらを使用する準備が整います。

```
source env/bin/activate
$ python single_run.py
```

backgroundで実行
```
bash bash.sh
```

```
crontab -e

*/10 * * * * bash /path/to/your/bash.sh
```