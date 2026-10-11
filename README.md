# morning-brief-feed

Alexa の「定時ニュース（フラッシュニュース）」で読み上げる、自分用モーニングブリーフのフィード。

- フィード URL: https://tanaka50910205.github.io/morning-brief-feed/feed.json
- 毎朝の「ポッドキャスト風ニュース」スケジュールタスクが、ラジオ原稿（episode.json）から `feed.json` を作って push する
- 生成: `python3 scripts/build_feed.py --episode path/to/episode.json`

## 公開範囲について

このリポジトリと GitHub Pages は公開されている。中身は公開ニュースのまとめだけにし、個人的な予定やメールの内容は載せない。
