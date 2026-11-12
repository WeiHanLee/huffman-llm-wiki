# AI 審查報告（第 1 輪，獨立對話）

審查範圍：topic-huffman-arith/drafts/01–14.md，逐句對照 cards/*.md 與 raw/01–06。數值例子都已重算：Huffman 樹 a–e 的合併順序和碼字與 raw/05 Example 相符；區間 [0.48, 0.54)、[0.534, 0.54) 算出來正確；(15×1+24×3)/39 = 2.2308。

## 忠實度
| 頁 | 句子（節錄） | 問題 | 嚴重度（錯誤/建議） | 依據（卡片/raw 章節） | 建議退回到哪一關（逐頁稿/證據卡/wiki） |
|---|---|---|---|---|---|
| 13 | 速度：算術編碼「較慢（需維護區間與精度）」 | 括號裡的因果沒有來源。卡片指向的 raw/06 #Precision and renormalization 只講固定精度、四捨五入和重新正規化，沒有說這會讓算術編碼變慢。「Huffman 較快」的依據只有 raw/05 #Optimality 的「Huffman coding is faster」。這個理由從 wiki/huffman-vs-arithmetic.md 第 16 行就有了，卡片 C7 原樣抄過來。 | 錯誤 | huffman-vs-arithmetic#C7；raw/05#Optimality；raw/06#Precision and renormalization | wiki（刪掉括號理由，或改成只寫「Huffman 較快」並引 raw/05#Optimality），再重新產卡 |
| 13 | 常見應用：Huffman 欄寫「DEFLATE（gzip）、JPEG、MP3」 | raw/05 #Applications 原文是「Prefix codes are widely used as a back-end stage… DEFLATE…, JPEG, and MP3」，主詞是「前綴碼」，不是 Huffman。huffman-coding#C21 寫的是「前綴碼」（正確），但比較卡 C9 把它放進 Huffman 欄，等於推論超出來源。raw 裡只有 JPEG 有直接支持：raw/06 #History and patents 說「JPEG implementations mostly use Huffman coding」。 | 錯誤 | huffman-vs-arithmetic#C9；huffman-coding#C21；raw/05#Applications；raw/06#History and patents | wiki（改成「前綴碼常用於 DEFLATE、JPEG、MP3；JPEG 實作多用 Huffman」），再重新產卡 |
| 13 | 「…但 Huffman 比較快、沒有專利包袱，**所以仍然到處都是**。」[card:huffman-coding#C20] | C20 和 raw/05 #Optimality 只說「算術編碼較貼近真實機率，但 Huffman 較快、歷史上沒有專利問題」，沒有「所以到處都是」這個因果結論。這句是從 wiki/huffman-vs-arithmetic.md 第 24 行的 💡 個人看法，變成帶出處的事實句。raw 裡最接近的支持是 raw/06 #History and patents：專利顧慮讓 bzip2 放棄算術編碼，JPEG 實作多用 Huffman（arithmetic-coding#C12），但本頁沒有引用。這句是學習目標 3 的答案，不能沒有來源。 | 錯誤 | huffman-coding#C20；arithmetic-coding#C12；raw/05#Optimality；raw/06#History and patents | 逐頁稿（加引 arithmetic-coding#C12，改寫成來源說得出的事實，例如「專利顧慮曾讓 bzip2 放棄算術編碼、JPEG 實作多用 Huffman」；「到處都是」若要保留，改成 💡 比喻並標明是推論） |
| 11 | 「只有機率剛好是**二的次方**時，Huffman 才會達到熵。」 | 卡片照 raw/06 寫「powers of two」，但對零基礎讀者，「二的次方」會被讀成 2、4、8，而機率不可能是這些數。raw/05 #Optimality 的寫法是「powers of 1/2」，huffman-coding#C18 也寫「1/2 的次方」。建議改成「1/2、1/4、1/8…這種 1/2 的次方」。 | 建議 | huffman-vs-arithmetic#C3；huffman-coding#C18；raw/05#Optimality；raw/06#Huffman coding | 逐頁稿 |
| 11 | 「Huffman 完全壓不了——每個符號還是要一個 bit」 | 卡片和 raw 都寫「單純的（plain）Huffman」，因為把符號分組（blocking）可以改善（raw/06 同段、huffman-vs-arithmetic#C4）。逐頁稿把「單純的」拿掉，說法變絕對了。 | 建議 | huffman-vs-arithmetic#C2、C4；raw/06#Huffman coding | 逐頁稿 |
| 10 | 「Huffman 約 2.23 bits」[card:shannon-fano#C13]；長條圖 Huffman=2.23 | 這個數字是自己算的（calc），不是來源數字。raw/04 檔頭特別註明原頁數字沒渲染出來，所以不收 2.23。重算 87/39 = 2.23，計算正確，碼長和次數也都有 raw 依據，所以不算錯誤。但投影片上和其他兩個來源數字並列、沒有標示，建議加註「依來源碼長自行計算」。 | 建議 | shannon-fano#C13；raw/04 檔頭註記與 #Comparison with Huffman coding | 逐頁稿 |
| 12 | 「傳 0.538 就夠了」[card:arithmetic-coding#C7] | 「只要傳足以落在最終區間內的位數就夠」是 C8 的內容（raw/06 #Decoding example），C7 只有「0.538 解出三個符號」。建議補引 C8，也順便補上「解碼端必須用同一個模型」。 | 建議 | arithmetic-coding#C7、C8；raw/06#Decoding example | 逐頁稿 |
| 06 | 💡 反例：A=`0`、B=`01`，收到 `01` 就分不清是 B 還是 A＋下一個碼的開頭 | 💡 行裡藏了一個不太準的事實主張：如果碼表只有 {0, 01}，就沒有碼以 1 開頭，所以完整收到的 `01` 只能是 B，它其實能唯一解碼，只是要往後多看一位。建議換成真正有歧義的反例，例如 A=`0`、B=`01`、C=`10`：`010` 可以是 A C，也可以是 B A。（這點是依常識判斷，raw 沒談反例） | 建議 | prefix-code#C1；raw/05#Terminology | 逐頁稿 |
| 05 | 「Shannon 的信源編碼定理，訂出了資料壓縮在統計上的極限。」 | 跟來源相符。不過 raw/03 #Introduction 說明定理適用於 i.i.d. 來源（source-coding-theorem#C2），本頁和第 14 頁把它講成一般性結論，沒有提適用條件。raw/02 也有一般化的說法，所以不算錯，只是建議加半句條件。 | 建議 | source-coding-theorem#C1、C2；raw/03#Introduction；raw/02#Data compression | 逐頁稿 |

其他經比對確認忠實的頁：01、02（純導覽 💡）、03、04、07、08（年代矛盾已依 C6 並列）、09（建樹、產碼、解碼三步驟與 a–e 碼字都符合 raw/05）、12 其餘句子、13 的「編碼單位」「專利」兩列、14。

## 覆蓋率與教學性
| 項目 | 結果 | 說明 |
|---|---|---|
| 學習目標 1：為什麼常見的東西用短碼就能壓縮？極限在哪？ | 部分達成 | 「極限＝熵」在第 4、5、14 頁講清楚了。但「常見符號給短碼→平均碼長變短」這個核心機制，前 13 頁都沒明講，第 14 頁回顧才第一次出現（huffman-coding#C1）。卡片裡現成的 entropy#C10（A–D 四字母：機率相等要 2 bits，機率不均時用長短不一的碼，平均更少）正是這題的答案，卻沒用到。建議放進第 4 或第 5 頁。 |
| 學習目標 2：Huffman 怎麼建樹、怎麼解碼？ | 大致達成 | 第 9 頁三步驟加互動建樹，涵蓋建樹與產碼。解碼只有一句，沒有實際解一串 bit 的例子，也漏了「解碼端需要同一棵樹或頻率表」（huffman-coding#C9 後半）。建議用 a–e 的碼字示範解一段 bit 串。 |
| 學習目標 3：算術編碼跟 Huffman 差在哪？為什麼 Huffman 還是到處都是？ | 部分達成 | 「差在哪」由第 11、12、13 頁回答，完整。「為什麼 Huffman 還到處都是」只靠第 13 頁最後一句，而這句的因果目前沒有來源（見忠實度表）。改用 arithmetic-coding#C12 的專利史實作答，就能補齊。 |
| 未解釋術語：bit／位元 | 建議補 | 封面就開始用，但全篇沒定義。entropy#C3（底數 2 的單位是 bit）可以用，或用一句「一個 0 或 1」帶過。 |
| 未解釋術語：碼字、平均碼長、最佳 | 建議補 | 第 6 頁用「碼字」定義前綴碼，但「碼字」本身沒定義。「平均碼長」第 6、7、10 頁都在用，但沒說它是依機率加權的平均；prefix-code#C3 的加權路徑長度可以拿來解釋。「最佳」（第 7、8 頁）也沒說是指「平均碼長最短」。 |
| 未解釋術語：節點、葉子、根、權重 | 建議補 | 第 9 頁直接使用。卡片 C7 有「權重＝出現頻率」，逐頁稿把這句刪了，建議補回，並用一句話說明樹的各部位名稱。 |
| 未解釋術語：冗餘、隨機結果、二進位碼、模型、半開區間 [0, 0.6) | 建議補 | 依序出現在第 3、4、8、12 頁。零基礎讀者可能看不懂 [a, b) 的記號，也不知道「模型」是什麼；arithmetic-coding#C4 可以補「模型＝預測每個符號機率的東西」。 |
| 未解釋術語：DEFLATE、gzip、JPEG、MP3 | 輕微 | 第 13 頁只列名稱。建議加上「壓縮檔、圖片、音樂」這類白話對應。 |
| 第 7 與第 10 頁銜接 | 建議補 | 第 7 頁把 Shannon–Fano 當成一種方法介紹，第 10 頁卻分成「Shannon 2.62／Fano 2.28」兩個數字。讀者會不知道兩者差在哪。建議第 7 頁補引 shannon-fano#C2（其實是兩個同名演算法）。 |
| 第 10 頁兩個例子並列 | 建議補 | 小寫 a–e（有熵 2.205）和大寫 A–E（沒有熵值）是不同資料，頁標題卻是「離熵多近」，容易混淆。建議明確標出「例一／例二」。 |
| 第 12 頁「為什麼這樣能壓縮」 | 建議補 | 只示範切區間，沒說明這樣為什麼比較省 bit。可補 arithmetic-coding#C3（逼近熵，訊息越長越明顯），讓第 11 頁埋的伏筆有收尾。 |

## 結論
錯誤 3 項、建議 6 項（另有教學性建議若干，見上表）；是否可進入渲染：否

需修正的 3 項錯誤都在第 13 頁：
1. 「較慢（需維護區間與精度）」的因果沒有來源 → 退回 wiki。
2. 應用欄把「前綴碼」寫成「Huffman」 → 退回 wiki。
3. 「所以仍然到處都是」是推論，沒有來源 → 退回逐頁稿，改引 arithmetic-coding#C12。

建議同時補上 entropy#C10，讓學習目標 1 在正文就有答案。
