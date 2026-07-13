#!/usr/bin/env python3
"""HackMD helper CLI for the hackmd-report skill.

Subcommands:
  fetch   Download weekly notes (filtered by folder + date range) to a directory.
  upload  Upload a markdown file to HackMD as a new note.

The HackMD API token is read from the HACKMD_API_TOKEN environment variable,
falling back to a .env file found in the current directory or any parent.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests

API_URL_DEFAULT = "https://api.hackmd.io/v1"


def load_dotenv_upward() -> None:
    """Populate os.environ from the nearest .env file (cwd upward), without overriding."""
    for directory in [Path.cwd(), *Path.cwd().parents]:
        env_file = directory / ".env"
        if env_file.is_file():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key, value = key.strip(), value.strip().strip("'\"")
                os.environ.setdefault(key, value)
            return


def get_headers() -> dict:
    token = os.environ.get("HACKMD_API_TOKEN")
    if not token:
        sys.exit("Error: HACKMD_API_TOKEN not set (env var or .env file).")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def api_url() -> str:
    return os.environ.get("HACKMD_API_URL", API_URL_DEFAULT).rstrip("/")


def date_to_ms(date_str: str, end_of_day: bool = False) -> int:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    ms = int(dt.timestamp() * 1000)
    if end_of_day:
        ms += 24 * 3600 * 1000 - 1
    return ms


def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*\s]+', "_", name).strip("_")[:80] or "untitled"


def cmd_fetch(args: argparse.Namespace) -> None:
    headers = get_headers()
    resp = requests.get(f"{api_url()}/notes", headers=headers)
    resp.raise_for_status()
    notes = resp.json()

    start_ms = date_to_ms(args.start_date)
    end_ms = date_to_ms(args.end_date, end_of_day=True)

    def in_folder(note: dict) -> bool:
        return any(
            f.get("name") == args.folder_name for f in note.get("folderPaths", [])
        )

    matched = [
        n
        for n in notes
        if in_folder(n) and start_ms <= n.get("createdAt", 0) <= end_ms
    ]
    matched.sort(key=lambda n: n.get("createdAt", 0))

    if not matched:
        sys.exit(
            f"Error: no notes found in folder '{args.folder_name}' "
            f"between {args.start_date} and {args.end_date}."
        )

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for i, note in enumerate(matched, 1):
        detail = requests.get(f"{api_url()}/notes/{note['id']}", headers=headers)
        detail.raise_for_status()
        data = detail.json()
        content = (data.get("content") or "").strip()
        title = data.get("title") or "Untitled"
        created = datetime.fromtimestamp(note["createdAt"] / 1000).strftime("%Y-%m-%d")
        if not content:
            print(f"  [skip] empty note: {title} ({note['id']})", file=sys.stderr)
            continue
        filename = f"{i:02d}_{created}_{sanitize_filename(title)}.md"
        (out_dir / filename).write_text(
            f"<!-- title: {title} | createdAt: {created} | id: {note['id']} -->\n\n"
            + content,
            encoding="utf-8",
        )
        manifest.append(
            {"file": filename, "title": title, "createdAt": created, "id": note["id"]}
        )
        print(f"  saved {filename}")

    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nFetched {len(manifest)} notes into {out_dir}/ (see manifest.json)")


def cmd_upload(args: argparse.Namespace) -> None:
    headers = get_headers()
    content = Path(args.file).read_text(encoding="utf-8")

    if args.tags:
        # HackMD reads tags from YAML frontmatter in the note content.
        frontmatter = f"---\ntags: {args.tags}\n---\n\n"
        if not content.lstrip().startswith("---"):
            content = frontmatter + content

    payload = {
        "title": args.title,
        "content": content,
        "readPermission": "owner",
        "writePermission": "owner",
    }
    resp = requests.post(f"{api_url()}/notes", headers=headers, json=payload)
    resp.raise_for_status()
    note = resp.json()
    print(f"Uploaded: https://hackmd.io/{note['id']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="Download filtered weekly notes")
    fetch.add_argument("--folder-name", required=True)
    fetch.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    fetch.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    fetch.add_argument("--output-dir", required=True)
    fetch.set_defaults(func=cmd_fetch)

    upload = sub.add_parser("upload", help="Upload a markdown file as a new note")
    upload.add_argument("--title", required=True)
    upload.add_argument("--file", required=True, help="Path to the markdown file")
    upload.add_argument(
        "--tags", default="", help="Comma-separated tags, e.g. 'annual-report, 2025'"
    )
    upload.set_defaults(func=cmd_upload)

    args = parser.parse_args()
    load_dotenv_upward()
    args.func(args)


if __name__ == "__main__":
    main()
