#!/usr/bin/env python3
"""② 證據卡（平行）：每個相關 wiki 頁各產生一張卡，彼此獨立。
卡片內容＝該頁所有帶 [src:]/[calc:] 的主張，逐字複製、加上編號 C1, C2…，不得改寫。
用法：python3 tools/make_cards.py <topic_dir> [頁名 ...]   （不給頁名＝sources.md 中所有相關頁）
"""
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"


def make_card(tdir: Path, page: str) -> str:
    lines = (WIKI / f"{page}.md").read_text(encoding="utf-8").splitlines()
    title = lines[0].lstrip("# ").strip()
    out = [f"# 證據卡：{title}", f"來源頁：wiki/{page}.md（只抽此頁，不混其他來源）", ""]
    n = 0
    for line in lines:
        s = line.strip()
        if ("[src:" in s or "[calc:" in s) and not s.startswith("#"):
            n += 1
            out.append(f"- C{n}｜{s.lstrip('- ').strip()}")
    (tdir / "cards" / f"{page}.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    return f"{page}: {n} 條主張"


def main() -> int:
    tdir = ROOT / sys.argv[1]
    (tdir / "cards").mkdir(exist_ok=True)
    pages = sys.argv[2:]
    if not pages:
        src = (tdir / "sources.md").read_text(encoding="utf-8")
        pages = re.findall(r"^\| \[\[([^\]]+)\]\] .*✅ \|$", src, re.M)
    with ThreadPoolExecutor() as ex:          # 平行：每張卡只看自己那一頁
        for msg in ex.map(lambda p: make_card(tdir, p), pages):
            print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
