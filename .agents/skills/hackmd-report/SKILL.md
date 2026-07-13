---
name: hackmd-report
description: 從 HackMD 抓取指定資料夾與日期區間的週報，由 agent 親自閱讀並統整成年度績效報告，最後上傳回 HackMD。Use when the user asks to generate an annual/performance report from HackMD weekly notes (e.g. 「生成年度報告」、「統整週報」、"generate my annual report from HackMD").
---

# HackMD 年度績效報告生成

從 HackMD 抓取週報 → **由你（agent）親自閱讀並撰寫報告** → 存檔 → 上傳回 HackMD。
不呼叫任何外部 LLM API — 你就是撰寫報告的 LLM。

## 前置需求

- `.env`（專案根目錄）需有 `HACKMD_API_TOKEN`（選填 `HACKMD_API_URL`，預設 `https://api.hackmd.io/v1`）。
- helper script 只依賴 `requests`，用 `uv run python` 執行即可。

## 需要的參數

向使用者確認（缺一不可）：
1. **folder-name** — HackMD 資料夾名稱（例：`DRC Weekly Report`）
2. **start-date / end-date** — `YYYY-MM-DD` 日期區間
3. **year-tag** — 報告年份標籤（例：`2025`）

## 工作流程

### 1. 抓取週報

請根據你目前執行的平台，選擇對應的路徑執行指令：

**對於 Antigravity CLI / OpenCode / Codex：**
```bash
uv run python .agents/skills/hackmd-report/scripts/hackmd_cli.py fetch \
  --folder-name "<folder-name>" \
  --start-date <start-date> \
  --end-date <end-date> \
  --output-dir <scratchpad>/weekly_notes
```

**對於 Claude：**
```bash
uv run python .claude/skills/hackmd-report/scripts/hackmd_cli.py fetch \
  --folder-name "<folder-name>" \
  --start-date <start-date> \
  --end-date <end-date> \
  --output-dir <scratchpad>/weekly_notes
```

週報會依建立時間排序存成 `NN_YYYY-MM-DD_標題.md`，並附 `manifest.json` 清單。
若回報找不到 notes，向使用者確認資料夾名稱與日期區間是否正確。

### 2. 閱讀全部週報

用 Read 工具逐一讀取 `weekly_notes/` 下所有 `.md` 檔（依檔名序號即時間順序）。
閱讀時記下：重要成果、應用到專案的技術、研發性質的工作、遇到的問題與解法、可量化的數字（完成專案數、解決問題數等）。

### 3. 撰寫年度績效報告

以繁體中文撰寫，**必須**使用以下章節結構（Markdown 格式）：

```markdown
# 一、年度重點成就摘要
[簡述本年度最重要的工作成果]

# 二、技術運用
說明：開發之技術或系統，實際應用於 BG/BU/外部客戶
評估原則：開發何種技術/系統/功能用於哪一專案
[請列舉具體的技術應用案例]

# 三、技術研發
說明：研發新技術
評估原則：研發何種技術/功能於院長會議中報告討論，或申請專利論文
[請列舉研發性質的工作內容]

# 四、遇到的挑戰和解決方案
[描述主要挑戰及對應的解決方法]

# 五、量化指標
- 完成專案數：[X] 個
- 解決問題數：[Y] 個
- 其他相關數據
```

撰寫原則：
- 內容必須完全根據週報事實，不得虛構成果或數字；量化指標要能從週報內容對得上。
- 合併同一專案跨多週的進度為一條完整敘事，不要逐週流水帳。
- 具體點名技術、系統、專案名稱。

### 4. 存檔到本地

寫入 `reports/年度績效報告_<start-date>_to_<end-date>.md`（沿用專案既有慣例）。

### 5. 上傳到 HackMD

請根據你目前執行的平台，選擇對應的路徑執行指令：

**對於 Antigravity CLI / OpenCode / Codex：**
```bash
uv run python .agents/skills/hackmd-report/scripts/hackmd_cli.py upload \
  --title "年度績效報告_<start-date>_to_<end-date>" \
  --file "reports/年度績效報告_<start-date>_to_<end-date>.md" \
  --tags "annual-report, <year-tag>"
```

**對於 Claude：**
```bash
uv run python .claude/skills/hackmd-report/scripts/hackmd_cli.py upload \
  --title "年度績效報告_<start-date>_to_<end-date>" \
  --file "reports/年度績效報告_<start-date>_to_<end-date>.md" \
  --tags "annual-report, <year-tag>"
```

權限為 owner-only（read/write），與原本 pipeline 一致。上傳成功後把 HackMD URL 與本地檔案路徑一併回報給使用者；若上傳失敗，本地檔案仍保留，回報錯誤並附上本地路徑。
