#!/usr/bin/env python3
"""① 檢索 wiki ＋ G1 覆蓋率關卡。
用法：python3 tools/retrieve.py <topic_dir>
讀 <topic_dir>/topic.json：{"title":..., "keywords":[...], "must_cover":{"概念":"wiki頁名", ...}}
輸出 <topic_dir>/sources.md；相關頁 < 3 或必備概念缺頁 → 結束碼 1（停下）。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
SKIP = {"index", "log"}


def main(topic_dir: str) -> int:
    tdir = ROOT / topic_dir
    topic = json.loads((tdir / "topic.json").read_text(encoding="utf-8"))
    kws = [k.lower() for k in topic["keywords"]]
    rows = []
    for p in sorted(WIKI.glob("*.md")):
        if p.stem in SKIP:
            continue
        raw_text = p.read_text(encoding="utf-8")
        claims = len(re.findall(r"\[src:|\[calc:", raw_text))
        text = re.sub(r"\[(src|calc):[^\]]*\]", "", raw_text).lower()   # 出處標記不算命中
        hits = {k: len(re.findall(re.escape(k), text)) for k in kws}
        score = sum(hits.values())
        rows.append((p.stem, score, claims, {k: v for k, v in hits.items() if v}))
    rows.sort(key=lambda r: -r[1])
    relevant = [r for r in rows if r[1] >= 2]

    problems = []
    if len(relevant) < 3:
        problems.append(f"相關頁只有 {len(relevant)} 頁（< 3）→ 依停止條件 ③ 停下")
    rel_names = {r[0] for r in relevant}
    for concept, page in topic["must_cover"].items():
        if page not in rel_names:
            problems.append(f"必備概念「{concept}」沒有對應的相關 wiki 頁（{page}）→ 退回：先 ingest")

    lines = [f"# 檢索結果：{topic['title']}", "",
             f"關鍵字：{', '.join(topic['keywords'])}", "",
             "| wiki 頁 | 關鍵字命中 | 可引用主張數 | 命中明細 | 相關？ |", "|---|---|---|---|---|"]
    for name, score, claims, hits in rows:
        lines.append(f"| [[{name}]] | {score} | {claims} | {', '.join(f'{k}×{v}' for k, v in hits.items())} | {'✅' if score >= 2 else '—'} |")
    lines += ["", "## G1 覆蓋率關卡", ""]
    lines += [f"- 必備概念「{c}」→ [[{p}]] {'✅' if p in rel_names else '❌'}" for c, p in topic["must_cover"].items()]
    lines += ["", f"**結果：{'PASS ✅' if not problems else 'FAIL ❌'}**（相關頁 {len(relevant)} 頁）"]
    lines += [f"- {x}" for x in problems]
    (tdir / "sources.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[-(len(problems) + 1):]))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
