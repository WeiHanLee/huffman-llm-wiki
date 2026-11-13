# 資料壓縮 LLM Wiki：Huffman 編碼與算術編碼

NTUST 生成式 AI 課程第十週作業：先用「先討論、後生成」建立 LLM Wiki，再用一個 **graph workflow** 把 Wiki 變成教學 HTML 簡報。

## 線上瀏覽
- 入口：https://weihanlee.github.io/huffman-llm-wiki/
- 教學簡報：https://weihanlee.github.io/huffman-llm-wiki/slides.html
- Wiki：https://weihanlee.github.io/huffman-llm-wiki/wiki.html

## 資料夾
| 路徑 | 內容 |
|---|---|
| `discussion.md` | 先討論：8 題需求訪談＋需求摘要（確認後才建檔） |
| `AGENTS.md` / `CLAUDE.md` | 員工手冊（Claude Code 用 `@AGENTS.md` 共用） |
| `raw/` | 6 篇 Wikipedia 條目擷取筆記（唯讀） |
| `wiki/` | 9 個知識頁＋`index.md`＋`log.md` |
| `.agents/workflows/topic-slides.md` | 簡報 graph 規格（五件事、節點權限、退回路線） |
| `tools/` | 每一道檢查關卡都是腳本：`lint_wiki.py`、`retrieve.py`（G1）、`make_cards.py`、`check_drafts.py`（G2）、`render_deck.py`、`check_render.py`（G3）、`calc.py` |
| `topic-huffman-arith/` | 一次實際執行的所有中間產物：`sources.md`、`cards/`、`outline.md`、`drafts/`、`deck.html`、`report.md` |
| `checks/` | 檢查紀錄：lint、G2 突變測試、AI 審查兩輪、G3、截圖 |
| `site/wiki.html` | Wiki 的可瀏覽網頁版 |
| `docs/` | GitHub Pages 用的獨立網頁（入口、簡報、Wiki） |
| `submission/` | 繳交用 Word／PDF |

## 重跑
```bash
python3 tools/lint_wiki.py
python3 tools/retrieve.py topic-huffman-arith      # ① + G1
python3 tools/make_cards.py topic-huffman-arith    # ②（平行）
python3 tools/check_drafts.py topic-huffman-arith  # G2
python3 tools/render_deck.py topic-huffman-arith   # ⑤
python3 tools/check_render.py topic-huffman-arith  # G3（需要 playwright）
```
