# 證據卡：信源編碼定理（Shannon's source coding theorem）
來源頁：wiki/source-coding-theorem.md（只抽此頁，不混其他來源）

- C1｜又稱無雜訊編碼定理（noiseless coding theorem），它訂出了資料壓縮在統計上的極限。[src:raw/03-source-coding-theorem.md#Introduction]
- C2｜適用對象：每個符號彼此獨立、同分布（i.i.d.）的資料來源。[src:raw/03-source-coding-theorem.md#Introduction]
- C3｜壓到低於熵，幾乎一定會遺失資訊；但可以做到「任意接近熵」而幾乎不遺失。[src:raw/03-source-coding-theorem.md#Introduction]
- C4｜白話版：N 個符號、每個的熵是 H，只要給「多於 N×H 個 bits」就能在 N 很大時幾乎無損壓縮。[src:raw/03-source-coding-theorem.md#Statements]
- C5｜對「一個符號換一個碼字」的符號碼（symbol code），定理同時給出平均碼長的上界與下界。[src:raw/03-source-coding-theorem.md#Statements]
- C6｜這個定理讓 [[entropy]] 從抽象的「不確定性」變成有實際意義的「最少要用幾個 bits」。[src:raw/03-source-coding-theorem.md#Introduction]
