# synthon

## about synthon
Pythonのユーティリティー集
> shindy + python = synthon


## modules

- ## convert
    変換系モジュール。dict 型から xml を作成する機能等がある。

- ## graphics
    グラフィック系モジュール。画像の生成等を行う。GitHubの初期アイコンのようにビット風の画像を生成する機能もある。

- ## network
    ネットワーク系モジュール。ソケット通信を行うクラス ThreadingTCPServer（サーバーサイド）, Client（クライアントサイド）を用意。Python の標準ライブラリ [socket](https://docs.python.org/ja/3/library/socket.html) のラッパークラスとなる。

- ## os
    osにOSに依存している機能を利用するためのモジュール（のラッパー）。unix系のコマンドを参考にls（ファイルの一覧取得）やwc（ファイルの文字数、行数取得）を用意。

- ## utils
    その他ユーティリティー。関数にデコレータを付与するだけでその関数の処理時間を計測する。