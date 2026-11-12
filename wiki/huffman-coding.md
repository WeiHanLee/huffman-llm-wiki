# Huffman 編碼（Huffman coding）

💡 一句話：「由下往上合併」——每次把最不常出現的兩個符號綁在一起，綁到剩一棵樹；常出現的符號離樹根近，碼就短。

## 是什麼
- Huffman 碼是一種用於無失真壓縮的「最佳」[[prefix-code]]：越常出現的符號，給越短的位元串。[src:raw/05-huffman-coding.md#Lead]
- 由 David A. Huffman 在 MIT 讀博士（Sc.D.）時提出，1952 年發表。[src:raw/05-huffman-coding.md#Lead]

## 故事：一份期末報告
- 1951 年 Huffman 修 Robert M. Fano 的資訊理論課，老師讓學生在「期末報告」和「期末考」二選一，他選了報告，題目是找出最有效率的二進位碼。[src:raw/05-huffman-coding.md#History]
- 他原本一直證明不出哪套碼最好，直到想到「依頻率排序建二元樹」的方法，並證明它最有效率。[src:raw/05-huffman-coding.md#History]
- 和由上而下的 [[shannon-fano]] 不同，由下而上建樹保證最佳。[src:raw/05-huffman-coding.md#History]
- ⚠ 矛盾：Huffman 編碼的年代，Wikipedia〈Huffman coding〉說 1951 年修課時提出、1952 年發表 [src:raw/05-huffman-coding.md#History] [src:raw/05-huffman-coding.md#Lead]；〈Data compression〉則寫「developed in 1950」[src:raw/01-data-compression.md#Theory]。

## 演算法三步驟
- ① 建樹：每個符號先是一片葉子，權重＝出現頻率；反覆把「權重最小的兩個節點」合併成一個新節點（權重相加），直到只剩一個根。[src:raw/05-huffman-coding.md#Basic technique]
- ② 產生碼字：從根往下走，左邊標 0、右邊標 1；走到某片葉子的路徑就是那個符號的碼。[src:raw/05-huffman-coding.md#Basic technique]
- ③ 解碼：一個一個讀 bit、沿著樹往下走，走到葉子就輸出一個符號；所以解碼端必須拿到同一棵樹或頻率表。[src:raw/05-huffman-coding.md#Basic technique]

## 例子：五個符號 a–e
| 符號 | 權重 | 碼字 | 碼長 [src:raw/05-huffman-coding.md#Example] |
|---|---|---|---|
| a | 0.10 | `010` | 3 [src:raw/05-huffman-coding.md#Example] |
| b | 0.15 | `011` | 3 [src:raw/05-huffman-coding.md#Example] |
| c | 0.30 | `11` | 2 [src:raw/05-huffman-coding.md#Example] |
| d | 0.16 | `00` | 2 [src:raw/05-huffman-coding.md#Example] |
| e | 0.29 | `10` | 2 [src:raw/05-huffman-coding.md#Example] |

- 平均碼長 2.25 bits／符號，熵約 2.205 bits，已非常接近理論極限。[src:raw/05-huffman-coding.md#Example]

## 什麼時候最好、什麼時候不夠好
- 在「機率已知、符號彼此獨立、一次編一個符號」的條件下，Huffman 是最佳的。[src:raw/05-huffman-coding.md#Optimality]
- 機率剛好是 1/2 的次方時效率最高；符號種類很少時，浪費可能很明顯。[src:raw/05-huffman-coding.md#Optimality]
- 把多個符號綁成一塊（blocking）可以改善，但成本會指數成長。[src:raw/05-huffman-coding.md#Optimality]
- 算術編碼能更貼近真實機率，但 Huffman 比較快，歷史上也沒有專利問題。[src:raw/05-huffman-coding.md#Optimality]

## 實際應用
- 前綴碼常被當作壓縮流程的最後一段，例如 DEFLATE（PKZIP、gzip 使用）、JPEG、MP3。[src:raw/05-huffman-coding.md#Applications]
- 傳真機使用修改版的 Huffman 編碼。[src:raw/05-huffman-coding.md#Applications]

相關：[[prefix-code]]、[[shannon-fano]]、[[entropy]]、[[source-coding-theorem]]
