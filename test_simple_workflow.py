#!/usr/bin/env python3
"""
Simple test script to verify the complete workflow works.
This tests the integration without requiring actual API calls.
"""

import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime

# Get project root directory (where this file is located)
project_root = os.path.dirname(os.path.abspath(__file__))
# Add the project root to Python path
sys.path.insert(0, project_root)

from main import main


def test_simple_workflow():
    """Test a simplified version of the workflow."""

    print("🧪 Starting simple workflow test...")

    # Mock environment variables
    test_env = {
        "HACKMD_API_TOKEN": "test_token",
        "OPENAI_API_KEY": "test_openai_key",
        "OPENAI_MODEL": "gpt-6-luna",
        "HACKMD_API_URL": "https://api.hackmd.io/v1",
    }

    # Mock command line arguments
    test_args = [
        "--start-date",
        "2024-01-01",
        "--end-date",
        "2024-01-31",
        "--folder-name",
        "Test Folder",
        "--max-tokens",
        "10000",
        "--llm-provider",
        "openai",
        "--year-tag",
        "2024",
    ]

    # Mock note data
    mock_note = {
        "id": "test_note_id",
        "title": "Test Weekly Report",
        "createdAt": int(
            datetime.strptime("2024-01-15", "%Y-%m-%d").timestamp() * 1000
        ),
        "folderPaths": [{"name": "Test Folder"}],
        "content": "This week I worked on project X and solved issue Y.",
    }

    with (
        patch.dict(os.environ, test_env, clear=True),
        patch("sys.argv", ["main.py"] + test_args),
    ):

        # Mock the HackMD client
        with patch(
            "main.HackMDClient"
        ) as mock_hackmd_class:
            mock_hackmd_instance = MagicMock()
            mock_hackmd_class.return_value = mock_hackmd_instance

            # Mock HackMD API responses
            mock_hackmd_instance.get_notes.return_value = [mock_note]
            mock_hackmd_instance.filter_notes_by_folder_and_date.return_value = [
                mock_note
            ]
            mock_hackmd_instance.get_note_content.return_value = mock_note
            mock_hackmd_instance.upload_note.return_value = (
                "https://hackmd.io/test-report"
            )

            # Mock LLM client
            with patch(
                "main.create_llm_client"
            ) as mock_llm_factory:
                mock_llm_instance = MagicMock()
                mock_llm_instance.get_provider_name.return_value = "openai"
                mock_llm_instance.get_model_name.return_value = "gpt-6-luna"
                mock_llm_instance.count_tokens.return_value = 50  # Well under limit
                mock_llm_instance.generate.return_value = """
# 一、年度重點成就摘要

本年度完成了多個重要專案，包括X、Y和Z系統的開發與部署。

# 二、技術運用

- 開發了X系統並應用於A專案
- 實現了Y功能用於B客戶

# 三、技術研發

- 研究了新的機器學習算法
- 發表了關於Z技術的論文

# 四、遇到的挑戰和解決方案

主要挑戰包括資源限制和技術債務，通過優先級管理和重構成功解決。

# 五、量化指標

- 完成專案數：12個
- 解決問題數：45個
- 客戶滿意度：95%
"""
                mock_llm_factory.return_value = mock_llm_instance

                # Mock file saving
                with patch("main.save_local_report") as mock_save:
                    mock_save.return_value = "年度績效報告_2024-01-01_to_2024-01-31.md"

                    try:
                        main()
                        print("✅ Workflow completed successfully!")
                    except SystemExit as e:
                        if e.code != 0:
                            raise AssertionError(f"Workflow failed with SystemExit {e.code}")
                        print("✅ Workflow completed with SystemExit 0")

                    # Verify key calls were made
                    assert mock_hackmd_instance.get_notes.called
                    assert (
                        mock_hackmd_instance.filter_notes_by_folder_and_date.called
                    )
                    assert mock_hackmd_instance.get_note_content.called
                    assert mock_llm_instance.count_tokens.called
                    assert mock_llm_instance.generate.called
                    assert mock_save.called
                    assert mock_hackmd_instance.upload_note.called

                    print("✅ All expected function calls were made")


if __name__ == "__main__":
    try:
        test_simple_workflow()
        print("All tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
