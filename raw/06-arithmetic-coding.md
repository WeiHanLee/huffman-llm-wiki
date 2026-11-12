# Arithmetic coding（Wikipedia）

- URL: https://en.wikipedia.org/wiki/Arithmetic_coding
- 擷取日期：2026-11-12
- 擷取方式：WebFetch 工具（重點摘要；不提供全文）。

## Lead
Arithmetic coding is an entropy coding method for lossless compression. Instead of replacing each symbol with its own code, it encodes an entire message as a single number, a fraction q with 0 ≤ q < 1. Frequent symbols take fewer bits and rare ones take more, so the total size drops. The best possible result is set by the source's entropy, and arithmetic coding gets close to that limit, especially for long messages.

## Equal probabilities
If each of three symbols (A, B, C) is equally likely, fixed-width binary codes need 2 bits per symbol, which wastes one bit pattern. Treating the sequence as a base-3 number and then converting it to binary uses fewer bits overall. The article's example encodes "ABBCAB" in 10 bits instead of 12. When all symbols are equally likely, no compression is possible beyond this.

## Defining a model
A model predicts how likely each symbol is. The encoder starts with the interval [0, 1) and splits it into sub-intervals sized by those probabilities. It then keeps the sub-interval matching each actual symbol and repeats. Example model with four symbols: NEUTRAL (60%), POSITIVE (20%), NEGATIVE (10%), and END-OF-DATA (10%). The END-OF-DATA symbol marks where the stream stops.

## Decoding example
The fraction 0.538 is decoded by repeatedly checking which sub-interval contains it. This recovers NEUTRAL, then NEGATIVE, then END-OF-DATA, which ends decoding. Only enough digits to land inside the final interval need to be transmitted. The decoder must use the same model as the encoder.

## Precision and renormalization
Real coders cannot track exact fractions, so they work at fixed precision and round interval boundaries. Renormalization handles the limit on precision: when the current range shares leading digits, those digits are emitted and the range is shifted and widened. This lets the coder keep encoding long messages.

## Huffman coding
Huffman coding gives each symbol a whole-number bit length, which limits its efficiency. For a binary source with probabilities 0.95 and 0.05, plain Huffman coding cannot compress at all, since each symbol still costs one bit. Grouping symbols into blocks improves this, and Huffman coding reaches entropy only when probabilities are powers of two. However, the blocks grow very large to get close to entropy. Arithmetic coding approaches entropy without this cost.

## History and patents
Jorma Rissanen at IBM Research and Richard Pasco, a Stanford PhD student, independently developed the basic algorithms. Both published in May 1976. Many arithmetic coding techniques were patented over the years; those patents have mostly expired. Patent concerns led bzip2 to drop arithmetic coding, and JPEG implementations mostly use Huffman coding instead.
