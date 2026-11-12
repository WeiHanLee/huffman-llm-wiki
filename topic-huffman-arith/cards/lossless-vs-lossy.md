# 證據卡：無失真 vs 失真壓縮（Lossless vs Lossy）
來源頁：wiki/lossless-vs-lossy.md（只抽此頁，不混其他來源）

- C1｜原理是移除「統計上的冗餘」，因此原始資料可以完整還原。[src:raw/01-data-compression.md#Lossless]
- C2｜原文：「No information is lost in lossless compression.」[src:raw/01-data-compression.md#Lossless]
- C3｜最簡單的例子是連續長度編碼（run-length encoding）：把一長串相同顏色的像素，改記成「個數＋顏色」。[src:raw/01-data-compression.md#Lossless]
- C4｜最常用的方法之一是 Lempel–Ziv 家族，包括 LZW 和 DEFLATE。[src:raw/01-data-compression.md#Lossless]
- C5｜丟掉被判斷為不必要或較不重要的資訊，用一些保真度換取更小的檔案。[src:raw/01-data-compression.md#Lossy]
- C6｜例：人眼對亮度比對顏色敏感，所以 JPEG 會捨去觀看者不易察覺的細節。[src:raw/01-data-compression.md#Lossy]
- C7｜本 wiki 的主角 Huffman 與算術編碼都用於無失真壓縮。[src:raw/05-huffman-coding.md#Lead] [src:raw/06-arithmetic-coding.md#Lead]
