# mitm-degubber
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=769590506&skip_quickstart=true)

`mitmproxy` を使ったiOS Simulator用のローカルプロキシ & デバッグツールです。

## 機能

- HTTPS通信の閲覧: iOS Simulator の HTTPS 通信について、暗号化前のデータを傍受します。
- 通信の改竄: iOS Simulator を介して行われるリクエスト/レスポンスを任意のデータに改竄します。

## ユースケース

- アプリなど、リクエストの確認が難しい環境での通信の解析・通信の変化に対する応答の確認に用いることができます。
- Google Tag Manager などを使ってサードパーティーJSの開発を行なっている場合、プレビュー配信が難しい環境で直接コンテンツJSをオーバーライドすることでプレビューを可能にします。
    - 例1. アプリWebViewに配信されているサードパーティー製JavaScriptをローカルのJavaScriptに置き換え、動作を確認する
    - 例2. アプリWebViewに配信されているCSSファイル改竄し、コンテンツを公開することなくサイトの表示を確認する
    - 例3. 動作検証用のSDKを自分の環境にのみ配信し、サイトの詳細な動作を調べる


## 動作環境

- Python: 3.11.0
- pip: 22.3
- GNU Make: 3.81
- マシン: M1 Macbook Air
- OS: Ventura 13.4.1

## セットアップ

### 事前準備
- iOS Similatorをインストールします。
- Python2系,3系の両方を使えるようにしておきます。

### セットアップ

> **Note**
> おすすめのVSCode推奨の拡張機能が `.vscode/extensions.json` に書かれています。必須ではありませんが、必要に応じてインストールしてください。PythonのLinterやFormatterなどが含まれます。

**仮想環境を作成**

仮想環境を作成し、依存関係をインストールします。

```bash
echo 'Info: Setup virtual env...'
python -m venv .venv
. .venv/bin/activate
echo 'Info:  has successfully created, and virtual env has activated.'

echo 'Info: Installing dependencies...'
pip install -r requirements.txt
echo 'Info: Dependencies has successfully installed.'

echo 'Info: Prepare...'
if [ ! -f .env ]; then
    cp .env.sample .env
    echo 'Info: .env file has successfully created. Please rewrite .env file'
else
    echo 'Info: Skip to create .env file. Because it is already exists.'
fi
```

**Proxy用ネットワーク設定を作成**


手順は次を参考にしてください。
- [ネットワークのプロキシ設定を保存する（macOS）](https://zenn.dev/yoshida567/scraps/6f27347bd218b8)

**証明書をMacへインストール**

Macにインストールする証明書をダウンロードし、キーチェーンアクセスに登録します。ダウンロードを以下の手順で行います。

- ネットワークのプロキシ設定を、先ほど作成したプロキシ用の設定に切り替えます。（[参考](https://zenn.dev/yoshida567/scraps/6f27347bd218b8)）
- `make run` で mitmproxy の GUI を起動します。
- プロキシ設定ができていれば http://mitm.it/ へアクセスできます。アクセスしたサイトから macOS 用の証明書をダウンロードします。
- ダウンロードしたらWebサーバを終了します。

続いて、ダウンロードした証明書をキーチェーンアクセスに登録します。以下のスクリプトによって登録を行ってください。（手動で登録してもOKです。）

```bash
# 事前に証明書を mitmproxy-ca-cert.pem という名前で作業ディレクトリに配置しておいてください。
sudo security add-trusted-cert -d -p ssl -p basic -k /Library/Keychains/System.keychain mitmproxy-ca-cert.pem

# 登録が完了したら証明書は消去してOKです。
rm mitmproxy-ca-cert.pem
```

Macで証明書を信頼します。

- キーチェーンアクセスを開く
- `mitmproxy` という証明書を探す
- 証明書を選択し、右クリックメニュー > 情報を見る > 信頼 > この証明書を使用する時 > 常に信頼 と操作
- [参考リンク](https://zenn.dev/link/comments/2129a203238f1b)

**iOS Simulatorに証明書をインストール**

iOS Simulatorに証明書をインストールすることでMac側で通信をプロキシできるようになります。

Python2系(2.7.18など)に切り替えて、以下の手順を実行してください。

```zsh
git clone https://github.com/ADVTOOLS/ADVTrustStore.git
cd ADVTrustStore
./iosCertTrustManager.py -a ~/.mitmproxy/mitmproxy-ca-cert.pem
cd ../
rm -r ADVTrustStore
```

これでインストールは完了です。

以下のように動作確認を行ってください。

### 動作確認1: 通信をキャプチャできていることを確認する
- `make run` によって mitmproxy の GUI を webブラウザで開く
- iOS Simulator で適当なプロトコルHTTPSのサイトを閲覧する
- ブラウザ側で暗号化前の通信が閲覧できればOK。

### 動作確認2: 通信データを改ざんできることを確認する

> **Warning**
> 自身が所有するWebサイトでチェックするなど、問題が起きないように十分気をつけてチェックを行なってください。

HTMLを改竄し、 `window.alert` を呼び出すJavaScriptを挿入してみます。


- `src/interceptor/example_replace.py` の `target_url_regex` をテスト対象のURLを示す正規表現で書き換えます。
- `mitmweb -s src/interceptor/example_replace.py` を実行します。
- テスト対象サイトをiOS Simulator で開きます。
- アラートウィンドウが表示されればOKです。

## 使い方

### iOS Simulator の HTTPS 通信を傍受するには

以下の手順でプロキシサーバを起動します。

- システム環境設定 > ネットワーク > ネットワーク設定 > 作成したプロキシ用の設定に切り替え
- `make run` でGUIを起動
- iOS Simulator で通信を確認したいサイトを閲覧

> **Note**
> プロキシサーバを利用している間は iOS Simulator 以外の通信はブロックされる可能性があります。ネットワーク設定を切り替えればOFFにできるので、必要な時だけプロキシ用のネットワーク設定に切り替えてください。

### リクエスト/レスポンスを改竄するには
通信の改竄は以下の手順で行うことができます。

- `example_insert_js.py` を参考に、通信を改竄する拡張機能を作成します。
- `mitmweb -s src/interceptor/example_replace.py` のように `-s` オプションに利用したい拡張機能を指定して起動します。拡張機能は通信の都度実行されます。
