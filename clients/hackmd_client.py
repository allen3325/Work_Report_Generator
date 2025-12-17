import requests
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import time


class HackMDClient:
    """
    Client for interacting with HackMD API.

    Args:
        api_token (str): HackMD API token
        api_url (str, optional): HackMD API base URL. Defaults to "https://api.hackmd.io/v1".
    """

    def __init__(self, api_token: str, api_url: str = "https://api.hackmd.io/v1"):
        self.api_token = api_token
        self.api_url = api_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def get_notes(self) -> List[Dict[str, Any]]:
        """
        Get all notes from HackMD.

        Returns:
            List[Dict[str, Any]]: List of note metadata

        Raises:
            Exception: If API call fails
        """
        url = f"{self.api_url}/notes"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get notes from HackMD: {str(e)}")

    def get_note_content(self, note_id: str) -> Dict[str, Any]:
        """
        Get full content of a specific note.

        Args:
            note_id (str): The ID of the note to retrieve

        Returns:
            Dict[str, Any]: Full note content

        Raises:
            Exception: If API call fails or content is empty
        """
        url = f"{self.api_url}/notes/{note_id}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            note_data = response.json()

            # Check if content is empty
            if not note_data.get("content") or note_data["content"].strip() == "":
                raise Exception(
                    f"Note content is empty - [Note ID: {note_id}, Title: {note_data.get('title', 'Untitled')}]"
                )

            return note_data
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Failed to get note content - [Note ID: {note_id}, Error: {str(e)}]"
            )

    def upload_note(
        self, title: str, content: str, tags: Optional[List[str]] = None
    ) -> str:
        """
        Upload a new note to HackMD.

        Args:
            title (str): Title of the note
            content (str): Content of the note
            tags (Optional[List[str]]): List of tags for the note

        Returns:
            str: URL of the uploaded note

        Raises:
            Exception: If API call fails
        """
        url = f"{self.api_url}/notes"
        payload = {
            "title": title,
            "content": content,
            "readPermission": "owner",
            "writePermission": "owner"
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            note_data = response.json()
            print(note_data)
            return f"https://hackmd.io/{note_data['id']}"
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to upload note to HackMD: {str(e)}")

    def filter_notes_by_folder_and_date(
        self,
        notes: List[Dict[str, Any]],
        folder_name: str,
        start_date: str,
        end_date: str,
    ) -> List[Dict[str, Any]]:
        """
        Filter notes by folder name and date range.

        Args:
            notes (List[Dict[str, Any]]): List of notes to filter
            folder_name (str): Target folder name
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format

        Returns:
            List[Dict[str, Any]]: Filtered list of notes

        Raises:
            ValueError: If no notes found in the specified date range
        """
        # Convert date strings to timestamps
        start_timestamp = self._date_to_timestamp(start_date)
        end_timestamp = self._date_to_timestamp(end_date)

        filtered_notes = []

        for note in notes:
            # Check if note belongs to target folder
            if not self._note_in_folder(note, folder_name):
                continue

            # Check if note createdAt is within date range
            created_at = note.get("createdAt", 0)
            if start_timestamp <= created_at <= end_timestamp:
                filtered_notes.append(note)

        if not filtered_notes:
            raise ValueError(
                f"No notes found in folder '{folder_name}' "
                f"between {start_date} and {end_date}"
            )

        # Sort by createdAt in ascending order
        filtered_notes.sort(key=lambda x: x.get("createdAt", 0))

        return filtered_notes

    def _note_in_folder(self, note: Dict[str, Any], folder_name: str) -> bool:
        """
        Check if a note belongs to a specific folder.

        Args:
            note (Dict[str, Any]): Note metadata
            folder_name (str): Target folder name

        Returns:
            bool: True if note is in the folder, False otherwise
        """
        folder_paths = note.get("folderPaths", [])
        return any(folder.get("name") == folder_name for folder in folder_paths)

    def _date_to_timestamp(self, date_str: str) -> int:
        """
        Convert date string to Unix timestamp in milliseconds.

        Args:
            date_str (str): Date string in YYYY-MM-DD format

        Returns:
            int: Unix timestamp in milliseconds

        Raises:
            ValueError: If date format is invalid
        """
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return int(dt.timestamp() * 1000)
        except ValueError as e:
            raise ValueError(
                f"Invalid date format: {date_str}. Expected YYYY-MM-DD"
            ) from e
