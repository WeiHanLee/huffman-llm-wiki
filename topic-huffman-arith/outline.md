# 大綱：Huffman 與算術編碼入門——用更少的 bit 說同一件事

讀者：完全沒學過的同學｜長度：14 頁（限制 8–15）｜每頁只引用列出的卡片

## 學習目標（看完能回答）
1. 為什麼「常見的東西用短碼」就能壓縮？極限在哪？
2. Huffman 編碼怎麼建樹、怎麼解碼？
3. 算術編碼跟 Huffman 差在哪？為什麼 Huffman 還是到處都是？

## 教學弧線
動機（為什麼壓縮）→ 極限（熵）→ 規則（前綴碼）→ 方法演進（Shannon–Fano → Huffman → 算術編碼）→ 比較 → 回顧

| # | 頁標題 | 教學目的 | 引用卡片 |
|---|---|---|---|
| 01 | 封面：用更少的 bit 說同一件事 | 引起興趣 | data-compression C1 |
| 02 | 今天的路線圖 | 預告三個學習目標 | — （導覽頁） |
| 03 | 壓縮是什麼？無失真 vs 失真 | 建立基本詞彙 | data-compression C1–C3、lossless-vs-lossy C1、C5、C6、C7 |
| 04 | 熵：資料「有多難猜」 | 直覺理解熵（擲硬幣）＋常見用短碼為何能壓縮 | entropy C1、C4、C6、C7、C10 |
| 05 | 壓縮的地板：信源編碼定理 | 知道極限存在 | entropy C11、source-coding-theorem C1–C3 |
| 06 | 規則：前綴碼 | 為何 0/1 串能唯一解碼 | prefix-code C1、C4 |
| 07 | 第一次嘗試：Shannon–Fano 由上往下切 | 方法演進起點 | shannon-fano C1–C4 |
| 08 | Huffman 的故事：一份期末報告 | 人物與動機（含 ⚠ 年代矛盾） | huffman-coding C2、C3、C5、C6 |
| 09 | Huffman 三步驟（互動建樹） | 會手算建樹 | huffman-coding C7–C9、C11–C15 |
| 10 | 成績單：離熵多近？ | 用數字看效果 | huffman-coding C16、shannon-fano C12、C13 |
| 11 | Huffman 的天花板：整數 bit | 引出算術編碼的動機 | huffman-vs-arithmetic C1–C4、huffman-coding C18 |
| 12 | 算術編碼：把訊息縮成一個小數（互動切區間） | 理解區間切分 | arithmetic-coding C2、C3、C5–C8 |
| 13 | 怎麼選？對照表 | 比較與工程取捨 | huffman-vs-arithmetic C5、C7、C8、C9、huffman-coding C20、arithmetic-coding C12 |
| 14 | 重點回顧＋小測驗 | 檢核學習目標 | 回顧前頁卡片：huffman-coding C1、huffman-vs-arithmetic C1、arithmetic-coding C2、entropy C12 |

附：最後一個區塊列出「參考來源」（wiki 頁 → raw → Wikipedia URL），不算頁數。

## 修訂紀錄
- 2026-11-12 使用者確認大綱（14 頁）。
- 2026-11-12 依 AI 審查第 1 輪：頁序與頁數不變，僅擴充 03/04/05/07/11/12/13 可引用的卡片（補術語定義、學習目標 1 的機制、專利史實）。
