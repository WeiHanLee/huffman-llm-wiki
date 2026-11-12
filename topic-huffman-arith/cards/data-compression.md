# 證據卡：資料壓縮（Data compression）
來源頁：wiki/data-compression.md（只抽此頁，不混其他來源）

- C1｜資料壓縮又稱為信源編碼（source coding），是用比原始表示法更少的位元來編碼資訊。[src:raw/01-data-compression.md#Lead]
- C2｜負責壓縮的叫編碼器（encoder），負責還原的叫解碼器（decoder）。[src:raw/01-data-compression.md#Lead]
- C3｜壓縮分成兩大類：無失真（lossless）與失真（lossy），差別見 [[lossless-vs-lossy]]。[src:raw/01-data-compression.md#Lead]
- C4｜熵編碼（entropy coding）起源於 1940s 的 Shannon–Fano 編碼，它是 [[huffman-coding]] 的基礎。[src:raw/01-data-compression.md#Theory]
- C5｜[[arithmetic-coding]]（算術編碼）是較現代的技術，壓縮效果可以比 Huffman 編碼更好，也適合統計特性會隨時間變化的「自適應模型」。[src:raw/01-data-compression.md#Theory]
- C6｜壓縮能壓到多小，極限由「熵」決定，見 [[entropy]]。[src:raw/02-entropy.md#Data compression]
