#!/bin/sh

# MacBookのWifiインターフェース名を手動で入力
ADAPTER="en0"

# Wi-FiがOffの場合は終了
airportpower=`networksetup -getairportpower ${ADAPTER}|cut -d' ' -f4`
if test ${airportpower} = 'Off'; then
  echo 'Wifi is Off.'
  exit
fi

# 接続中のネットワークのSSIDを取得して、それに応じてネットワーク環境を切り替える
ssid=`networksetup -getairportnetwork ${ADAPTER}|cut -d':' -f2|cut -b 2-`

# 接続中のネットワークのSSIDを表示 WiFiに接続する際に使用するエンドポイント名と一致する
echo "SSID: ${ssid}"
