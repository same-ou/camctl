"""Process service endpoint definitions."""

from __future__ import annotations

from enum import Enum


class ProcessEndpoint(str, Enum):
    LIST = "process-instance"
    COUNT = "process-instance/count"
    DETAIL = "process-instance/{process_id}"
    CANCEL = "process-instance/{process_id}"
    VARIABLES = "process-instance/{process_id}/variables"


__all__ = ["ProcessEndpoint"]
