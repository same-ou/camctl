"""Tests for process response models."""

from __future__ import annotations

from camctl.api.camunda.resources.processes.models.process import (
    ProcessCancelResult,
    ProcessInstance,
    ProcessStartResult,
)


class TestProcessInstance:
    def test_from_dict_full(self):
        data = {
            "id": "proc-1",
            "definitionId": "def-1",
            "definitionKey": "invoiceProcess",
            "businessKey": "INV-001",
            "ended": False,
            "tenantId": "tenant-1",
            "suspended": False,
            "caseInstanceId": "case-1",
            "links": [{"rel": "self", "href": "/process-instance/proc-1"}],
        }
        p = ProcessInstance.from_dict(data)
        assert p.id == "proc-1"
        assert p.definition_id == "def-1"
        assert p.definition_key == "invoiceProcess"
        assert p.business_key == "INV-001"
        assert p.ended is False
        assert p.tenant_id == "tenant-1"
        assert p.suspended is False
        assert p.links is not None

    def test_from_dict_minimal(self):
        p = ProcessInstance.from_dict({"id": "proc-2"})
        assert p.id == "proc-2"
        assert p.definition_id is None
        assert p.business_key is None
        assert p.ended is None

    def test_inherited_fields(self):
        p = ProcessInstance.from_dict({
            "id": "p1",
            "tenantId": "t",
            "suspended": True,
            "caseInstanceId": "c",
        })
        assert p.tenant_id == "t"
        assert p.suspended is True
        assert p.case_instance_id == "c"


class TestProcessStartResult:
    def test_from_dict(self):
        r = ProcessStartResult.from_dict({
            "processInstanceId": "proc-1",
            "status": "started",
            "message": "Process started",
        })
        assert r.process_instance_id == "proc-1"
        assert r.status == "started"
        assert r.message == "Process started"


class TestProcessCancelResult:
    def test_from_dict(self):
        r = ProcessCancelResult.from_dict({
            "processId": "proc-1",
            "status": "cancelled",
            "message": "Process cancelled",
        })
        assert r.process_id == "proc-1"
        assert r.status == "cancelled"
        assert r.message == "Process cancelled"
