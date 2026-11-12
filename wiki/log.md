# Wiki 紀錄（log）

## [2026-11-12] init | 依 discussion.md 確認之需求建立 AGENTS.md 與資料夾

## [2026-11-12] ingest 01 | Data compression → 新建 data-compression、lossless-vs-lossy

## [2026-11-12] ingest 02 | Entropy → 新建 entropy；更新 data-compression（加入極限連結）

## [2026-11-12] lint 規則修正 | L5 v1 以「整份 raw 檔子字串」比對，漏抓 entropy 頁的「2 bits」（原文為 two bits，'2' 被 base 2 誤配）。改為 v2：只在所引章節內、以完整數字 token 比對
## [2026-11-12] lint 修正 | entropy：「0」「2」改回來源用字 zero / two bits（3 個 L5）

## [2026-11-12] ingest 03 | Source coding theorem → 新建 source-coding-theorem；更新 entropy（連到定理）
## [2026-11-12] lint 修正 | source-coding-theorem：💡 白話行放在列表內被判缺出處（L4），改為行首 💡

## [2026-11-12] ingest 04 | Shannon–Fano → 新建 shannon-fano；更新 source-coding-theorem。擷取工具的「Huffman 約 2.23 bits」為工具自算，不收入 raw，wiki 改標 [calc:] 並以 tools/calc.py 重算（同法重算 Fano＝2.28，與來源一致）
## [2026-11-12] lint 修正 | shannon-fano：表頭含數字 39 但無出處（L4），補 [src:]

## [2026-11-12] ingest 05 | Huffman coding → 新建 prefix-code、huffman-coding；更新 shannon-fano、data-compression
## [2026-11-12] 矛盾 | Huffman 編碼年代：raw/05 = 1951 修課提出、1952 發表；raw/01 = developed in 1950。兩說並列於 huffman-coding，未裁決
## [2026-11-12] lint 修正 | huffman-coding：「來源 05／01」被 L5 誤判為數字 → 改寫成條目名稱；表頭補出處（L4）

## [2026-11-12] ingest 06 | Arithmetic coding → 新建 arithmetic-coding、huffman-vs-arithmetic；更新 huffman-coding、data-compression。以 tools/calc.py 驗證 0.538 落在 [0.534, 0.54)
## [2026-11-12] lint 修正 | huffman-vs-arithmetic、arithmetic-coding：又把 one bit / powers of two / May 轉成 1、2、5（L5×3），改回來源用字。這是第 3 次同類錯誤 → 寫入 AGENTS.md §4 規則
## [2026-11-12] lint 規則修正 | v3：不含數字的純標籤表頭不視為主張

## [2026-11-12] AI 審查回饋 → 退回 wiki | huffman-vs-arithmetic：①「較慢（需維護區間與精度）」的理由 raw 沒寫 → 改為「來源只說 Huffman 較快」；②應用欄把 raw 的「前綴碼」寫成 Huffman → 改為「前綴碼常用於…；JPEG 實作多用 Huffman」並補 raw/06 出處
## [2026-11-12] 自查 | lossless-vs-lossy：「主角都屬於無失真」是事實主張卻用 💡 逃過 L4 → 改成有出處的一般行（lint 的盲點：💡 行不被檢查）
## [2026-11-12] graph round 2 | 逐頁稿依審查修正（03/04/05/06/07/09/10/11/12/13）；G2 擋下審查員建議的「1/4、1/8」（來源沒有）；13 頁字數超限，小修 4 次才過（超過 workflow 上限 2 輪）
## [2026-11-12] G3 | 參考頁溢出 72px、手機 390px 頁寬 512px → 修 CSS；檢查器 R2 改用 textContent（摺疊的測驗答案）；Google Fonts 連線失敗屬沙盒環境
## [2026-11-12] AI 審查第 2 輪 | 0 錯誤、10 建議 → 可交件；採用 2 項標示建議
## [2026-11-12] graph 修正 | 發現 G2 失敗時渲染仍執行 → 新增 tools/run_graph.sh（set -e）強制關卡；整條 graph 全過
