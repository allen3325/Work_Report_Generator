# Report Generator

A Python CLI tool that generates annual performance reports from HackMD weekly notes using LLM services.

## Features

- ✅ Fetch weekly reports from HackMD
- ✅ Filter by folder and date range
- ✅ Support multiple LLM providers (OpenAI, Gemini, Claude)
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
CLAUDE_MODEL=claude-sonnet-4-6  # Required: e.g., claude-sonnet-4-6, claude-opus-4-8
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
```

## Command Line Arguments

| Argument | Type | Required | Description | Choices |
|----------|------|----------|-------------|---------|
| `--start-date` | string | ✅ | Start date (YYYY-MM-DD) | - |
| `--end-date` | string | ✅ | End date (YYYY-MM-DD) | - |
| `--folder-name` | string | ✅ | Target folder name in HackMD | - |
| `--max-tokens` | integer | ✅ | Maximum token limit | - |
| `--llm-provider` | string | ✅ | LLM service provider | `openai`, `gemini`, `claude` |
| `--year-tag` | string | ✅ | Year tag for HackMD | - |

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
│   └── test_integration.py  # Integration tests for workflow
└── clients/
    ├── hackmd_client.py     # HackMD API client
    └── llm/
        ├── __init__.py      # LLM client factory
        ├── base.py          # Abstract base class
        ├── openai_client.py # OpenAI implementation
        ├── gemini_client.py # Gemini implementation
        └── claude_client.py # Claude implementation
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
