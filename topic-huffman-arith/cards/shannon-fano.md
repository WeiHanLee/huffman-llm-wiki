# 證據卡：Shannon–Fano 編碼（Shannon–Fano coding）
來源頁：wiki/shannon-fano.md（只抽此頁，不混其他來源）

- C1｜以 Claude Shannon 和 Robert Fano 命名，用符號的機率建出一套前綴碼（prefix code）。[src:raw/04-shannon-fano.md#Introduction]
- C2｜其實有兩種不同演算法共用這個名字：Shannon 的方法（1948）和 Fano 的方法（1949）。[src:raw/04-shannon-fano.md#Naming]
- C3｜它們產生的碼「不一定最好」：平均碼長與最佳值相差在一個 bit 以內（within one bit），但不保證最短；Huffman 編碼才保證。[src:raw/04-shannon-fano.md#Introduction]
- C4｜把符號依機率由大到小排序，切成兩組、讓兩組總機率盡量接近；第一組加「0」、第二組加「1」，再對每組重複，直到每個符號單獨一組。[src:raw/04-shannon-fano.md#Fano's code]
- C5｜| 符號 | 次數（共 39） [src:raw/04-shannon-fano.md#Fano's code] | 機率 | Fano 碼長 | Huffman 碼長 |
- C6｜| A | 15 | 0.385 | 2 | 1 [src:raw/04-shannon-fano.md#Fano's code] [src:raw/04-shannon-fano.md#Comparison with Huffman coding] |
- C7｜| B | 7 | 0.179 | 2 | 3 [src:raw/04-shannon-fano.md#Fano's code] [src:raw/04-shannon-fano.md#Comparison with Huffman coding] |
- C8｜| C | 6 | 0.154 | 2 | 3 [src:raw/04-shannon-fano.md#Fano's code] [src:raw/04-shannon-fano.md#Comparison with Huffman coding] |
- C9｜| D | 6 | 0.154 | 3 | 3 [src:raw/04-shannon-fano.md#Fano's code] [src:raw/04-shannon-fano.md#Comparison with Huffman coding] |
- C10｜| E | 5 | 0.128 | 3 | 3 [src:raw/04-shannon-fano.md#Fano's code] [src:raw/04-shannon-fano.md#Comparison with Huffman coding] |
- C11｜第一刀切在 B 和 C 之間，兩邊總次數是 22 和 17。[src:raw/04-shannon-fano.md#Fano's code]
- C12｜Fano 平均碼長約 2.28 bits；Shannon 的方法是 2.62 bits。[src:raw/04-shannon-fano.md#Comparison with Huffman coding]
- C13｜Huffman 平均碼長約 2.23 bits，三者中最短。[calc:tools/calc.py sf_huffman_avg＝(15×1+24×3)/39，來源原數字未渲染]
