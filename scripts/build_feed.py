#!/usr/bin/env python3
"""Alexa フラッシュニュース（Flash Briefing）用の JSON フィードを生成する。

使い方:
    # 毎朝のラジオ原稿（episode.json）から、全コーナーを1項目にまとめたフィードを作る
    python3 scripts/build_feed.py --episode /mnt/project-files/morning-news/episode.json

    # 任意の本文1つで作る（テスト用）
    python3 scripts/build_feed.py "読み上げ本文"

feed.json を上書きする。Alexa はフィード1つにつき5項目までしか読まないため、全コーナーを1項目にまとめる。
テキスト読み上げ上限は1項目 4500 文字なので、超えた分は切り詰める。
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


def clean(text: str) -> str:
    text = " ".join(str(text).split())
    if len(text) > MAX_CHARS:
        text = text[: MAX_CHARS - 1] + "…"
    return text


def item(uid: str, when_utc: datetime, title: str, text: str) -> dict:
    return {
        "uid": uid,
        "updateDate": when_utc.strftime("%Y-%m-%dT%H:%M:%S.0Z"),
        "titleText": title,
        "mainText": clean(text),
        "redirectionUrl": PAGES_URL,
    }


def from_text(text: str) -> list:
    now = datetime.now(JST)
    return [item(f"morning-brief-{now:%Y%m%d}", now.astimezone(timezone.utc),
                 f"モーニングブリーフ {now.month}月{now.day}日", text)]


def from_episode(path: Path) -> list:
    ep = json.loads(path.read_text(encoding="utf-8"))
    segments = [s for s in ep.get("segments", []) if str(s.get("text", "")).strip()]
    if not segments:
        raise ValueError("episode.json に読み上げられる segments がありません")
    now = datetime.now(JST)
    date_key = str(ep.get("date") or now.strftime("%Y-%m-%d")).replace("-", "")
    title = ep.get("dateLabel") or f"モーニングブリーフ {now.month}月{now.day}日"
    # Alexa はフィード1つにつき最大5項目しか読まないので、全コーナーを1項目にまとめる
    text = " ".join(str(s["text"]).strip() for s in segments)
    return [item(f"morning-radio-{date_key}", now.astimezone(timezone.utc).replace(microsecond=0), title, text)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", help="読み上げ本文（テスト用）")
    parser.add_argument("--episode", help="ラジオ原稿の episode.json")
    args = parser.parse_args()

    if args.episode:
        feed = from_episode(Path(args.episode))
    elif args.text and args.text.strip():
        feed = from_text(args.text)
    else:
        parser.error("--episode か本文を指定してください")

    FEED_PATH.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(x["mainText"]) for x in feed)
    print(f"wrote {FEED_PATH} ({len(feed)} items, {total} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
