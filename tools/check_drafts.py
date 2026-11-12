#!/usr/bin/env python3
"""G2：逐頁稿檢查（出處 / 數字 / 字數 / 頁數 / 只用大綱指定的卡）。
用法：python3 tools/check_drafts.py <topic_dir> [--json]

逐頁稿格式（drafts/NN.md）：
  第一行 `# 標題`；第二行 `layout: <cover|bullets|tree|interval|table|quiz|bars>`
  `- 內容 [card:頁名#Cn]`        一般主張，必須有 [card:]
  `?? 問題 || 答案 [card:…]`       小測驗
  `| 欄 | 欄 | 欄 [card:…] |`      表格列
  `💡 …`                          教學鷹架（比喻/提問），不得含數字
  `@ …`                           頁面資訊（作者、副標），不得含數字
  `::widget 參數`                  互動元件（數字由 G3 驗證）
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARD_RE = re.compile(r"\[card:([\w-]+)#(C\d+)\]")
NUM_RE = re.compile(r"(?<![\w.])\d+(?:[./]\d+)?%?(?![\w])")
MAX_CHARS = 230          # 每頁可見字數上限（不含出處標記與元件）
MIN_SLIDES, MAX_SLIDES = 8, 15


def load_cards(tdir):
    cards = {}
    for p in (tdir / "cards").glob("*.md"):
        for m in re.finditer(r"^- (C\d+)｜(.+)$", p.read_text(encoding="utf-8"), re.M):
            cards[(p.stem, m.group(1))] = m.group(2)
    return cards


def allowed_cards(tdir):
    """從 outline.md 解析每頁可引用的卡片；『回顧』頁可引用前面所有頁用過的卡。"""
    allowed, review_pages = {}, set()
    for line in (tdir / "outline.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| (\d\d) \|.*\| ([^|]*) \|$", line)
        if not m:
            continue
        sid, cell = m.group(1), m.group(2)
        if cell.strip().startswith("回顧"):
            review_pages.add(sid)
        ids = set()
        for seg in re.finditer(r"([a-z][\w-]+) ((?:C\d+(?:–C\d+)?[、]?)+)", cell):
            page = seg.group(1)
            for part in re.findall(r"C(\d+)(?:–C(\d+))?", seg.group(2)):
                a, b = int(part[0]), int(part[1] or part[0])
                ids |= {(page, f"C{i}") for i in range(a, b + 1)}
        allowed[sid] = ids
    return allowed, review_pages


def visible(line):
    line = CARD_RE.sub("", line)
    line = re.sub(r"^(- |\?\? |💡 |@ )", "", line.strip())
    return line.replace("||", "").replace("|", "")


def main():
    tdir = ROOT / sys.argv[1]
    cards = load_cards(tdir)
    allowed, review_pages = allowed_cards(tdir)
    drafts = sorted((tdir / "drafts").glob("*.md"))
    issues = []
    used_so_far = set()
    if not (MIN_SLIDES <= len(drafts) <= MAX_SLIDES):
        issues.append(("頁數", "deck", f"{len(drafts)} 頁，不在 {MIN_SLIDES}–{MAX_SLIDES}"))
    for d in drafts:
        sid = d.stem
        lines = d.read_text(encoding="utf-8").splitlines()
        chars, cited_any = 0, False
        ok_cards = allowed.get(sid, set()) | (used_so_far if sid in review_pages else set())
        for n, line in enumerate(lines, 1):
            s = line.strip()
            where = f"drafts/{sid}.md:{n}"
            if not s or s.startswith("layout:") or s.startswith("::"):
                continue
            if s.startswith("# "):
                chars += len(s) - 2
                continue
            chars += len(visible(s))
            text_wo_code = re.sub(r"`[^`]*`", "", CARD_RE.sub("", s))
            if s.startswith("💡") or s.startswith("@"):
                if NUM_RE.search(text_wo_code):
                    issues.append(("鷹架含數字", where, "💡/@ 行不得含數字（數字一定要有出處）"))
                continue
            if re.fullmatch(r"\|?[\s:\-|]+\|?", s) or (s.startswith("|") and not NUM_RE.search(s) and not CARD_RE.search(s) and lines[n:n+1] and re.fullmatch(r"\|?[\s:\-|]+\|?", lines[n].strip())):
                continue                                  # 表格分隔線、純標籤表頭
            refs = CARD_RE.findall(s)
            if not refs:
                issues.append(("缺出處", where, f"沒有 [card:]：{s[:40]}"))
                continue
            cited_any = True
            src_text = ""
            for page, cid in refs:
                if (page, cid) not in cards:
                    issues.append(("引用不存在", where, f"[card:{page}#{cid}] 不存在"))
                    continue
                if (page, cid) not in ok_cards:
                    issues.append(("越權引用", where, f"[card:{page}#{cid}] 不在大綱為本頁指定的卡片中"))
                src_text += cards[(page, cid)] + "\n"
                used_so_far.add((page, cid))
            src_nums = set(NUM_RE.findall(re.sub(r"\[(src|calc):[^\]]*\]", "", src_text)))
            for num in NUM_RE.findall(text_wo_code):
                if num not in src_nums:
                    issues.append(("數字查不到", where, f"「{num}」不在所引卡片中"))
        if not cited_any and sid not in ("02",):
            issues.append(("整頁無出處", f"drafts/{sid}.md", "本頁沒有任何 [card:]"))
        if chars > MAX_CHARS:
            issues.append(("字太多", f"drafts/{sid}.md", f"{chars} 字 > {MAX_CHARS}"))
    if "--json" in sys.argv:
        print(json.dumps([dict(type=t, where=w, msg=m) for t, w, m in issues], ensure_ascii=False, indent=2))
    else:
        for t, w, m in issues:
            print(f"[{t}] {w}  {m}")
        print(f"\n頁數 {len(drafts)}｜問題 {len(issues)}")
        print("G2 PASS ✅" if not issues else "G2 FAIL ❌")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
