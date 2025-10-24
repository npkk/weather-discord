# weather-discord

Discordにお天気を知らせるだけのアプリ
予報で降り出しそうな時・雨が上がった時に通知する

## how to use

1. `uv sync`する
2. `.env`を書く
    - `.env.sample`の値を埋める
    - 要Yahoo!APIキー(https://developer.yahoo.co.jp/start)
    - LONGITUDE, LATITUDEには天気を取得したい地点を入れる
    - DISCORD_WEBHOOK_URLはお知らせを垂れ流したいチャンネルのWebhook URL
        - `歯車 -> 連携サービス -> ウェブフック -> 新しいウェブフック` から新規作成できる
3. 適当に定時実行させる(cron, systemd.service, etc...)
    - systemd.serviceは`weather-discord.{service,timer}`に記述済み
        - pathは適宜要書き換え

## クレジット表示

下記APIを利用しています

Webサービス by Yahoo! JAPAN （https://developer.yahoo.co.jp/sitemap/）