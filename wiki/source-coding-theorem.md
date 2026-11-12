# 信源編碼定理（Shannon's source coding theorem）

💡 一句話：熵是一道「地板」——無失真壓縮可以很接近它，但壓到它下面一定會掉資訊。

## 內容
- 又稱無雜訊編碼定理（noiseless coding theorem），它訂出了資料壓縮在統計上的極限。[src:raw/03-source-coding-theorem.md#Introduction]
- 適用對象：每個符號彼此獨立、同分布（i.i.d.）的資料來源。[src:raw/03-source-coding-theorem.md#Introduction]
- 壓到低於熵，幾乎一定會遺失資訊；但可以做到「任意接近熵」而幾乎不遺失。[src:raw/03-source-coding-theorem.md#Introduction]
- 白話版：N 個符號、每個的熵是 H，只要給「多於 N×H 個 bits」就能在 N 很大時幾乎無損壓縮。[src:raw/03-source-coding-theorem.md#Statements]
- 對「一個符號換一個碼字」的符號碼（symbol code），定理同時給出平均碼長的上界與下界。[src:raw/03-source-coding-theorem.md#Statements]

## 為什麼重要
- 這個定理讓 [[entropy]] 從抽象的「不確定性」變成有實際意義的「最少要用幾個 bits」。[src:raw/03-source-coding-theorem.md#Introduction]
💡 後面介紹的編碼方法，都可以拿「離熵多近」來評分。

相關：[[entropy]]、[[data-compression]]
