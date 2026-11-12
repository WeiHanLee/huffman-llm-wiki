# 算術編碼（Arithmetic coding）

💡 一句話：不幫每個符號各發一個碼，而是把「整則訊息」縮成 0 到 1 之間的一個小數。

## 是什麼
- 算術編碼是一種用於無失真壓縮的熵編碼方法。[src:raw/06-arithmetic-coding.md#Lead]
- 它不是把每個符號換成各自的碼，而是把整則訊息編成一個小數 q，0 ≤ q < 1。[src:raw/06-arithmetic-coding.md#Lead]
- 最好的成績由來源的熵決定，而算術編碼能很接近這個極限，訊息越長越明顯。[src:raw/06-arithmetic-coding.md#Lead]

## 核心想法：不斷切區間
- 先要有一個「模型」預測每個符號的機率；編碼器從區間 [0, 1) 開始，依機率切成小段，留下實際符號對應的那一段，再重複。[src:raw/06-arithmetic-coding.md#Defining a model]
- 範例模型：NEUTRAL 60%、POSITIVE 20%、NEGATIVE 10%、END-OF-DATA 10%；END-OF-DATA 表示訊息結束。[src:raw/06-arithmetic-coding.md#Defining a model]
- 編碼「NEUTRAL → NEGATIVE → END-OF-DATA」時，區間依序縮成 [0, 0.6) → [0.48, 0.54) → [0.534, 0.54)。[calc:tools/calc.py ac_step1~3，以來源的 60/20/10/10 模型逐步切分] [src:raw/06-arithmetic-coding.md#Defining a model]
- 來源的解碼範例：小數 0.538 依序解出 NEUTRAL、NEGATIVE、END-OF-DATA。[src:raw/06-arithmetic-coding.md#Decoding example]
- 只要傳「足夠落在最終區間內」的位數就好；解碼端必須使用和編碼端相同的模型。[src:raw/06-arithmetic-coding.md#Decoding example]

💡 直覺：常見的符號佔的區間寬，切完區間縮得少，花的位數就少；罕見符號讓區間縮很多，花的位數就多。

## 實作上的眉角
- 真實的編碼器沒辦法記住無限精度的小數，所以用固定精度並把邊界四捨五入。[src:raw/06-arithmetic-coding.md#Precision and renormalization]
- 重新正規化（renormalization）：當區間上下界的開頭幾位數相同時，就先把那幾位輸出、把區間放大，才能一直編下去。[src:raw/06-arithmetic-coding.md#Precision and renormalization]

## 歷史
- 基本演算法由 IBM 的 Jorma Rissanen 和 Stanford 博士生 Richard Pasco 各自獨立提出，兩人都在 1976 年五月（May 1976）發表。[src:raw/06-arithmetic-coding.md#History and patents]
- 許多相關技術曾被申請專利，現在大多已過期；專利顧慮曾讓 bzip2 放棄算術編碼，JPEG 實作也多半改用 Huffman。[src:raw/06-arithmetic-coding.md#History and patents]

相關：[[huffman-coding]]、[[entropy]]、[[huffman-vs-arithmetic]]
