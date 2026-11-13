# 任務：把這個資料夾發布到 GitHub，並開啟 GitHub Pages

> 給 Claude Code CLI 執行。請在**這個資料夾（huffman-wiki/，也就是本檔所在位置）**裡開啟 Claude Code，然後說：「照 PUBLISH_TO_GITHUB.md 執行」。

## 背景（不用改任何內容）
- 這是一個已經完成的作業資料夾，**已經是 git repo**（有完整 commit 紀錄，分支 `main`），只是還沒有 remote。
- `docs/` 裡有三個已測試過的獨立網頁：`index.html`（入口）、`slides.html`（教學簡報）、`wiki.html`（Wiki 網頁）。
- `submission/` 裡的 Word/PDF 繳交檔，連結**已經預先寫成**下面的網址，所以 repo 名稱必須完全一樣。

| 項目 | 值 |
|---|---|
| GitHub 帳號 | `WeiHanLee` |
| repo 名稱 | `huffman-llm-wiki`（公開 Public） |
| Pages 來源 | 分支 `main`、資料夾 `/docs` |
| 完成後網址 | https://weihanlee.github.io/huffman-llm-wiki/ 、 …/slides.html 、 …/wiki.html |

## 規則
- **不要修改、刪除、重新產生**任何既有檔案，也不要 rewrite git 歷史（不要 rebase、amend、force push）。git 紀錄本身就是作業的證據。
- 每一步做完先確認成功，再做下一步；失敗就停下來，告訴我錯誤訊息和建議做法。
- 不要把任何 token 或密碼寫進檔案。

## 步驟

### 1. 檢查環境
```bash
git --version
gh --version
gh auth status
git status --short          # 應該是乾淨的
git log --oneline | head -5 # 最新一筆應該是 "publish: ..." 或 "docs/: standalone pages ..."
git branch --show-current   # 應該是 main
```
- 沒有 `gh`：Windows 用 `winget install --id GitHub.cli`，macOS 用 `brew install gh`，裝完執行 `gh auth login`（選 GitHub.com → HTTPS → 用瀏覽器登入）。
- `gh auth status` 顯示的帳號必須是 `WeiHanLee`。

### 2. 建立公開 repo 並推送
先檢查 repo 是否已存在：
```bash
gh repo view WeiHanLee/huffman-llm-wiki >/dev/null 2>&1 && echo EXISTS || echo NOT_FOUND
```
- **NOT_FOUND** → 建立並一次推送：
  ```bash
  gh repo create WeiHanLee/huffman-llm-wiki --public --source=. --remote=origin --push \
    --description "NTUST 生成式 AI 第十週：資料壓縮 LLM Wiki（Huffman／算術編碼）與教學 HTML 簡報"
  ```
- **EXISTS**（我先在網頁上建好了空 repo）→ 只加 remote 並推送：
  ```bash
  git remote add origin https://github.com/WeiHanLee/huffman-llm-wiki.git
  git push -u origin main
  ```
  如果 push 被拒，是因為 repo 不是空的（例如建立時勾了 README）。**不要 force push**，停下來告訴我。

### 3. 開啟 GitHub Pages（main 分支的 /docs）
```bash
gh api -X POST repos/WeiHanLee/huffman-llm-wiki/pages \
  -f "source[branch]=main" -f "source[path]=/docs"
```
- 如果回應說 Pages 已經存在（409），改用更新：
  ```bash
  gh api -X PUT repos/WeiHanLee/huffman-llm-wiki/pages \
    -f "source[branch]=main" -f "source[path]=/docs"
  ```
- 如果 API 失敗，請我手動操作：repo → Settings → Pages → Source 選「Deploy from a branch」→ Branch 選 `main`、資料夾選 `/docs` → Save。

### 4. 等部署完成並驗證
Pages 第一次部署大約需要 1～3 分鐘。每 20 秒檢查一次，最多 5 分鐘：
```bash
gh api repos/WeiHanLee/huffman-llm-wiki/pages --jq '.status'   # 等到 built
for u in "" slides.html wiki.html; do
  curl -s -o /dev/null -w "%{http_code}  https://weihanlee.github.io/huffman-llm-wiki/$u\n" "https://weihanlee.github.io/huffman-llm-wiki/$u"
done
```
三個都要是 `200`。再確認內容正確：
```bash
curl -s https://weihanlee.github.io/huffman-llm-wiki/slides.html | grep -o "<title>[^<]*</title>"   # 應為 Huffman 與算術編碼入門
curl -s https://weihanlee.github.io/huffman-llm-wiki/wiki.html   | grep -o "<title>[^<]*</title>"   # 應為 Huffman 壓縮 LLM Wiki
```

### 5. 回報
完成後用繁體中文告訴我：
1. repo 網址
2. 三個 Pages 網址，以及各自的 HTTP 狀態
3. 繳交檔位置：`submission/NTUST_M11507327_電機工程系_李威漢_用LLM Wiki做一份教學HTML簡報.pdf`（連結已是上面的網址，**不需要重新產生**）
4. 請我用**無痕視窗**打開簡報網址，確認不用登入就能看，並用 ← → 翻頁

## 若網址必須改（例如 repo 名稱不同）
只有在 repo 名稱不是 `huffman-llm-wiki` 時才需要處理：先告訴我，因為 `submission/` 的 Word/PDF 和 `submission.md` 裡的網址都要跟著改。Word 檔可以直接在 Word 裡編輯第 2、3 節的連結，再另存 PDF。
