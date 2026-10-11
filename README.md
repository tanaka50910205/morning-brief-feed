# morning-brief-feed

Alexa の「定時ニュース（フラッシュニュース）」で読み上げる、自分用モーニングブリーフのフィード。

- フィード URL: https://tanaka50910205.github.io/morning-brief-feed/feed.json
- 毎朝、Claude のスケジュールタスクが `feed.json` を更新して push する
- 生成: `python3 scripts/build_feed.py "本文"`

## 公開範囲について

このリポジトリと GitHub Pages は公開されている。読み上げ本文には予定名・人名・メール件名などの固有名詞を入れず、「午後に会議が3つ」程度のざっくりした内容にとどめる。
