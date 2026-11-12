#!/usr/bin/env python3
"""⑤ 渲染 HTML（決定性）：drafts/*.md → deck.html。
只做「格式轉換」，不改任何一個字；所有文字原樣 HTML-escape 後放入。
用法：python3 tools/render_deck.py <topic_dir>
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARD_RE = re.compile(r"\[card:([\w-]+)#(C\d+)\]")
SRC_RE = re.compile(r"\[src:([^\]#]+)#([^\]]+)\]")


def load_cards(tdir):
    cards = {}
    for p in (tdir / "cards").glob("*.md"):
        for m in re.finditer(r"^- (C\d+)｜(.+)$", p.read_text(encoding="utf-8"), re.M):
            cards[(p.stem, m.group(1))] = m.group(2)
    return cards


def clean_claim(t):
    t = SRC_RE.sub("", t)
    t = re.sub(r"\[calc:[^\]]*\]", "（計算值）", t)
    t = re.sub(r"\[\[([^\]]+)\]\]", r"\1", t)
    return t.replace("`", "").strip()


def inline(text):
    """escape，並把 `code` 轉成 <code>。"""
    parts = re.split(r"(`[^`]*`)", text)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) >= 2:
            out.append(f"<code>{html.escape(p[1:-1])}</code>")
        else:
            out.append(html.escape(p))
    return "".join(out)


def refs_html(refs, cards):
    tags = []
    for page, cid in refs:
        tip = html.escape(f"wiki/{page}.md {cid}：{clean_claim(cards.get((page, cid), '?'))}", quote=True)
        tags.append(f'<span class="ref" tabindex="0" data-tip="{tip}">{html.escape(page)} {cid}</span>')
    return f'<span class="refs">{"".join(tags)}</span>'


def parse_widget(line):
    kind, *args = line[2:].split()
    params = {}
    for a in args:
        k, _, v = a.partition("=")
        params[k] = v
    return kind, params


def render_slide(path, cards, idx, total):
    lines = path.read_text(encoding="utf-8").splitlines()
    title = lines[0][2:].strip()
    layout = "bullets"
    items, widget, table, quiz, subs = [], None, [], [], []
    used = []
    for raw in lines[1:]:
        s = raw.strip()
        if not s:
            continue
        if s.startswith("layout:"):
            layout = s.split(":", 1)[1].strip()
            continue
        if s.startswith("::"):
            widget = parse_widget(s)
            continue
        refs = CARD_RE.findall(s)
        used += [r for r in refs if r not in used]
        body = CARD_RE.sub("", s).rstrip()
        if s.startswith("@ "):
            subs.append(f'<p class="sub">{inline(body[2:])}</p>')
        elif s.startswith("💡"):
            items.append(f'<li class="hint"><span class="hint-mark" aria-hidden="true">💡</span><span>{inline(body[1:].strip())}</span></li>')
        elif s.startswith("?? "):
            q, _, a = body[3:].partition("||")
            quiz.append(f'<details class="quiz"><summary>{inline(q.strip())}</summary><p>{inline(a.strip())} {refs_html(refs, cards)}</p></details>')
        elif s.startswith("|"):
            if re.fullmatch(r"\|?[\s:\-|]+\|?", s):
                continue
            cells = [c.strip() for c in body.strip("|").split("|")]
            table.append((cells, refs))
        elif s.startswith("- "):
            warn = body[2:].startswith("⚠")
            items.append(f'<li class="{"warn" if warn else "claim"}"><span>{inline(body[2:])}</span> {refs_html(refs, cards)}</li>')
    # 組合
    parts = [f'<h2 class="title">{inline(title)}</h2>']
    if layout == "cover":
        parts = [f'<p class="eyebrow mono">0100 1000 · 0101 0101 · 0100 0110</p><h1 class="cover-title">{inline(title)}</h1>'] + subs[:1]
        parts.append(f'<ul class="items cover-items">{"".join(items)}</ul>')
        parts += subs[1:]
    else:
        main = ""
        if table:
            head, *rows = table
            th = "".join(f"<th>{inline(c)}</th>" for c in head[0])
            trs = ""
            for cells, refs in rows:
                tds = "".join(f"<td>{inline(c)}</td>" for c in cells)
                trs += f"<tr>{tds}<td class='refcell'>{refs_html(refs, cards)}</td></tr>"
            main += f'<div class="table-wrap"><table><thead><tr>{th}<th class="refcell">出處</th></tr></thead><tbody>{trs}</tbody></table></div>'
        if items:
            main += f'<ul class="items">{"".join(items)}</ul>'
        if quiz:
            main += f'<div class="quizzes"><p class="quiz-label">小測驗（點題目看答案）</p>{"".join(quiz)}</div>'
        if widget:
            kind, params = widget
            data = json.dumps(params, ensure_ascii=False)
            wid = f'<figure class="widget" data-widget="{kind}" data-params=\'{html.escape(data, quote=True)}\'></figure>'
            parts.append(f'<div class="split"><div class="col">{main}</div><div class="col">{wid}</div></div>')
        else:
            parts.append(main)
    pages = []
    for p, _ in used:
        if p not in pages:
            pages.append(p)
    foot_src = "、".join(f"wiki/{p}" for p in pages) if pages else "導覽頁（無事實主張）"
    footer = (f'<footer class="slide-foot"><span class="mono">📚 出處：{html.escape(foot_src)}</span>'
              f'<span class="mono">{idx:02d} / {total:02d}</span></footer>')
    return (f'<section class="slide layout-{layout}" id="s{idx}" data-draft="{path.stem}" aria-label="第 {idx} 頁：{html.escape(title, quote=True)}">'
            f'<div class="slide-body">{"".join(parts)}</div>{footer}</section>'), pages


def references_slide(all_pages, idx, total):
    rows = []
    for page in all_pages:
        text = (ROOT / "wiki" / f"{page}.md").read_text(encoding="utf-8")
        title = text.splitlines()[0].lstrip("# ").strip()
        raws = sorted({r for r, _ in SRC_RE.findall(text)})
        links = []
        for r in raws:
            rt = (ROOT / r).read_text(encoding="utf-8")
            url = re.search(r"URL: (\S+)", rt).group(1)
            name = rt.splitlines()[0].lstrip("# ").replace("（Wikipedia）", "")
            links.append(f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">{html.escape(name)}</a>')
        rows.append(f"<tr><td class='mono'>wiki/{html.escape(page)}</td><td>{html.escape(title)}</td><td>{'、'.join(links)}</td></tr>")
    return (f'<section class="slide layout-refs" id="s{idx}" data-draft="refs" aria-label="第 {idx} 頁：參考來源">'
            f'<div class="slide-body"><h2 class="title">參考來源：簡報 → Wiki → 原始條目</h2>'
            f'<div class="table-wrap"><table class="refs-table"><thead><tr><th>Wiki 頁</th><th>主題</th><th>原始來源（raw/，Wikipedia 英文條目，2026-11-12 擷取）</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="sub small">每一句的出處標籤（如「entropy C6」）＝ 證據卡編號，滑過去可看 wiki 原句；證據卡再指回 raw 章節。</p></div>'
            f'<footer class="slide-foot"><span class="mono">📚 由 tools/render_deck.py 自動產生</span><span class="mono">{idx:02d} / {total:02d}</span></footer></section>')


def main():
    tdir = ROOT / sys.argv[1]
    cards = load_cards(tdir)
    drafts = sorted((tdir / "drafts").glob("*.md"))
    total = len(drafts) + 1
    slides, all_pages = [], []
    for i, d in enumerate(drafts, 1):
        h, pages = render_slide(d, cards, i, total)
        slides.append(h)
        all_pages += [p for p in pages if p not in all_pages]
    slides.append(references_slide(all_pages, total, total))
    tpl = (ROOT / "tools" / "deck_template.html").read_text(encoding="utf-8")
    out = tpl.replace("<!--SLIDES-->", "\n".join(slides))
    (tdir / "deck.html").write_text(out, encoding="utf-8")
    print(f"deck.html：{total} 頁（{len(drafts)} 頁內容＋參考來源）")


if __name__ == "__main__":
    main()
