# 前綴碼（Prefix code）

💡 一句話：沒有任何一個碼字是另一個碼字的「開頭」，所以一串 0/1 從頭讀下去，永遠只有一種切法。

## 定義
- 前綴碼：沒有任何碼字（codeword）是另一個碼字的前綴，所以解碼不會有歧義。[src:raw/05-huffman-coding.md#Terminology]
- 「Huffman code」這個詞常被寬鬆地拿來指任何前綴碼，即使不是用 Huffman 演算法做出來的。[src:raw/05-huffman-coding.md#Terminology]

💡 例子：若 A=`0`、B=`10`、C=`11`，收到 `01011` 只能切成 0｜10｜11 → A B C。反例：若 A=`0`、B=`01`，收到 `01` 就不知道是「B」還是「A＋下一個碼的開頭」。

## 怎麼評分一套前綴碼
- 加權路徑長度（weighted path length）＝每個符號的權重 × 碼長，再全部加總；把它壓到最小，就等於把平均碼長壓到最小。[src:raw/05-huffman-coding.md#Terminology]
- 平均碼長的理論下限就是 [[entropy]]。[src:raw/05-huffman-coding.md#Terminology]

相關：[[shannon-fano]]、[[huffman-coding]]、[[entropy]]
