from __future__ import annotations

from enum import auto

from fastapi_utils.enums import StrEnum


class Status(StrEnum):  # type: ignore
    WAITING = auto()
    IN_PROGRESS = auto()
    DONE = auto()
    FAILED = auto()

    @staticmethod
    def from_job_status(status: str) -> Status:
        if status == 'queued':
            return Status.WAITING
        if status == 'started':
            return Status.IN_PROGRESS
        if status == 'finished':
            return Status.DONE
        return Status.FAILED
