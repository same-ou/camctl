"""Task service endpoint definitions."""

from __future__ import annotations

from enum import Enum


class TaskEndpoint(str, Enum):
    LIST = "task"
    COUNT = "task/count"
    COUNT_BY_CANDIDATE_GROUP = "task/report/candidate-group-count"
    DETAIL = "task/{task_id}"
    COMPLETE = "task/{task_id}/complete"
    TASK_VARIABLES = "task/{task_id}/variables"
    TASK_VARIABLE = "task/{task_id}/variables/{var_name}"
    LOCAL_TASK_VARIABLES = "task/{task_id}/localVariables"
    LOCAL_TASK_VARIABLE = "task/{task_id}/localVariables/{var_name}"
    
    


__all__ = ["TaskEndpoint"]
