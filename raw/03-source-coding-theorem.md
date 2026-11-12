# Shannon's source coding theorem（Wikipedia）

- URL: https://en.wikipedia.org/wiki/Shannon%27s_source_coding_theorem
- 擷取日期：2026-11-12
- 擷取方式：WebFetch 工具（重點摘要＋125 字元內短引文；引號內為原文）。

## Introduction
Shannon's source coding theorem, also called the noiseless coding theorem, sets "the statistical limits to possible data compression." It applies to data from a source of independent, identically distributed (i.i.d.) random variables and gives operational meaning to Shannon entropy. Compressing such data below its entropy rate almost certainly loses information, while rates arbitrarily close to the entropy are achievable with negligible loss. For sources with more complex dependencies, Kolmogorov complexity is a better tool for describing compression limits.

## Statements
Source coding (informal): N i.i.d. random variables, each with entropy H(X), "can be compressed into more than N H(X)" bits with negligible risk of information loss as N grows; compressing them into fewer bits almost certainly loses information.
Symbol codes (informal): the theorem "places an upper and a lower bound on the minimal possible expected length of codewords", as a function of the entropy of the input and the size of the target alphabet.
