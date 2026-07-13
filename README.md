# Report Generator

A Python CLI tool that generates annual performance reports from HackMD weekly notes using LLM services.

## Features

- ✅ Fetch weekly reports from HackMD
- ✅ Filter by folder and date range
- ✅ Support multiple LLM providers (OpenAI, Gemini, Claude, Claude Vertex AI, OpenAI-Compatible like vLLM, and Ollama Cloud)
- ✅ Token counting and limit checking
- ✅ Generate structured annual performance reports
- ✅ Save reports locally and upload to HackMD

## Installation

```bash
# Clone the repository
git clone https://github.com/allen3325/Work_Report_Generator.git
cd report-generator

# Install dependencies using uv (recommended)
uv sync
```

## Configuration

Get your api key here:
- [HackMD_API (Required)](https://hackmd.io/settings#api)
- LLM Service(Chose One)
- [OpenAI](https://platform.openai.com/api-keys)
- [Gemini](https://aistudio.google.com/api-keys)
- [Claude](https://platform.claude.com/settings/keys)

Create a `.env` file in the project root:

```env
# HackMD API
HACKMD_API_TOKEN=your_hackmd_token_here
HACKMD_API_URL=https://api.hackmd.io/v1  # Optional, defaults to this

# LLM API Keys and Models (both API key and model required based on your chosen provider)

# For OpenAI
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-5.4-mini  # Required: e.g., gpt-5.4-mini, gpt-5.5

# For Google Gemini
GEMINI_API_KEY=your_gemini_key_here
GEMINI_MODEL=gemini-3.5-flash  # Required: e.g., gemini-3.5-flash

# For Anthropic Claude
CLAUDE_API_KEY=your_claude_key_here
CLAUDE_MODEL=claude-sonnet-5  # Required: e.g., claude-sonnet-5, claude-opus-4-8

# For OpenAI Compatible (e.g., vLLM, Ollama, LiteLLM)
OPENAI_COMPATIBLE_API_KEY=your_compatible_api_key_here  # Can be a dummy value (e.g., "empty") if not required
OPENAI_COMPATIBLE_MODEL=your_model_name_here            # e.g., Qwen/Qwen2.5-7B-Instruct
OPENAI_COMPATIBLE_BASE_URL=http://localhost:8000/v1     # The API base endpoint

# For Ollama Cloud
OLLAMA_CLOUD_API_KEY=your_ollama_cloud_api_key_here
OLLAMA_CLOUD_MODEL=llama3:cloud  # e.g., llama3:cloud, gpt-oss:120b-cloud

# For Claude Vertex AI (Anthropic on GCP Vertex AI)
CLAUDE_VERTEX_PROJECT_ID=your_gcp_project_id_here
CLAUDE_VERTEX_REGION=global  # Optional, defaults to global
CLAUDE_VERTEX_MODEL=claude-sonnet-5  # Required: e.g., claude-3-5-sonnet@20240620 or claude-sonnet-5
```

## Usage

```bash
# Using OpenAI
python main.py \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --folder-name "DRC Weekly Report" \
  --max-tokens 100000 \
  --llm-provider openai \
  --year-tag 2025

# Using Google Gemini
python main.py \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --folder-name "DRC Weekly Report" \
  --max-tokens 500000 \
  --llm-provider gemini \
  --year-tag 2025

# Using Anthropic Claude
python main.py \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --folder-name "DRC Weekly Report" \
  --max-tokens 150000 \
  --llm-provider claude \
  --year-tag 2025

# Using OpenAI Compatible API (e.g., vLLM or Ollama)
python main.py \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --folder-name "DRC Weekly Report" \
  --max-tokens 150000 \
  --llm-provider openai_compatible \
  --year-tag 2025

# Using Ollama Cloud
python main.py \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --folder-name "DRC Weekly Report" \
  --max-tokens 150000 \
  --llm-provider ollama_cloud \
  --year-tag 2025

# Using Claude Vertex AI
python main.py \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --folder-name "DRC Weekly Report" \
  --max-tokens 150000 \
  --llm-provider claude_vertex \
  --year-tag 2025
```

## Command Line Arguments

| Argument | Type | Required | Description | Choices |
|----------|------|----------|-------------|---------|
| `--start-date` | string | ✅ | Start date (YYYY-MM-DD) | - |
| `--end-date` | string | ✅ | End date (YYYY-MM-DD) | - |
| `--folder-name` | string | ✅ | Target folder name in HackMD | - |
| `--max-tokens` | integer | ✅ | Maximum token limit | - |
| `--llm-provider` | string | ✅ | LLM service provider | `openai`, `gemini`, `claude`, `claude_vertex`, `openai_compatible`, `ollama_cloud` |
| `--year-tag` | string | ✅ | Year tag for HackMD | - |

## Agent Skills (智慧 Agent 技能)

本專案支援內建的 Agent Skills，能讓支援 Agent 能力的開發助手（例如 Google Antigravity、Claude Code、Codex 等）在不呼叫外部 LLM API 的情況下，由 Agent 親自閱讀週報、彙整內容並撰寫成年度績效報告。

### 內建技能：`hackmd-report`

此技能定義於以下路徑：
- Antigravity / Codex: [.agents/skills/hackmd-report/SKILL.md](file:///home/os-chewei.chang/Projects/report_generator/.agents/skills/hackmd-report/SKILL.md)
- Claude Code: [.claude/skills/hackmd-report/SKILL.md](file:///home/os-chewei.chang/Projects/report_generator/.claude/skills/hackmd-report/SKILL.md)

啟動後，Agent 會引導執行以下工作流：
1. **抓取週報**：執行輔助指令從 HackMD 抓取指定資料夾與時間區間的週報。
2. **閱讀週報**：Agent 逐一閱讀抓取下來的週報 Markdown 檔案。
3. **撰寫報告**：Agent 根據週報內容，以繁體中文撰寫符合專案規範結構的年度績效報告。
4. **存檔與上傳**：將報告儲存至本地的 `reports/` 資料夾，並上傳回 HackMD（權限設定為 owner-only 僅限擁有者）。

### 使用步驟

#### 1. 設定環境變數
於根目錄的 `.env` 中設定 HackMD 的 API Token：
```env
HACKMD_API_TOKEN=your_hackmd_token_here
```
*(注意：此模式不需要設定任何 LLM 相關的 API Key，如 `OPENAI_API_KEY` 或 `GEMINI_API_KEY`，因為 Agent 本身就是執行撰寫的 LLM。)*

#### 2. 喚醒 Agent 並下達指令
在支援 Agent 的終端機或對話視窗中，直接輸入以下指令，並提供必要的參數：

> **指令範例：**
> 「請幫我用 `hackmd-report` 技能生成 2025 年度的績效報告」

當 Agent 詢問或需要參數時，請提供以下資訊：
* **folder-name**：HackMD 中的週報資料夾名稱（例：`DRC Weekly Report`）
* **start-date** / **end-date**：日期區間，格式為 `YYYY-MM-DD`（例：`2025-01-01` 與 `2025-12-31`）
* **year-tag**：報告年份標籤（例：`2025`）

#### 3. Agent 自動化執行
Agent 將會自動執行以下流程：
1. 使用輔助腳本 [.agents/skills/hackmd-report/scripts/hackmd_cli.py](file:///home/os-chewei.chang/Projects/report_generator/.agents/skills/hackmd-report/scripts/hackmd_cli.py) 抓取週報：
   ```bash
   # Antigravity / OpenCode / Codex 平台
   uv run python .agents/skills/hackmd-report/scripts/hackmd_cli.py fetch \
     --folder-name "<folder-name>" \
     --start-date <start-date> \
     --end-date <end-date> \
     --output-dir <scratchpad>/weekly_notes

   # Claude Code 平台
   uv run python .claude/skills/hackmd-report/scripts/hackmd_cli.py fetch \
     --folder-name "<folder-name>" \
     --start-date <start-date> \
     --end-date <end-date> \
     --output-dir <scratchpad>/weekly_notes
   ```
2. 逐一閱讀並統整報告內容。
3. 產生報告並寫入本地檔案：`reports/年度績效報告_<start-date>_to_<end-date>.md`。
4. 上傳至 HackMD 並回報您報告的網址：
   ```bash
   # Antigravity / OpenCode / Codex 平台
   uv run python .agents/skills/hackmd-report/scripts/hackmd_cli.py upload \
     --title "年度績效報告_<start-date>_to_<end-date>" \
     --file "reports/年度績效報告_<start-date>_to_<end-date>.md" \
     --tags "annual-report, <year-tag>"
   ```

## Project Structure

```
report_generator/
├── main.py                  # Main entry point
├── config.py                # Configuration and argument parsing
├── utils.py                 # Utility functions
├── pyproject.toml           # Project dependencies configuration
├── uv.lock                  # Locked package versions
├── .env.example             # Environment variables example template
├── test_simple_workflow.py  # Simplified end-to-end test script
├── tests/                   # Test suite directory
│   ├── test_config.py       # Unit tests for configuration
│   ├── test_integration.py  # Integration tests for workflow
│   ├── test_ollama_cloud_client.py # Unit tests for Ollama Cloud client
│   └── test_openai_compatible_client.py # Unit tests for OpenAI-compatible client
└── clients/
    ├── hackmd_client.py     # HackMD API client
    └── llm/
        ├── __init__.py      # LLM client factory
        ├── base.py          # Abstract base class
        ├── openai_client.py # OpenAI implementation
        ├── gemini_client.py # Gemini implementation
        ├── claude_client.py # Claude implementation
        ├── claude_vertex_client.py # Claude Vertex AI implementation
        ├── openai_compatible_client.py # OpenAI-Compatible client implementation
        └── ollama_cloud_client.py # Ollama Cloud client implementation
```

## Report Structure

The generated report follows this structure:

```markdown
# 一、年度重點成就摘要

# 二、技術運用

# 三、技術研發

# 四、遇到的挑戰和解決方案

# 五、量化指標
```

## Error Handling

The tool handles various error scenarios:

- Missing environment variables
- Invalid API keys
- HackMD API failures
- LLM API failures
- Token limit exceeded
- Empty note content
- File system errors

## Development

```bash
# Install development dependencies using uv (recommended)
uv sync

# Or using pip
pip install -e .

# Run tests
uv run pytest

# Format code
uv run black .

# Lint code
uv run flake8 .

# Type checking
uv run mypy .
```
