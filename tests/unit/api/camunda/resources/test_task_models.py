"""Tests for task response models."""

from __future__ import annotations

from camctl.api.camunda.resources.tasks.models.task import (
    CamundaFormRef,
    CountPerCandidateGroup,
    Task,
    TaskCompletionResult,
)


class TestTask:
    def test_from_dict_full_payload(self):
        data = {
            "id": "task-1",
            "name": "Review",
            "assignee": "john",
            "created": "2024-01-01T00:00:00Z",
            "due": "2024-01-02T00:00:00Z",
            "followUp": "2024-01-03T00:00:00Z",
            "lastUpdated": "2024-01-01T12:00:00Z",
            "delegationState": "PENDING",
            "description": "Review the document",
            "executionId": "exec-1",
            "owner": "admin",
            "parentTaskId": "parent-1",
            "priority": 50,
            "processDefinitionId": "proc-def-1",
            "processInstanceId": "proc-1",
            "caseDefinitionId": "case-def-1",
            "caseExecutionId": "case-exec-1",
            "taskDefinitionKey": "reviewTask",
            "formKey": "embedded:app:forms/review.html",
            "taskState": "CREATED",
            "status": "active",
            "tenantId": "tenant-1",
            "suspended": False,
            "caseInstanceId": "case-1",
        }
        task = Task.from_dict(data)
        assert task.id == "task-1"
        assert task.name == "Review"
        assert task.assignee == "john"
        assert task.follow_up == "2024-01-03T00:00:00Z"
        assert task.last_updated == "2024-01-01T12:00:00Z"
        assert task.priority == 50
        assert task.process_definition_id == "proc-def-1"
        assert task.task_definition_key == "reviewTask"
        assert task.tenant_id == "tenant-1"
        assert task.suspended is False

    def test_from_dict_with_camunda_form_ref(self):
        data = {
            "id": "task-2",
            "camundaFormRef": {
                "key": "form-key",
                "binding": "latest",
                "version": 3,
            },
        }
        task = Task.from_dict(data)
        assert isinstance(task.camunda_form_ref, CamundaFormRef)
        assert task.camunda_form_ref.key == "form-key"
        assert task.camunda_form_ref.binding == "latest"
        assert task.camunda_form_ref.version == 3

    def test_from_dict_minimal(self):
        task = Task.from_dict({"id": "task-3"})
        assert task.id == "task-3"
        assert task.name is None
        assert task.assignee is None

    def test_inherited_camunda_resource_fields(self):
        task = Task.from_dict({
            "id": "t1",
            "tenantId": "t",
            "suspended": True,
            "caseInstanceId": "c",
        })
        assert task.tenant_id == "t"
        assert task.suspended is True
        assert task.case_instance_id == "c"


class TestTaskCompletionResult:
    def test_from_dict(self):
        r = TaskCompletionResult.from_dict({
            "taskId": "task-1",
            "status": "completed",
            "message": "Task completed successfully",
        })
        assert r.task_id == "task-1"
        assert r.status == "completed"
        assert r.message == "Task completed successfully"


class TestCountPerCandidateGroup:
    def test_from_dict(self):
        r = CountPerCandidateGroup.from_dict({
            "groupName": "accounting",
            "taskCount": 42,
        })
        assert r.group_name == "accounting"
        assert r.task_count == 42
