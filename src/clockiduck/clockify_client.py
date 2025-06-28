"""
Client for interacting with the Clockify API.
"""

import requests
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field

from .config import settings

# --- Pydantic Models for API responses ---


class TimeInterval(BaseModel):
    start: datetime
    end: Optional[datetime] = None


class TimeEntry(BaseModel):
    id: str
    description: str
    user_id: str = Field(..., alias="userId")
    project_id: str = Field(..., alias="projectId")
    task_id: Optional[str] = Field(None, alias="taskId")
    time_interval: TimeInterval = Field(..., alias="timeInterval")

    @property
    def duration_seconds(self) -> int:
        """
        Calculates duration in seconds.
        If end time is not present (timer running), duration is 0.
        """
        if self.time_interval.end and self.time_interval.start:
            return int((self.time_interval.end - self.time_interval.start).total_seconds())
        return 0


# --- Clockify Client Class ---


class ClockifyClient:
    """A client to fetch data from the Clockify API."""

    def __init__(self, api_key: str, workspace_id: str):
        if not api_key or not workspace_id:
            raise ValueError("API key and Workspace ID are required.")
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.base_url = "https://api.clockify.me/api/v1"
        self.headers = {"X-Api-Key": self.api_key}
        self.user_id = self._get_user_id()

    def _get_user_id(self) -> str:
        """Fetches the user ID for the authenticated user."""
        response = requests.get(f"{self.base_url}/user", headers=self.headers)
        response.raise_for_status()
        return response.json()["id"]

    def get_time_entries(self, start: Optional[datetime] = None) -> List[TimeEntry]:
        """
        Fetches all time entries for the user since the given start time.
        Handles pagination automatically and filters out running timers.
        """
        all_entries: List[TimeEntry] = []
        page = 1
        page_size = 1000  # Use max page size for fewer requests

        endpoint = f"{self.base_url}/workspaces/{self.workspace_id}/user/{self.user_id}/time-entries"
        params = {"page-size": page_size}
        if start:
            params["start"] = start.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        while True:
            params["page"] = page
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            page_entries_data = response.json()
            if not page_entries_data:
                break

            for entry_data in page_entries_data:
                if entry_data.get("timeInterval", {}).get("end") is not None:
                    all_entries.append(TimeEntry.model_validate(entry_data))
            page += 1
        return all_entries


# A singleton instance for easy use across the app
client = ClockifyClient(api_key=settings.CLOCKIFY_API_KEY, workspace_id=settings.CLOCKIFY_WORKSPACE_ID)