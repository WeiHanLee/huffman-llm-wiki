#!/usr/bin/env python3
"""G3：渲染檢查（Playwright 實際開啟 deck.html）。
R1 每頁內容區不溢出（1280×720 舞台）
R2 逐頁稿每一句可見文字都原樣出現在對應投影片（渲染不得改字）
R3 互動元件：Huffman 樹算出的碼字＝證據卡碼字；算術編碼區間＝tools/calc_results.json；長條圖數值都在卡片中
R4 手機寬度（390px）頁面不橫向捲動
R5 無 console error
用法：python3 tools/check_render.py <topic_dir>   截圖存到 checks/shots/
"""
import json
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CARD_RE = re.compile(r"\[card:[^\]]+\]")


def norm(s):
    return re.sub(r"\s+", "", s)


def draft_segments(path):
    segs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith(("layout:", "::")) or re.fullmatch(r"\|?[\s:\-|]+\|?", s):
            continue
        s = CARD_RE.sub("", s).replace("`", "")
        s = re.sub(r"^(# |- |\?\? |💡 ?|@ )", "", s)
        for part in re.split(r"\|\||\|", s):
            if part.strip():
                segs.append(part.strip())
    return segs


def main():
    tdir = ROOT / sys.argv[1]
    shots = ROOT / "checks" / "shots"
    shots.mkdir(parents=True, exist_ok=True)
    issues, notes = [], []
    cards = (tdir / "cards" / "huffman-coding.md").read_text(encoding="utf-8")
    expected_codes = dict(re.findall(r"\| ([a-e]) \| [\d.]+ \| `([01]+)` \|", cards))
    calc = json.loads((ROOT / "tools" / "calc_results.json").read_text(encoding="utf-8"))
    expected_iv = [[str(calc[f"ac_step{i}_lo"]).rstrip("0").rstrip(".") if calc[f"ac_step{i}_lo"] else "0",
                    str(calc[f"ac_step{i}_hi"])] for i in (1, 2, 3)]
    sf_card = (tdir / "cards" / "shannon-fano.md").read_text(encoding="utf-8") + json.dumps(calc)

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 860})
        errors = []
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto((tdir / "deck.html").as_uri())
        pg.wait_for_timeout(800)
        n = pg.evaluate("window.__deck.count")
        drafts = {d.stem: d for d in (tdir / "drafts").glob("*.md")}
        for i in range(n):
            pg.evaluate(f"window.__deck.show({i})")
            pg.evaluate("document.querySelectorAll('.slide.active .widget').forEach(f => f.__finish && f.__finish())")
            pg.wait_for_timeout(120)
            info = pg.evaluate("""() => { const s = document.querySelector('.slide.active'); const b = s.querySelector('.slide-body');
                const r = b.getBoundingClientRect(); let worst = 0;
                b.querySelectorAll('*').forEach(e => { const q = e.getBoundingClientRect(); if (q.height) worst = Math.max(worst, q.bottom - r.bottom, q.right - r.right); });
                return { id: s.dataset.draft, sh: b.scrollHeight, ch: b.clientHeight, sw: b.scrollWidth, cw: b.clientWidth, worst, text: s.textContent }; }""")
            tag = f"第 {i+1} 頁（draft {info['id']}）"
            if info["sh"] > info["ch"] + 1 or info["sw"] > info["cw"] + 1 or info["worst"] > 1:
                issues.append(("R1 溢出", tag, f"內容 {info['sh']}px > 可用 {info['ch']}px（超出 {info['worst']:.0f}px）"))
            else:
                notes.append(f"{tag} 高度 {info['sh']}/{info['ch']}px")
            pg.locator(".slide.active").screenshot(path=str(shots / f"slide-{i+1:02d}.png"))
            if info["id"] in drafts:
                text = norm(info["text"])
                for seg in draft_segments(drafts[info["id"]]):
                    if norm(seg) not in text:
                        issues.append(("R2 改字", tag, f"稿件句子沒有原樣出現：{seg[:30]}"))
        codes = pg.evaluate("window.__huffmanCodes")
        if codes != expected_codes:
            issues.append(("R3 元件", "Huffman 樹", f"算出 {codes}，卡片是 {expected_codes}"))
        else:
            notes.append(f"Huffman 樹碼字＝卡片：{codes}")
        iv = pg.evaluate("window.__intervals")
        if iv != expected_iv:
            issues.append(("R3 元件", "算術編碼區間", f"算出 {iv}，calc 是 {expected_iv}"))
        else:
            notes.append(f"算術區間＝calc：{iv}")
        for v in re.findall(r"=(\d+\.\d+)", (tdir / "drafts" / "10.md").read_text(encoding="utf-8").split("::bars")[1]):
            if v not in sf_card:
                issues.append(("R3 元件", "長條圖", f"數值 {v} 不在卡片/calc 中"))
        # 深色模式截圖
        pg.emulate_media(color_scheme="dark")
        for i in (0, 8, 11):
            pg.evaluate(f"window.__deck.show({i})")
            pg.locator(".slide.active").screenshot(path=str(shots / f"dark-{i+1:02d}.png"))
        # R4 手機
        m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        m.goto((tdir / "deck.html").as_uri())
        m.wait_for_timeout(600)
        sw = m.evaluate("document.documentElement.scrollWidth")
        if sw > 391:
            issues.append(("R4 手機", "390px", f"頁面寬 {sw}px，會橫向捲動"))
        else:
            notes.append(f"手機 390px：頁寬 {sw}px，無橫向捲動")
        m.screenshot(path=str(shots / "phone.png"))
        b.close()
    env = [e for e in errors if "ERR_TUNNEL_CONNECTION_FAILED" in e]
    real = [e for e in errors if e not in env]
    if env:
        notes.append(f"環境：沙盒無法連到 Google Fonts（{len(env)} 筆），以系統字型 Noto Sans CJK TC 量測；發布後正常載入")
    if real:
        issues.append(("R5 console", "deck", "; ".join(real[:3])))
    for t, w, msg in issues:
        print(f"[{t}] {w}  {msg}")
    print("\n".join("  · " + x for x in notes))
    print(f"\n問題 {len(issues)}")
    print("G3 PASS ✅" if not issues else "G3 FAIL ❌")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
