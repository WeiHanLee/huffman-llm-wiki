const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, ImageRun, ExternalHyperlink, AlignmentType, LevelFormat, PageBreak } = require("docx");
const { imageSize } = (() => { try { return require("image-size"); } catch { return {}; } })();

const S = "/tmp/claude-0/-home-claude/6f6f30fb-5e94-54b2-ab5d-d1f1e7600e23/scratchpad/doc";
const SHOTS = "/home/claude/huffman-wiki/checks/shots";
const WIKI_URL = process.env.WIKI_URL || "https://claude.ai/artifact/337UMUQ1j27QdhTN8JvQLL";
const DECK_URL = process.env.DECK_URL || "https://claude.ai/artifact/R7ijvj8J2HEQ5eEzStdojU";
const FONT = { ascii: "Calibri", hAnsi: "Calibri", eastAsia: "Microsoft JhengHei", cs: "Calibri" };

function pngSize(p) {
  const b = fs.readFileSync(p);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), data: b };
}
const r = (text, o = {}) => new TextRun({ text, font: FONT, size: 22, ...o });
const P = (runs, o = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [r(runs)], spacing: { after: 100, line: 300 }, ...o });
const H = (t) => new Paragraph({ children: [r(t, { bold: true, size: 26 })], spacing: { before: 280, after: 120 }, keepNext: true });
const B = (runs, level = 0) => new Paragraph({ children: Array.isArray(runs) ? runs : [r(runs)], numbering: { reference: "bul", level }, spacing: { after: 80, line: 300 } });
let INST = 1;
const N = (runs) => new Paragraph({ children: Array.isArray(runs) ? runs : [r(runs)], numbering: { reference: "num", level: 0, instance: INST }, spacing: { after: 80, line: 300 } });
const bold = (t) => r(t, { bold: true });
const link = (url) => new ExternalHyperlink({ link: url, children: [r(url, { color: "1F4FD8", underline: {} })] });
function IMG(path, caption, maxW = 600) {
  const { w, h, data } = pngSize(path);
  const width = Math.min(maxW, w), height = Math.round(h * width / w);
  return [
    new Paragraph({ children: [new ImageRun({ type: "png", data, transformation: { width, height } })], alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 }, keepNext: true }),
    new Paragraph({ children: [r(caption, { size: 20, color: "444444" })], alignment: AlignmentType.CENTER, spacing: { after: 220 } }),
  ];
}

