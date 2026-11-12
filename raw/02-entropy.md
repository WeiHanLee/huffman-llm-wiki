# Entropy (information theory)（Wikipedia）

- URL: https://en.wikipedia.org/wiki/Entropy_(information_theory)
- 擷取日期：2026-11-12
- 擷取方式：WebFetch 工具（重點摘要＋125 字元內短引文；引號內為原文）。

## Lead
"the entropy of a random variable quantifies the average level of uncertainty or information" associated with its possible outcomes. Entropy measures the expected amount of information needed to describe the variable's state, given how probability is spread across its possible states. The logarithm base sets the unit: base 2 gives bits, base e gives nats, and base 10 gives hartleys. Claude Shannon introduced the concept in his 1948 paper, which is why it is also called Shannon entropy.

## Introduction
"the \"informational value\" of a communicated message depends on the degree to which the content" is surprising. Likely events convey little information, while unlikely events convey a lot. A lottery ticket that will not win tells you almost nothing, but knowing a specific number will win is highly informative. Surprisal, or self-information, increases as an event's probability decreases, and entropy is the expected value of that surprisal.

## Example
"Consider a coin with probability p of landing on heads and probability 1 − p of landing on tails." A fair coin (p = 1/2) gives the maximum surprise and an entropy of one bit. A coin that always lands the same way has zero entropy, because there is no uncertainty. Biased coins fall between these extremes. A die roll has higher entropy than a coin toss, since each die outcome is less probable.

## Data compression
"Information theory is useful to calculate the smallest amount of information required to convey a message", which is central to data compression. A four-letter example (A, B, C, D): equal probabilities need two bits per letter, but skewed probabilities allow variable-length codes that average fewer bits. Shannon's source coding theorem sets entropy as the limit on lossless compression.
"English text has between 0.6 and 1.3 bits of entropy per character of the message." English is fairly predictable, so it compresses well. The PPM algorithm can reach about 1.5 bits per character on English text.
