from typing import List, Dict, Any
from datetime import datetime
import os


def build_prompt(filtered_notes: List[Dict[str, Any]]) -> str:
    """
    Build the prompt for LLM report generation.

    Args:
        filtered_notes (List[Dict[str, Any]]): List of filtered notes

    Returns:
        str: Formatted prompt for LLM
    """
    prompt = """你是一位專業的績效報告撰寫助理。請根據以下週報內容，生成一份完整的年度工作績效報告。

報告必須包含以下章節（使用 Markdown 格式）：

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

---

以下是按時間順序排列的週報內容：
"""

    for i, note in enumerate(filtered_notes, 1):
        created_at = note.get("createdAt", 0)
        date_str = datetime.fromtimestamp(created_at / 1000).strftime("%Y-%m-%d")
        title = note.get("title", "Untitled")

        prompt += f"""
## 週報 {i} (創建日期: {date_str})
{title}

## 內容
{note.get("content")}
"""

    return prompt


def calculate_total_tokens(filtered_notes: List[Dict[str, Any]], llm_client) -> int:
    """
    Calculate total tokens for all notes.

    Args:
        filtered_notes (List[Dict[str, Any]]): List of filtered notes
        llm_client: LLM client for token counting

    Returns:
        int: Total token count
    """
    total_tokens = 0

    for note in filtered_notes:
        # Get note content (we need to fetch full content for token counting)
        note_content = note.get("content", "")
        if note_content:
            total_tokens += llm_client.count_tokens(note_content)

    return total_tokens


def save_local_report(content: str, start_date: str, end_date: str) -> str:
    """
    Save the generated report to a local file.

    Args:
        content (str): Report content
        start_date (str): Start date
        end_date (str): End date

    Returns:
        str: Path to the saved file

    Raises:
        Exception: If file writing fails
    """
    # Get project root directory (where utils.py is located)
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Create reports directory in project root if it doesn't exist
    reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # Build filename with reports directory
    filename = f"年度績效報告_{start_date}_to_{end_date}.md"
    filepath = os.path.join(reports_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath
    except IOError as e:
        raise Exception(f"Failed to write local file: {str(e)}")
