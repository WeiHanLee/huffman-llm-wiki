# 熵（Entropy）

💡 一句話：熵＝「平均有多意外」；越難猜的資料，熵越高，越難壓縮。

## 定義與直覺
- 隨機變數的熵，衡量其可能結果的平均不確定性（或資訊量）。[src:raw/02-entropy.md#Lead]
- 熵由 Claude Shannon 在 1948 年的論文提出，所以又稱 Shannon 熵。[src:raw/02-entropy.md#Lead]
- 對數的底決定單位：底 2 的單位是位元（bit）。[src:raw/02-entropy.md#Lead]
- 越可能發生的事帶來的資訊越少，越不可能的事帶來的資訊越多；例如「這張彩券不會中」幾乎沒告訴你什麼。[src:raw/02-entropy.md#Introduction]
- 每個事件的「意外程度」稱為自資訊（self-information），熵就是自資訊的期望值。[src:raw/02-entropy.md#Introduction]

## 例子：擲硬幣
- 公平硬幣（p = 1/2）最難猜，熵是 1 bit（one bit）。[src:raw/02-entropy.md#Example]
- 永遠出同一面的硬幣沒有不確定性，熵是零（zero）。[src:raw/02-entropy.md#Example]
- 擲骰子的熵比擲硬幣高，因為每個結果更不可能。[src:raw/02-entropy.md#Example]

## 和壓縮的關係
- 資訊理論可以算出傳達一則訊息「最少需要多少資訊」，這正是資料壓縮的核心。[src:raw/02-entropy.md#Data compression]
- 四個字母 A、B、C、D 機率相同時，每個字母需要兩個 bits（two bits）；機率不均時，用長短不一的碼就能平均更少。[src:raw/02-entropy.md#Data compression]
- 英文文字的熵約為每字元 0.6 到 1.3 bits，所以英文很好壓縮。[src:raw/02-entropy.md#Data compression]
- 熵是無失真壓縮的極限，這就是 [[source-coding-theorem]]。[src:raw/02-entropy.md#Data compression]

相關：[[data-compression]]、[[lossless-vs-lossy]]、[[source-coding-theorem]]
