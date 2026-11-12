# Huffman coding（Wikipedia）

- URL: https://en.wikipedia.org/wiki/Huffman_coding
- 擷取日期：2026-11-12
- 擷取方式：WebFetch 工具（重點摘要；不提供全文）。

## Lead
A Huffman code is an optimal prefix code used for lossless data compression. David A. Huffman developed the algorithm as an MIT Sc.D. student and published it in 1952. It assigns shorter bit strings to more frequent symbols. Huffman coding is optimal among methods that encode symbols one at a time, but arithmetic coding can achieve better compression when that is needed.

## History
In 1951, Huffman was a student in an information theory course taught by Robert M. Fano, who offered students a choice between a term paper and a final exam. Huffman chose the paper, on finding the most efficient binary code. He struggled to prove that any code was optimal until he developed the idea of building a frequency-sorted binary tree, which he then showed was most efficient. Unlike the top-down Shannon–Fano approach, building the tree bottom-up guarantees optimality.

## Terminology
- Prefix code: no codeword is a prefix of another, so decoding is unambiguous. "Huffman code" is often used loosely for any prefix code, even ones not built by Huffman's algorithm.
- Weighted path length: the sum of each symbol's weight times its codeword length. Minimizing it minimizes the expected codeword length.
- Entropy (Shannon): the theoretical lower limit on average bits per symbol.

## Example
Five-symbol example (a–e):

| Symbol | Weight | Codeword | Length |
|---|---|---|---|
| a | 0.10 | 010 | 3 |
| b | 0.15 | 011 | 3 |
| c | 0.30 | 11 | 2 |
| d | 0.16 | 00 | 2 |
| e | 0.29 | 10 | 2 |

The weighted average length is 2.25 bits per symbol, compared with an entropy of about 2.205 bits, so the code is very close to the theoretical limit.

## Basic technique
Building the tree: each symbol starts as a leaf node weighted by its frequency. Repeatedly, the two lowest-weight nodes are merged under a new internal node whose weight is their sum, until one root node remains. A priority queue does this in O(n log n) time.
Generating codes: traverse the tree from the root, labeling left edges 0 and right edges 1. A symbol's code is the sequence of labels on the path to its leaf.
Decompression: read bits and walk the tree until reaching a leaf, which yields a symbol. The decoder needs the tree or frequency table, which can be preset or sent as a prefix to the data.

## Optimality
Huffman coding is optimal among symbol-by-symbol codes when symbol probabilities are known and symbols are independent. It is not optimal when symbols are combined into blocks, when probabilities are unknown, or when symbols are not independent and identically distributed. It is most efficient when symbol probabilities are powers of 1/2. For small alphabets, its inefficiency can be significant. Blocking symbols can improve compression but grows exponentially in cost. Arithmetic coding can match the true probabilities more closely, but Huffman coding is faster and was historically free of patent issues.

## Applications
Prefix codes are widely used as a back-end stage in compression, for example in DEFLATE (used in PKZIP and gzip), JPEG, and MP3. Fax machines use a modified Huffman scheme. Variants include adaptive Huffman coding, which updates the tree as data arrives.
