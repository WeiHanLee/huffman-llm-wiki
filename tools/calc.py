#!/usr/bin/env python3
"""重算 wiki 中標 [calc:] 的數字，寫入 tools/calc_results.json 供 lint L5 比對。
每個數字都只用 raw/ 中出現的來源數字計算。"""
import json
import math
from pathlib import Path

results = {}

# raw/04-shannon-fano.md#Fano's code：counts 15,7,6,6,5（共 39）
counts = {"A": 15, "B": 7, "C": 6, "D": 6, "E": 5}
total = sum(counts.values())
assert total == 39
# raw/04#Comparison with Huffman coding：Huffman 碼長 A=1、B–E=3
huff_len = {"A": 1, "B": 3, "C": 3, "D": 3, "E": 3}
# raw/04#Fano's code：Fano 碼長 A,B,C=2、D,E=3
fano_len = {"A": 2, "B": 2, "C": 2, "D": 3, "E": 3}

huff_avg = sum(counts[s] * huff_len[s] for s in counts) / total
fano_avg = sum(counts[s] * fano_len[s] for s in counts) / total
entropy = -sum(c / total * math.log2(c / total) for c in counts.values())

results["sf_huffman_avg"] = round(huff_avg, 2)       # 87/39
results["sf_fano_avg_check"] = round(fano_avg, 2)    # 應等於來源的 2.28
results["sf_entropy"] = round(entropy, 2)

assert results["sf_fano_avg_check"] == 2.28, "Fano 平均碼長和來源 2.28 不符"

# raw/06-arithmetic-coding.md#Defining a model：NEUTRAL 60%、POSITIVE 20%、NEGATIVE 10%、END-OF-DATA 10%
# raw/06#Decoding example：0.538 解出 NEUTRAL → NEGATIVE → END-OF-DATA
model = [("NEUTRAL", 0.6), ("POSITIVE", 0.2), ("NEGATIVE", 0.1), ("END-OF-DATA", 0.1)]


def narrow(lo, hi, sym):
    start = lo
    for name, p in model:
        width = (hi - lo) * p
        if name == sym:
            return start, start + width
        start += width
    raise KeyError(sym)


lo, hi = 0.0, 1.0
steps = []
for sym in ["NEUTRAL", "NEGATIVE", "END-OF-DATA"]:
    lo, hi = narrow(lo, hi, sym)
    steps.append((round(lo, 3), round(hi, 3)))
results["ac_step1_lo"], results["ac_step1_hi"] = steps[0]
results["ac_step2_lo"], results["ac_step2_hi"] = steps[1]
results["ac_step3_lo"], results["ac_step3_hi"] = steps[2]
assert steps[2][0] <= 0.538 < steps[2][1], "0.538 不在最終區間內，和來源矛盾"

out = Path(__file__).with_name("calc_results.json")
out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
for k, v in results.items():
    print(f"{k} = {v}")
