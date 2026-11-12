# Wiki 目錄：資料壓縮（Huffman 編碼與算術編碼）

> 讀者：完全沒學過的同學。建議閱讀順序由上而下。

## 基礎
- [[data-compression]]：資料壓縮是什麼、編碼器／解碼器、熵編碼的歷史脈絡
- [[lossless-vs-lossy]]：無失真與失真壓縮的差別與例子
- [[entropy]]：熵＝平均意外程度，也是無失真壓縮的極限
- [[source-coding-theorem]]：信源編碼定理——熵是壓縮的地板

## 編碼方法
- [[prefix-code]]：前綴碼——為什麼一串 0/1 能唯一解碼
- [[shannon-fano]]：由上而下對半切的早期方法，含與 Huffman 的同例比較
- [[huffman-coding]]：由下而上合併的最佳前綴碼，含建樹三步驟與 a–e 例子（⚠ 年代矛盾）
- [[arithmetic-coding]]：把整則訊息縮成一個小數的區間切分法

## 比較
- [[huffman-vs-arithmetic]]：整數位元限制、對照表、為何 Huffman 仍廣泛使用
