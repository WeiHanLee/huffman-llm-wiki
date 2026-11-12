#!/usr/bin/env python3
"""LLM Wiki lint：依 AGENTS.md §7 檢查 L1–L5。

用法：python3 tools/lint_wiki.py [--json]
結束碼：0 = 全過；1 = 有問題。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
CALC = ROOT / "tools" / "calc_results.json"
EXEMPT_PAGES = {"index", "log"}          # 目錄與紀錄頁不檢查 L4/L5

LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
SRC_RE = re.compile(r"\[src:([^\]#]+)#([^\]]+)\]")
CALC_RE = re.compile(r"\[calc:[^\]]+\]")
# 數字：1/2、0.538、2.205、1952、60%、O(n log n) 的 n 不算
NUM_RE = re.compile(r"(?<![\w.])\d+(?:[./]\d+)?%?(?![\w])")


def raw_headings(path: Path) -> set:
    return {m.group(1).strip() for m in re.finditer(r"^#{2,3}\s+(.+)$", path.read_text(encoding="utf-8"), re.M)}


def raw_section(path: Path, heading: str) -> str:
    """只回傳 raw 檔中指定 ## 章節的內容（v2：避免整檔子字串誤判）。"""
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"^#{{2,3}}\s+{re.escape(heading)}\s*$(.*?)(?=^#{{2,3}}\s|\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def strip_markup(line: str) -> str:
    line = SRC_RE.sub("", line)
    line = CALC_RE.sub("", line)
    line = LINK_RE.sub("", line)
    line = re.sub(r"`[^`]*`", "", line)            # 行內程式碼（如 codeword 010）不當數字主張
    return line


def numbers_in(text: str) -> list:
    out = []
    for m in NUM_RE.finditer(text):
        tok = m.group(0)
        out.append(tok)
    return out


def is_content(line: str, next_is_sep: bool = False) -> bool:
    s = line.strip()
    if not s or s.startswith("#") or s.startswith("💡") or s.startswith("相關："):
        return False
    if re.fullmatch(r"\|?[\s:\-|]+\|?", s):       # 表格分隔線
        return False
    if s.startswith("|") and next_is_sep and not re.search(r"\d", s):   # 純標籤表頭（v3）
        return False
    return True


def main() -> int:
    issues = []
    pages = {p.stem: p for p in WIKI.glob("*.md")}
    calc_values = set()
    if CALC.exists():
        calc_values = {str(v) for v in json.loads(CALC.read_text(encoding="utf-8")).values()}

    inbound = {name: set() for name in pages}
    for name, path in pages.items():
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        for lineno, line in enumerate(lines, 1):
            nxt = lines[lineno] if lineno < len(lines) else ""
            next_is_sep = bool(re.fullmatch(r"\|?[\s:\-|]+\|?", nxt.strip())) and "-" in nxt
            # L1 斷鏈
            for target in LINK_RE.findall(line):
                target = target.strip()
                if target not in pages:
                    issues.append(("L1", f"wiki/{name}.md:{lineno}", f"[[{target}]] 指向不存在的頁面"))
                elif target != name:
                    inbound[target].add(name)
            if name in EXEMPT_PAGES or not is_content(line, next_is_sep):
                continue
            srcs = SRC_RE.findall(line)
            has_calc = bool(CALC_RE.search(line))
            # L4 缺出處 / 出處無效
            if not srcs and not has_calc:
                issues.append(("L4", f"wiki/{name}.md:{lineno}", f"主張缺出處：{line.strip()[:50]}"))
                continue
            raw_texts = []
            for fname, heading in srcs:
                rp = ROOT / fname.strip()
                if not rp.exists():
                    issues.append(("L4", f"wiki/{name}.md:{lineno}", f"引用的 raw 檔不存在：{fname}"))
                    continue
                if heading.strip() not in raw_headings(rp):
                    issues.append(("L4", f"wiki/{name}.md:{lineno}", f"{fname} 沒有章節「{heading}」"))
                raw_texts.append(raw_section(rp, heading.strip()))
            # L5 數字可追溯（v2：只在所引章節內、以完整數字 token 比對）
            source_nums = set(numbers_in("\n".join(raw_texts)))
            for num in numbers_in(strip_markup(line)):
                if num in source_nums:
                    continue
                if has_calc and num in calc_values:
                    continue
                issues.append(("L5", f"wiki/{name}.md:{lineno}", f"數字「{num}」在所引來源中找不到"))

    # L2 孤兒頁、L3 index 漏列
    index_text = pages["index"].read_text(encoding="utf-8") if "index" in pages else ""
    index_links = set(LINK_RE.findall(index_text))
    for name in pages:
        if name in EXEMPT_PAGES:
            continue
        if name not in index_links:
            issues.append(("L3", f"wiki/{name}.md", "index.md 未列出此頁"))
        if not (inbound[name] - {"index", "log"}):
            issues.append(("L2", f"wiki/{name}.md", "孤兒頁：除 index 外沒有任何頁面連到它"))

    if "--json" in sys.argv:
        print(json.dumps([dict(code=c, where=w, msg=m) for c, w, m in issues], ensure_ascii=False, indent=2))
    else:
        counts = {}
        for c, w, m in issues:
            counts[c] = counts.get(c, 0) + 1
            print(f"[{c}] {w}  {m}")
        print(f"\n頁數 {len(pages)}｜問題 {len(issues)}  " + " ".join(f"{k}:{v}" for k, v in sorted(counts.items())))
        print("LINT PASS ✅" if not issues else "LINT FAIL ❌")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
