# Data compression（Wikipedia）

- URL: https://en.wikipedia.org/wiki/Data_compression
- 擷取日期：2026-11-12
- 擷取方式：WebFetch 工具。該工具因著作權限制不提供全文，回傳「重點摘要＋125 字元內短引文」。引號內為原文短引，其餘為擷取工具的英文摘要。

## Lead
Data compression (also called source coding or bit-rate reduction) encodes information using fewer bits than the original representation. Compression is either lossy or lossless. The device that compresses is an encoder, and the one that reverses the process is a decoder.

## Lossless
Lossless methods remove statistical redundancy so that the original data can be fully restored. "No information is lost in lossless compression." Run-length encoding, which replaces long runs of identical pixels with a count and a color, is a simple example. Lempel–Ziv methods, including LZW and DEFLATE, are among the most widely used. The strongest modern lossless compressors rely on probabilistic models, and arithmetic coding can combine with those models to outperform Huffman coding.
Quote: "It can achieve superior compression compared to other techniques, such as the better-known Huffman algorithm."

## Lossy
Lossy compression discards information judged unnecessary or less important. It trades some fidelity for smaller size, and the right balance depends on how people perceive the data. For example, human eyes are more sensitive to brightness than to color, so image formats such as JPEG round off detail that viewers are unlikely to notice.

## Theory
Entropy coding "originated in the 1940s with the introduction of Shannon–Fano coding", which was "the basis for Huffman coding which was developed in 1950." Arithmetic coding is a more modern technique that uses a finite-state machine to turn a series of input symbols into a bit string. It can compress better than Huffman coding and works well with adaptive models whose statistics change over time.
