# 資料壓縮（Data compression）

💡 一句話：用比原本更少的位元（bit）來表示同一份資訊。

## 定義
- 資料壓縮又稱為信源編碼（source coding），是用比原始表示法更少的位元來編碼資訊。[src:raw/01-data-compression.md#Lead]
- 負責壓縮的叫編碼器（encoder），負責還原的叫解碼器（decoder）。[src:raw/01-data-compression.md#Lead]
- 壓縮分成兩大類：無失真（lossless）與失真（lossy），差別見 [[lossless-vs-lossy]]。[src:raw/01-data-compression.md#Lead]

## 歷史脈絡
- 熵編碼（entropy coding）起源於 1940s 的 Shannon–Fano 編碼，它是 [[huffman-coding]] 的基礎。[src:raw/01-data-compression.md#Theory]
- 算術編碼（arithmetic coding）是較現代的技術，壓縮效果可以比 Huffman 編碼更好，也適合統計特性會隨時間變化的「自適應模型」。[src:raw/01-data-compression.md#Theory]

- 壓縮能壓到多小，極限由「熵」決定，見 [[entropy]]。[src:raw/02-entropy.md#Data compression]

相關：[[lossless-vs-lossy]]、[[entropy]]
