#!/usr/bin/env python3
"""
Main entry point for the report generator.

This script generates an annual performance report from HackMD weekly notes
using LLM services.
"""

import os
import sys
from dotenv import load_dotenv
from typing import List, Dict, Any

# Import local modules
from config import parse_arguments, validate_env, get_env_vars
from clients.hackmd_client import HackMDClient
from clients.llm import create_llm_client
from utils import build_prompt, save_local_report


def main():
    """
    Main function to execute the report generation workflow.
    """
    try:
        # 1. Load environment variables
        load_dotenv()

        # # 2. Parse command line arguments
        args = parse_arguments()

        # # 3. Validate environment variables
        validate_env(args.llm_provider)

        # # 4. Get environment variables
        env_vars = get_env_vars()

        print(f"Starting report generation...")
        print(f"Date range: {args.start_date} to {args.end_date}")
        print(f"Folder: {args.folder_name}")
        print(f"LLM Provider: {args.llm_provider}")

        # # 5. Initialize clients
        hackmd = HackMDClient(
            api_token=env_vars["HACKMD_API_TOKEN"], api_url=env_vars["HACKMD_API_URL"]
        )

        llm = create_llm_client(
            provider=args.llm_provider,
            api_key=env_vars[f"{args.llm_provider.upper()}_API_KEY"],
            model=env_vars[f"{args.llm_provider.upper()}_MODEL"],
        )

        print(f"Clients initialized")

        # 6. Get all notes from HackMD
        print(f"Fetching notes from HackMD...")
        all_notes = hackmd.get_notes()
        print(f"Found {len(all_notes)} notes total")

        # 7. Filter notes by folder and date range
        print(f"Filtering notes...")
        filtered_notes = hackmd.filter_notes_by_folder_and_date(
            notes=all_notes,
            folder_name=args.folder_name,
            start_date=args.start_date,
            end_date=args.end_date,
        )
        print(
            f"Found {len(filtered_notes)} notes in specified folder and date range"
        )

        # 8. Get full content for each filtered note and calculate tokens
        print(f"Retrieving full content and calculating tokens...")
        notes_with_content = []
        total_tokens = 0

        for note in filtered_notes:
            try:
                # Get full note content
                full_note = hackmd.get_note_content(note["id"])
                notes_with_content.append(full_note)

                # Count tokens for this note
                note_tokens = llm.count_tokens(full_note["content"])
                total_tokens += note_tokens
                print(f"  Note '{full_note['title']}' - {note_tokens} tokens")

            except Exception as e:
                print(f"Error processing note {note.get('id', 'unknown')}: {str(e)}")
                continue

        # 9. Check token limit
        print(f"Total tokens: {total_tokens}")
        if total_tokens > args.max_tokens:
            raise ValueError(
                f"Total token count ({total_tokens}) exceeds limit ({args.max_tokens})"
            )

        # 10. Build prompt for LLM
        print(f"Building prompt for LLM...")
        prompt = build_prompt(notes_with_content)
        # 11. Generate report using LLM
        print(
            f"Generating report with {llm.get_provider_name()} ({llm.get_model_name()})..."
        )
        report_content = llm.generate(prompt)

        # 12. Save report locally
        print(f"Saving report locally...")
        local_filename = save_local_report(
            content=report_content, start_date=args.start_date, end_date=args.end_date
        )
        print(f"Report saved to: {local_filename}")

        # 13. Upload to HackMD
        print(f"Uploading to HackMD...")
        try:
            hackmd_url = hackmd.upload_note(
                title=f"年度績效報告_{args.start_date}_to_{args.end_date}",
                content=report_content,
                tags=["annual-report", args.year_tag],
            )
            print(f"Report uploaded to HackMD: {hackmd_url}")
        except Exception as e:
            print(
                f"Warning: Failed to upload to HackMD, but local file was saved: {str(e)}"
            )

        print(f"Report generation completed successfully!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
