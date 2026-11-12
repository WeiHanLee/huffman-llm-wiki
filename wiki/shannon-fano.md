# Shannon–Fano 編碼（Shannon–Fano coding）

💡 一句話：「由上往下對半切」——把符號依機率排好，切成兩堆差不多重的，左邊給 0、右邊給 1，一直切到每堆只剩一個。

## 是什麼
- 以 Claude Shannon 和 Robert Fano 命名，用符號的機率建出一套前綴碼（prefix code）。[src:raw/04-shannon-fano.md#Introduction]
- 其實有兩種不同演算法共用這個名字：Shannon 的方法（1948）和 Fano 的方法（1949）。[src:raw/04-shannon-fano.md#Naming]
- 它們產生的碼「不一定最好」：平均碼長與最佳值相差在一個 bit 以內（within one bit），但不保證最短；Huffman 編碼才保證。[src:raw/04-shannon-fano.md#Introduction]

## Fano 的做法（由上而下）
- 把符號依機率由大到小排序，切成兩組、讓兩組總機率盡量接近；第一組加「0」、第二組加「1」，再對每組重複，直到每個符號單獨一組。[src:raw/04-shannon-fano.md#Fano's code]

## 同一個例子：五個符號 A–E
| 符號 | 次數（共 39） [src:raw/04-shannon-fano.md#Fano's code] | 機率 | Fano 碼長 | Huffman 碼長 |
|---|---|---|---|---|
| A | 15 | 0.385 | 2 | 1 [src:raw/04-shannon-fano.md#Fano's code] [src:raw/04-shannon-fano.md#Comparison with Huffman coding] |
| B | 7 | 0.179 | 2 | 3 [src:raw/04-shannon-fano.md#Fano's code] [src:raw/04-shannon-fano.md#Comparison with Huffman coding] |
| C | 6 | 0.154 | 2 | 3 [src:raw/04-shannon-fano.md#Fano's code] [src:raw/04-shannon-fano.md#Comparison with Huffman coding] |
| D | 6 | 0.154 | 3 | 3 [src:raw/04-shannon-fano.md#Fano's code] [src:raw/04-shannon-fano.md#Comparison with Huffman coding] |
| E | 5 | 0.128 | 3 | 3 [src:raw/04-shannon-fano.md#Fano's code] [src:raw/04-shannon-fano.md#Comparison with Huffman coding] |

- 第一刀切在 B 和 C 之間，兩邊總次數是 22 和 17。[src:raw/04-shannon-fano.md#Fano's code]
- Fano 平均碼長約 2.28 bits；Shannon 的方法是 2.62 bits。[src:raw/04-shannon-fano.md#Comparison with Huffman coding]
- Huffman 平均碼長約 2.23 bits，三者中最短。[calc:tools/calc.py sf_huffman_avg＝(15×1+24×3)/39，來源原數字未渲染]

相關：[[entropy]]、[[source-coding-theorem]]