const body = [
  P([bold("NTUST_M11507327_電機工程系_李威漢_用 LLM Wiki 做一份教學 HTML 簡報")], { spacing: { after: 240 } }),

  H("1. LLM Wiki 主題與簡短介紹"),
  B([bold("主題："), r("資料壓縮——Huffman 編碼與算術編碼")]),
  B([bold("讀者設定："), r("完全沒學過的同學（重直覺與例子，公式最少化）")]),
  B([bold("建立方式："), r("依 Karpathy 的 LLM Wiki 架構（raw/ → wiki/ → AGENTS.md），採「先討論、後生成」：先讓 AI 一次問一題、共 8 題（讀者、資料類型、語言、出處粒度、矛盾處理、ingest 方式、產出、lint 項目），整理成需求摘要；我追問是否符合滿分條件後，加入「孤兒頁」lint，確認後才產生 AGENTS.md 與資料夾。")]),
  B([bold("規模："), r("ingest 6 篇 Wikipedia 條目（Data compression、Entropy、Shannon's source coding theorem、Shannon–Fano coding、Huffman coding、Arithmetic coding），一篇一 commit；產出 9 個知識頁＋index.md＋log.md。")]),
  B([bold("規則："), r("每句關鍵主張標 [src:raw/檔名#章節]，數字必須能在所引章節找到；兩來源矛盾（Huffman 編碼年代 1950 vs 1951 提出／1952 發表）兩說並列標 ⚠；來源沒有、自行重算的數字標「計算值」並附 calc.py。")]),

  H("2. LLM Wiki 連結或成果"),
  B([r("Wiki 網頁："), link(WIKI_URL)]),
  B("網頁內含：所有知識頁、raw 原文（出處標籤可點到原文章節）、需求訪談紀錄、AGENTS.md、log.md、git 紀錄（11 個 commit）、lint 結果、Graph 設計、執行報告。", 0),

  H("3. 教學 HTML 簡報連結"),
  B([r("簡報："), link(DECK_URL), r("（共 15 頁，← → 鍵翻頁）")]),
  B([bold("教學結構："), r("為什麼壓縮 → 熵（極限）→ 前綴碼（規則）→ Shannon–Fano → Huffman 故事 → Huffman 三步驟（互動建樹）→ 成績單 → Huffman 的天花板 → 算術編碼（互動切區間）→ 對照表 → 回顧＋小測驗 → 參考來源。")]),
  B([bold("Wiki 與簡報的對應："), r("每句後面的標籤（如「entropy C6」）是證據卡編號，滑過去會顯示 wiki 原句；頁尾列出本頁用到的 wiki 頁；最後一頁列出「簡報 → wiki 頁 → 原始條目」。")]),

  H("4. Loop / Graph 流程說明"),
  ...IMG(`${S}/graph.png`, "圖 1：/topic-slides Graph（藍＝產出節點、黃＝程式檢查關卡、紅＝人或獨立 AI 判斷）"),
  N([bold("① 檢索 wiki → G1 覆蓋率關卡："), r("retrieve.py 依關鍵字找相關頁，相關頁需 ≥3 且 6 個必備概念都有對應頁，不足就停下（先 ingest 新來源）。")]),
  N([bold("② 證據卡（平行）："), r("每張卡只抽一個 wiki 頁，逐字複製帶出處的主張並編號 C1、C2…，不得改寫。")]),
  N([bold("③ 大綱 → 👤 人工確認："), r("由我確認教學順序；可退回改大綱，或發現缺主題時退回檢索。")]),
  N([bold("④ 逐頁稿 → G2 程式檢查："), r("每句有 [card:]、卡片存在且是大綱指定的、數字在所引卡片中、💡 比喻行不得含數字、8–15 頁、每頁 ≤230 字。")]),
  N([bold("🧑‍⚖ AI 審查（新對話）："), r("另開一個沒看過製作過程的 AI，只給稿＋卡＋raw，查忠實度與覆蓋率，避免自己審自己。")]),
  N([bold("⑤ 渲染 HTML → G3 渲染檢查："), r("render_deck.py 決定性轉換、不經 AI，保證不改字；Playwright 逐頁開啟檢查溢出、稿件每句原樣出現、Huffman 樹算出的碼字＝卡片、算術區間＝重算值、手機寬度不橫向捲動。")]),
  N([bold("⑥ 交件："), r("產出 report.md。全程由 tools/run_graph.sh（set -e）串接，任一關結束碼非 0 就停。")]),
  P([bold("哪些步驟會重複執行？")], { spacing: { before: 160, after: 60 } }),
  B("逐頁稿節點內部的「寫 → G2 → 修」小 loop（上限 2 輪）；渲染節點的「渲染 → 截圖檢查 → 縮短稿」（上限 2 輪）；整條 graph 最多 3 輪。"),
  P([bold("哪些地方需要檢查或重新生成？")], { spacing: { before: 160, after: 60 } }),
  B("錯在哪關退回哪關：某頁講錯只重寫那頁；卡片或 wiki 錯 → 修 wiki、重抽那一張卡；字太多不縮字級，退回逐頁稿縮短；缺主題退回檢索。"),
  P([bold("為什麼這樣設計？")], { spacing: { before: 160, after: 60 } }),
  B("每一關只能看上一關的產出，錯誤才能定位到單一節點。"),
  B("程式能檢查的（出處、數字、字數、溢出）都寫成腳本，「做完了」由結束碼決定，而不是 AI 說了算。"),
  B("忠實度這種程式判斷不了的，才交給「沒看過製作過程」的 AI 審查。"),
  B("渲染交給腳本，排版時不可能順手改字；每關產出都是檔案，可放進 git、可單獨重跑。"),

  H("5. 一次實際執行的結果與檢查紀錄"), (INST = 2, null),
  N([bold("G1："), r("9 頁相關、6 個必備概念都有頁 → 通過（順便修正檢索 bug：命中數把出處檔名也算進去）。")]),
  N([bold("人工確認："), r("我確認 14 頁大綱。")]),
  N([bold("G2 第 1 次："), r("0 問題 → 懷疑太鬆，做突變測試（故意埋 6 種錯）→ 6/6 都抓到，確認檢查有效（圖 4）。")]),
  N([bold("AI 審查第 1 輪："), r("錯誤 3、建議 6 → 不可渲染（圖 5）。3 個錯誤都在第 13 頁對照表：")]),
  B("「算術編碼較慢（需維護區間與精度）」的理由 raw 沒寫 → 退回 wiki", 1),
  B("把 raw 的「前綴碼用於 DEFLATE、JPEG、MP3」寫成 Huffman → 退回 wiki", 1),
  B("「所以 Huffman 仍到處都是」把 💡 個人看法變成事實句 → 退回逐頁稿，改引 bzip2／JPEG 的專利史實", 1),
  N([bold("退回後 G2 再擋 7 次："), r("2 次是審查員建議加的「1/4、1/8」，來源沒有這兩個數字，所以連審查員的建議也不能帶入；5 次是字數超限（圖 6）。")]),
  N([bold("G3 第 1 次："), r("參考頁溢出 72px、手機頁寬 512px → 修 CSS 後通過；Huffman 樹碼字與卡片一致，算術區間 [0,0.6)→[0.48,0.54)→[0.534,0.54) 與重算值一致（圖 7）。")]),
  N([bold("AI 審查第 2 輪（新的 AI）："), r("錯誤 0、建議 10 → 可交件；採用 2 項標示類建議。")]),
  N([bold("第 3 輪："), r("發現 G2 失敗時渲染仍照跑（指令沒依結束碼中斷）→ 新增 run_graph.sh，整條 graph 全過（圖 8）。")]),

  H("6. 反思"),
  P([bold("（1）建 Wiki 時特別考量的事情")], { spacing: { before: 120, after: 60 } }),
  B([bold("讀者決定深度："), r("訪談第一題就定下「完全沒學過的同學」，所以每頁開頭有一句白話解釋，術語第一次出現附英文。這個設定也一路影響簡報的教學順序。")]),
  B([bold("出處要細到程式能檢查："), r("每句標 [src:raw/檔名#章節]，並規定數字要能在那個章節找到，lint 才能自動檢查，簡報也能一路追溯到 raw。")]),
  B([bold("矛盾不替來源做決定："), r("Huffman 編碼年代兩說並列、標 ⚠ 並記進 log，而不是讓 AI 挑一個看起來對的。")]),
  B([bold("誠實記錄資料來源："), r("擷取工具只給摘要與短引文，每個 raw 檔都註明擷取方式；工具自己算出的「Huffman 約 2.23 bits」不當來源數字，改標計算值並用 calc.py 重算（同法算 Fano＝2.28，與來源一致）。")]),
  B([bold("一次一篇、每篇 commit："), r("每次 ingest 都會回頭更新舊頁，一篇一 commit，出錯時能看出是哪一篇造成的。")]),
  P([bold("（2）哪一個節點最常出錯？")], { spacing: { before: 160, after: 60 } }),
  P("「撰寫」節點，不論是寫 wiki 頁還是逐頁稿。建 wiki 時 lint 擋下 12 個問題，其中 6 個是同一種錯：AI 會把來源的英文數字詞自動轉寫（two bits→2、one bit→1、May→5 月）。更嚴重的是 AI 審查抓到的錯：它會把自己的推論（「較慢是因為要維護區間」）或主詞替換（前綴碼→Huffman）寫成有出處的事實。這些錯的共同點是「看起來有出處」，只檢查有沒有標出處抓不到，必須比對到 raw 原文。"),
  P([bold("（3）發現問題後，把檢查往前移到哪一步？")], { spacing: { before: 160, after: 60 } }),
  B("數字轉寫：第 3 次發生後，把「數字照抄來源寫法」寫進 AGENTS.md，從「寫完再 lint」移到「撰寫時就遵守」，之後同類錯誤就消失了。"),
  B("推論變事實：3 個錯誤中有 2 個的源頭在 wiki。只修簡報的話，wiki 會繼續錯，所以把修正往前推到 wiki 層，再重抽那張證據卡。"),
  B("💡 漏洞：「標成比喻就不受檢查」會被拿來夾帶事實，所以在 G2 規定 💡 行不得含數字，並把 wiki 中的 💡 事實句改成有出處的一般行。"),
  P([bold("（4）有沒有因此修改 workflow／graph？為什麼？")], { spacing: { before: 160, after: 60 } }),
  B("新增退回路線「AI 審查 → wiki → 重抽卡片」：錯誤源頭在 wiki 時，只修簡報治標不治本。"),
  B("新增突變測試：第一次全過時，無法判斷是檢查有效還是太鬆。lint 第一版就真的太鬆（整份檔案比對，「2」被別段的「base 2」誤配而放行）。"),
  B("新增 run_graph.sh：實際發生過 G2 失敗、渲染卻照跑，關卡必須由結束碼強制擋下。"),
  B("修正三個檢查器 bug（lint 整檔比對、檢索計分含檔名、渲染檢查讀不到摺疊的測驗答案）：檢查器本身也是會出錯的節點。"),
  B("第 13 頁字數超限，每次只刪幾個字，小修了 4 次，超過自訂上限 2 輪；改成一次刪掉與表格重複的整句。"),
  P([bold("（5）其他心得")], { spacing: { before: 160, after: 60 } }),
  P("最大的收穫是「全過」不等於正確：lint 第一次全過其實是檢查器有 bug；G3 也曾在 G2 失敗的情況下顯示全過。要讓 AI 的流程可信，除了檢查 AI 的產出，也要檢查「檢查本身」。"),

  new Paragraph({ children: [new PageBreak()] }),
  H("7. 此份作業的重點截圖"),
  ...IMG(`${S}/discussion_c.png`, "圖 2：先討論、後生成——8 題需求訪談紀錄（discussion.md）", 520),
  ...IMG(`${S}/wiki.png`, "圖 3：Wiki 知識頁（每句帶出處標籤，可點回 raw 原文章節；⚠ 標示兩來源矛盾）"),
  ...IMG(`${S}/t_mut.png`, "圖 4：G2 突變測試——故意埋 6 種錯，全部被抓到"),
  ...IMG(`${S}/review_c.png`, "圖 5：AI 審查第 1 輪（獨立對話）抓到的 3 個錯誤，並指出要退回 wiki 或逐頁稿", 560),
  ...IMG(`${S}/t_g2.png`, "圖 6：退回逐頁稿後 G2 擋下審查員建議中沒有出處的數字（1/4、1/8）與字數超限"),
  ...IMG(`${S}/t_g3.png`, "圖 7：G3 第 1 次：抓到參考頁溢出、手機橫向捲動；互動元件數值與卡片／重算值一致", 520),
  ...IMG(`${S}/t_run.png`, "圖 8：最終以 run_graph.sh 串接整條 graph，所有關卡通過", 520),
  ...IMG(`${S}/t_lint.png`, "圖 9：建 Wiki 時 lint 抓到「two bits」被寫成「2」"),
  ...IMG(`${S}/git.png`, "圖 10：git 紀錄——init 後一篇一 commit，再到 graph 三輪", 480),
  ...IMG(`${SHOTS}/slide-01.png`, "圖 11：簡報封面"),
  ...IMG(`${SHOTS}/slide-09.png`, "圖 12：Huffman 三步驟（互動建樹，按「下一步」逐步合併）"),
  ...IMG(`${SHOTS}/slide-12.png`, "圖 13：算術編碼（互動切區間，0.538 落在最終區間 [0.534, 0.54)）"),
  ...IMG(`${SHOTS}/slide-13.png`, "圖 14：對照表（AI 審查修正後版本）"),
  ...IMG(`${SHOTS}/slide-15.png`, "圖 15：參考來源頁——簡報 → wiki 頁 → 原始條目"),
];

const BODY = body.filter(Boolean);
const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 22 } } } },
  numbering: { config: [
    { reference: "bul", levels: [
      { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } },
      { level: 1, format: LevelFormat.BULLET, text: "◦", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1080, hanging: 270 } } } } ] },
    { reference: "num", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
  ] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children: BODY }],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(process.argv[2], b); console.log("ok", process.argv[2]); });
