# ros2_mypkg
Raspberry Piを含むUSB付きシングルボードコンピュータに接続されている外部デバイスを人間が見て分かりやすい製品名で表示するパッケージです。

![](https://github.com/TakeSomen99/ros2_mypkg/actions/workflows/test.yml/badge.svg)
![Static Badge](https://img.shields.io/badge/python-blue)
![CMake](https://img.shields.io/badge/CMake-3.8%2B-blue?logo=cmake)

## 動作環境
+ OS: Ubuntu 24.04 LTS
+ ROS2: Jazzy
+ Python: 3.12.3
+ CMake: 3.28.3
+ 動作確認済み環境:
  + Ubuntu 24.04 LTS
  + Raspberry Pi 3B
  + Python 3.10, 3.11, 3.12
  + CMake 3.26, 3.27, 3.28

## パッケージ・サービス型一覧
|パッケージ名|概要|リンク|
|:---:|:---:|:---:|
|mypkg|USB付きマイコン等から接続されたデバイスの製品名を取得します。|https://github.com/TakeSomen99/mypkg.git|
|device_msgs|本パッケージで扱うメッセージ型を定義します。|https://github.com/TakeSomen99/device_msgs.git|

## 使用方法
本パッケージは以下の2つのファイルを含むサービス型通信を実現します。
+ src/mypkg/mypkg/server.py
+ src/mypkg/mypkg/client.py

また、本パッケージを利用すするにあたり

server.pyはマイコン等外部USB機器を使用する側で起動させてください。起動後server.pyはクライアントの要望に応じてDevice.srvで定義した型に則ってUSBデバイスの名前を送信します。メッセージのデータ型は下記の様にインポートすることが出来ます。
```python
from devicd_msgs.srv import Device
```
具体的なサービスの呼び出し例をclient.pyに記載しています。

以下は**ELECOM製UVC WEBカメラ UCAM-CC310FBBK** をRaspberry Pi 3BのUSB2.0ポートへつないだ時の実行例です。
```bash
$ git clone https://github.com/TakeSomen99/mypkg.git
$ git clone https://github.com/TakeSomen99/device_msgs.git
$ cd mypkg
$ colcon build
$ source install/setup.bash
$ ros2 launch mypkg talk_listen.launch.py
[INFO] [launch]: All log files can be found below /home/ubuntu/.ros/log/2025-12-31-22-06-41-492142-raspberrypi-9802
[INFO] [launch]: Default logging verbosity is set to INFO
[INFO] [server-1]: process started with pid [9805]
[INFO] [client-2]: process started with pid [9806]
[server-1] [INFO] [1767186405.732563583] [device_server]: DeviceService ready. Waiting...
[client-2] ['ELECOM_1MP_Webcam']
[INFO] [client-2]: process has finished cleanly [pid 9806]
```
デバイスを検知できなかった場合 **[client-2] []** と表示されます。ローンチファイルのみ動かした場合も同様の結果となります。本パッケージの起動確認の際にお使いください。

## 備考
現在はUVC対応USBカメラを対象としています。
USBキーボードやマウス、メモリなど、入力デバイスや記憶デバイスには対応しておりません。

## 注意事項
+ Raspberry Pi はRaspberry Pi Ltd. の登録商標または商標です。
+ ELECOM はエレコム株式会社の登録商標または商標です。
+ 本リポジトリ内で言及されている製品名・商標は各権利者に帰属します。
+ 本ソフトウェアは、これらの企業・製品との公式な関係や提携を示すものではありません。

## ライセンス
- このソフトウェアパッケージは，3条項BSDライセンスの下，再頒布および使用が許可されます．
- © 2025 TakeSomen99
