# 無失真 vs 失真壓縮（Lossless vs Lossy）

💡 比喻：無失真像把衣服真空壓縮，打開後一模一樣；失真像把照片縮小，看起來差不多但細節回不來。

## 無失真壓縮（lossless）
- 原理是移除「統計上的冗餘」，因此原始資料可以完整還原。[src:raw/01-data-compression.md#Lossless]
- 原文：「No information is lost in lossless compression.」[src:raw/01-data-compression.md#Lossless]
- 最簡單的例子是連續長度編碼（run-length encoding）：把一長串相同顏色的像素，改記成「個數＋顏色」。[src:raw/01-data-compression.md#Lossless]
- 最常用的方法之一是 Lempel–Ziv 家族，包括 LZW 和 DEFLATE。[src:raw/01-data-compression.md#Lossless]

## 失真壓縮（lossy）
- 丟掉被判斷為不必要或較不重要的資訊，用一些保真度換取更小的檔案。[src:raw/01-data-compression.md#Lossy]
- 例：人眼對亮度比對顏色敏感，所以 JPEG 會捨去觀看者不易察覺的細節。[src:raw/01-data-compression.md#Lossy]

💡 本 wiki 的主角 Huffman 與算術編碼都屬於「無失真」。

相關：[[data-compression]]
