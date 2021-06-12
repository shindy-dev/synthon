# synthon

## synthon とは
Python でコーディングする際に便利そうなモジュール群です。  
synthon の由来は以下の通り。（意外と気に入ってます笑）
> shindy + python = synthon

## モジュール
- ## convert
    変換系モジュール。dict 型から xml を作成する機能等がある。
- ## network
    ネットワーク系モジュール。ソケット通信を行うクラス ThreadingTCPServer（サーバーサイド）, Client（クライアントサイド）を用意。Python の標準ライブラリ [socket](https://docs.python.org/ja/3/library/socket.html) のラッパークラスとなる。

- ## os
    osにOSに依存している機能を利用するためのモジュール（のラッパー）。unix系のコマンドを参考にls（ファイルの一覧取得）やwc（ファイルの文字数、行数取得）を用意。

- ## utils
    その他ユーティリティー。関数にデコレータを付与するだけでその関数の処理時間を計測する。