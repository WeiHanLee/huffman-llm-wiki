#!/usr/bin/env python3
"""把整個 LLM Wiki 輸出成可瀏覽的單頁網站 site/wiki.html（hash 路由，每頁一個 #id）。"""
import html
import json
import re
import subprocess
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC_RE = re.compile(r"\[src:raw/([^\]#]+)\.md#([^\]]+)\]")
CALC_RE = re.compile(r"\[calc:([^\]]+)\]")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def slug(s):
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-")


def md(text, titles):
    text = SRC_RE.sub(lambda m: f'<a class="src" href="#raw-{m.group(1)}--{slug(m.group(2))}" title="raw/{html.escape(m.group(1))}.md#{html.escape(m.group(2))}">{html.escape(m.group(1)[:2])}·{html.escape(m.group(2))}</a>', text)
    text = CALC_RE.sub(lambda m: f'<span class="calc" title="{html.escape(m.group(1), quote=True)}">計算值</span>', text)
    text = LINK_RE.sub(lambda m: f'<a class="wl" href="#w-{m.group(1)}">{html.escape(titles.get(m.group(1), m.group(1)))}</a>', text)
    out = markdown.markdown(text, extensions=["tables", "fenced_code"])
    return out


def raw_md(name, text):
    """raw 檔：每個 ## 章節加錨點。"""
    def anchor(m):
        return f'<h3 id="raw-{name}--{slug(m.group(1))}">{html.escape(m.group(1))}</h3>'
    body = markdown.markdown(text, extensions=["tables"])
    return re.sub(r"<h2>(.+?)</h2>", anchor, body)


def main():
    wiki = {p.stem: p.read_text(encoding="utf-8") for p in sorted((ROOT / "wiki").glob("*.md"))}
    titles = {k: v.splitlines()[0].lstrip("# ").strip() for k, v in wiki.items()}
    order = re.findall(r"\[\[([^\]]+)\]\]", wiki["index"])
    sections = []
    nav = ['<p class="nav-h">Wiki</p>', '<a href="#w-index">目錄 index</a>']
    for name in order:
        nav.append(f'<a href="#w-{name}">{html.escape(titles[name])}</a>')
    nav += ['<p class="nav-h">建置紀錄</p>', '<a href="#about">關於這個 Wiki</a>', '<a href="#discussion">先討論：需求訪談</a>',
            '<a href="#agents">AGENTS.md（員工手冊）</a>', '<a href="#workflow">簡報 Graph 設計</a>', '<a href="#report">一次實際執行報告</a>', '<a href="#w-log">log.md</a>', '<a href="#git">git 紀錄</a>', '<a href="#lint">lint 結果</a>',
            '<p class="nav-h">原始來源 raw/</p>']
    for name in ["index"] + order + ["log"]:
        sections.append(f'<article class="page" id="w-{name}"><p class="path mono">wiki/{name}.md</p>{md(wiki[name], titles)}</article>')
    raws = sorted((ROOT / "raw").glob("*.md"))
    for r in raws:
        t = r.read_text(encoding="utf-8")
        nav.append(f'<a href="#raw-{r.stem}">{html.escape(t.splitlines()[0].lstrip("# ").replace("（Wikipedia）", ""))}</a>')
        sections.append(f'<article class="page raw" id="raw-{r.stem}"><p class="path mono">raw/{r.name}（唯讀）</p>{raw_md(r.stem, t)}</article>')
    for sid, path in [("discussion", "discussion.md"), ("agents", "AGENTS.md"), ("workflow", ".agents/workflows/topic-slides.md"), ("report", "topic-huffman-arith/report.md")]:
        body = markdown.markdown((ROOT / path).read_text(encoding="utf-8"), extensions=["tables", "fenced_code"])
        body = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', lambda m: '<pre class="mermaid">' + m.group(1) + '</pre>', body, flags=re.S)
        sections.append(f'<article class="page" id="{sid}"><p class="path mono">{path}</p>{body}</article>')
    gitlog = subprocess.run(["git", "log", "--reverse", "--format=%h|%ad|%s", "--date=format:%Y-%m-%d %H:%M"], cwd=ROOT, capture_output=True, text=True).stdout.strip().splitlines()
    rows = "".join(f"<tr><td class='mono'>{html.escape(h)}</td><td class='mono'>{html.escape(d)}</td><td>{html.escape(s)}</td></tr>" for h, d, s in (l.split("|", 2) for l in gitlog))
    sections.append(f'<article class="page" id="git"><h1>git 紀錄</h1><p>一次 ingest 一篇、每篇一個 commit（需求第 7 條）。</p><div class="tw"><table><thead><tr><th>commit</th><th>時間</th><th>訊息</th></tr></thead><tbody>{rows}</tbody></table></div></article>')
    lint = subprocess.run(["python3", "tools/lint_wiki.py"], cwd=ROOT, capture_output=True, text=True).stdout
    sections.append(f'<article class="page" id="lint"><h1>lint 結果（目前版本）</h1><p>由 <code>tools/lint_wiki.py</code> 執行 L1 斷鏈、L2 孤兒頁、L3 index 漏列、L4 主張缺出處、L5 數字查不到。</p><pre>{html.escape(lint)}</pre></article>')
    n_claims = sum(len(re.findall(r"\[src:|\[calc:", v)) for k, v in wiki.items() if k not in ("index", "log"))
    about = f"""<article class="page" id="about"><p class="path mono">README</p><h1>資料壓縮 LLM Wiki：Huffman 編碼與算術編碼</h1>
<p>依 Karpathy 的 LLM Wiki 構想，以「先討論、後生成」建立：先由 AI 訪談 8 題釐清需求，確認後才產生 AGENTS.md 與資料夾。</p>
<ul><li>讀者：完全沒學過的同學</li><li>來源：6 篇 Wikipedia 英文條目（raw/，一篇一 commit）</li>
<li>知識頁：{len(wiki) - 2} 頁，共 {n_claims} 個出處標記；每句關鍵主張都標 <span class="src-demo">05·Example</span> 這種出處（點了會跳到 raw 原文章節）</li>
<li>矛盾處理：兩說並列標 ⚠（見 <a class="wl" href="#w-huffman-coding">Huffman 編碼</a> 的年代）</li>
<li>計算值：來源沒有、依來源數字重算的值標 <span class="calc">計算值</span>，算法在 tools/calc.py</li></ul>
<p>建議閱讀順序：左側目錄由上而下。</p></article>"""
    sections.insert(0, about)
    tpl = (ROOT / "tools" / "wiki_template.html").read_text(encoding="utf-8")
    out = tpl.replace("<!--NAV-->", "\n".join(nav)).replace("<!--PAGES-->", "\n".join(sections))
    (ROOT / "site").mkdir(exist_ok=True)
    (ROOT / "site" / "wiki.html").write_text(out, encoding="utf-8")
    print("site/wiki.html", len(out) // 1024, "KB")


if __name__ == "__main__":
    main()
