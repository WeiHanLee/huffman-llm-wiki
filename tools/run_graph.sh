#!/usr/bin/env bash
# 整條 graph：任一關卡失敗（結束碼非 0）就停在那一關，不會往下跑。
set -euo pipefail
T=${1:-topic-huffman-arith}
cd "$(dirname "$0")/.."
echo "== Wiki lint";        python3 tools/lint_wiki.py
echo "== ① 檢索 + G1";      python3 tools/retrieve.py "$T"
echo "== ② 證據卡（平行）";  python3 tools/make_cards.py "$T"
echo "== G2 逐頁稿檢查";     python3 tools/check_drafts.py "$T"
echo "== ⑤ 渲染";           python3 tools/render_deck.py "$T"
echo "== G3 渲染檢查";       python3 tools/check_render.py "$T" | grep -v "高度"
echo "== 全部關卡通過 → 可交件"
