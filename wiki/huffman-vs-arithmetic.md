# Huffman vs 算術編碼（比較頁）

💡 一句話：Huffman 每個符號只能用「整數個」bit；算術編碼等於可以用「零點幾個」bit，所以更貼近熵。

## 關鍵差別：整數位元的限制
- Huffman 給每個符號的碼長都是整數個 bit，這限制了它的效率。[src:raw/06-arithmetic-coding.md#Huffman coding]
- 極端例子：兩個符號、機率 0.95 和 0.05 時，單純的 Huffman 完全壓不了，每個符號還是要一個 bit（one bit）。[src:raw/06-arithmetic-coding.md#Huffman coding]
- 只有機率剛好是二的次方（powers of two）時，Huffman 才會達到熵。[src:raw/06-arithmetic-coding.md#Huffman coding]
- 把符號綁成一塊可以改善，但要接近熵，塊會變得非常大；算術編碼不需要付這個代價就能逼近熵。[src:raw/06-arithmetic-coding.md#Huffman coding]

## 對照表
| 面向 | Huffman 編碼 | 算術編碼 |
|---|---|---|
| 編碼單位 | 一個符號一個碼字 [src:raw/05-huffman-coding.md#Optimality] | 整則訊息一個小數 [src:raw/06-arithmetic-coding.md#Lead] |
| 壓縮效果 | 符號逐一編碼中最佳，但受整數碼長限制 [src:raw/05-huffman-coding.md#Optimality] [src:raw/06-arithmetic-coding.md#Huffman coding] | 更接近熵，長訊息尤其明顯 [src:raw/06-arithmetic-coding.md#Lead] |
| 速度 | 較快 [src:raw/05-huffman-coding.md#Optimality] | 來源只說 Huffman 較快，未說明原因 [src:raw/05-huffman-coding.md#Optimality] |
| 專利 | 歷史上沒有專利問題 [src:raw/05-huffman-coding.md#Optimality] | 曾有許多專利，現多已過期 [src:raw/06-arithmetic-coding.md#History and patents] |
| 常見應用 | 前綴碼常用於 DEFLATE（gzip）、JPEG、MP3；JPEG 實作多用 Huffman [src:raw/05-huffman-coding.md#Applications] [src:raw/06-arithmetic-coding.md#History and patents] | 搭配機率模型的強力壓縮器 [src:raw/01-data-compression.md#Lossless] |

## 兩個來源的一致結論
- 〈Data compression〉：算術編碼能比知名的 Huffman 演算法壓得更好。[src:raw/01-data-compression.md#Lossless]
- 〈Huffman coding〉：Huffman 在「一次編一個符號」的方法中最佳，但需要時算術編碼能壓得更好。[src:raw/05-huffman-coding.md#Lead]

💡 那為什麼 Huffman 還到處都是？因為快、簡單、沒有專利包袱——工程上「夠好又便宜」常常贏過「最好但貴」。

相關：[[huffman-coding]]、[[arithmetic-coding]]、[[entropy]]、[[source-coding-theorem]]
