# Shannon–Fano coding（Wikipedia）

- URL: https://en.wikipedia.org/wiki/Shannon%E2%80%93Fano_coding
- 擷取日期：2026-11-12
- 擷取方式：WebFetch 工具（重點摘要；不提供全文）。
- ⚠ 擷取註記：Huffman 比較段的平均碼長，原頁數字未成功渲染，擷取工具回報的「about 2.23 bits」是工具**自行計算**的，不是來源數字，故本檔不收錄該值。

## Introduction
Shannon–Fano coding is one of two related techniques, named after Claude Shannon and Robert Fano, for building a prefix code from a set of symbols and their probabilities. Both methods produce suboptimal prefix codes. Their expected codeword lengths are within one bit of the optimum, but they don't always reach the lowest possible length. Huffman coding does.

## Naming
Two different algorithms share the name. Shannon's method (1948) chooses codeword lengths from the symbol probabilities and then assigns codewords using cumulative probabilities. Fano's method (1949) recursively splits the sorted symbols into two groups of nearly equal probability and appends a bit at each split. Some authors call Shannon's method "Shannon coding" and Fano's method "Fano coding" to avoid the confusion.

## Fano's code
Fano's method sorts symbols from most to least probable and divides them into two sets with nearly equal total probability. The first set receives a "0" and the second a "1." Each set with more than one symbol is then split the same way until every symbol is alone, and its codeword is the sequence of bits recording its splits.
Example: Five symbols A–E have counts of 15, 7, 6, 6, and 5 out of 39 total observations, giving probabilities of 0.385, 0.179, 0.154, 0.154, and 0.128. The split between B and C gives totals of 22 and 17. Further splits produce codewords of 2 bits for A, B, and C and 3 bits for D and E. The resulting average length is about 2.28 bits.

## Comparison with Huffman coding
Huffman coding builds its tree from the leaves up by repeatedly merging the two least probable nodes, so it always yields an optimal prefix code for the given probabilities.
Example: Using the same five symbols, Huffman coding gives A a 1-bit codeword and B, C, D, and E 3-bit codewords. This beats Fano's 2.28 bits and Shannon's 2.62 bits.
