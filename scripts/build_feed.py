#!/usr/bin/env python3
"""Alexa フラッシュニュース（Flash Briefing）用の JSON フィードを生成する。

使い方:
    python3 scripts/build_feed.py "今日の読み上げ本文"
    python3 scripts/build_feed.py --file brief.txt

feed.json を上書きする。Alexa のテキスト読み上げ上限は 4500 文字なので、それを超えた分は切り詰める。
"""
import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
MAX_CHARS = 4500
ROOT = Path(__file__).resolve().parent.parent
FEED_PATH = ROOT / "feed.json"
PAGES_URL = "https://tanaka50910205.github.io/morning-brief-feed/"


def build(text: str) -> dict:
    text = " ".join(text.split())  # 改行や余分な空白を詰める
    if len(text) > MAX_CHARS:
        text = text[: MAX_CHARS - 1] + "…"
    now_jst = datetime.now(JST)
    now_utc = now_jst.astimezone(timezone.utc)
    return {
        "uid": f"morning-brief-{now_jst:%Y%m%d}",
        "updateDate": now_utc.strftime("%Y-%m-%dT%H:%M:%S.0Z"),
        "titleText": f"モーニングブリーフ {now_jst.month}月{now_jst.day}日",
        "mainText": text,
        "redirectionUrl": PAGES_URL,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", help="読み上げ本文")
    parser.add_argument("--file", help="本文を読み込むテキストファイル")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        parser.error("本文か --file を指定してください")

    if not text.strip():
        print("本文が空です", file=sys.stderr)
        return 1

    feed = build(text)
    FEED_PATH.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {FEED_PATH} ({len(feed['mainText'])} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
