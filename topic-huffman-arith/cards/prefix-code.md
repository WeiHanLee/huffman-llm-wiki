# 證據卡：前綴碼（Prefix code）
來源頁：wiki/prefix-code.md（只抽此頁，不混其他來源）

- C1｜前綴碼：沒有任何碼字（codeword）是另一個碼字的前綴，所以解碼不會有歧義。[src:raw/05-huffman-coding.md#Terminology]
- C2｜「Huffman code」這個詞常被寬鬆地拿來指任何前綴碼，即使不是用 Huffman 演算法做出來的。[src:raw/05-huffman-coding.md#Terminology]
- C3｜加權路徑長度（weighted path length）＝每個符號的權重 × 碼長，再全部加總；把它壓到最小，就等於把平均碼長壓到最小。[src:raw/05-huffman-coding.md#Terminology]
- C4｜平均碼長的理論下限就是 [[entropy]]。[src:raw/05-huffman-coding.md#Terminology]
