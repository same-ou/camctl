"""Tests for Resource, IdentifiableResource, and CamundaResource."""

from dataclasses import dataclass
from typing import Optional

from camctl.api.camunda.common.resource import (
    CamundaResource,
    IdentifiableResource,
    Resource,
)


# Module-level classes needed for nested resource tests because
# get_type_hints resolves forward refs in the module namespace.


@dataclass(kw_only=True)
class _Inner(Resource):
    value: Optional[str] = None


@dataclass(kw_only=True)
class _Outer(Resource):
    inner: Optional[_Inner] = None


class TestResourceFromDict:
    def test_camel_to_snake_conversion(self):
        @dataclass(kw_only=True)
        class MyResource(Resource):
            first_name: Optional[str] = None
            last_name: Optional[str] = None

        r = MyResource.from_dict({"firstName": "John", "lastName": "Doe"})
        assert r.first_name == "John"
        assert r.last_name == "Doe"

    def test_unknown_keys_filtered(self):
        @dataclass(kw_only=True)
        class MyResource(Resource):
            name: Optional[str] = None

        r = MyResource.from_dict({"name": "test", "unknownKey": "ignored"})
        assert r.name == "test"

    def test_raw_preserved(self):
        @dataclass(kw_only=True)
        class MyResource(Resource):
            first_name: Optional[str] = None

        data = {"firstName": "John", "extra": "data"}
        r = MyResource.from_dict(data)
        assert "first_name" in r.raw
        assert "extra" in r.raw

    def test_nested_resource_auto_parsed(self):
        r = _Outer.from_dict({"inner": {"value": "nested"}})
        assert isinstance(r.inner, _Inner)
        assert r.inner.value == "nested"

    def test_empty_dict(self):
        r = Resource.from_dict({})
        assert r.raw == {}


class TestResourceToDict:
    def test_round_trip(self):
        @dataclass(kw_only=True)
        class MyResource(Resource):
            name: Optional[str] = None

        r = MyResource.from_dict({"name": "test"})
        d = r.to_dict()
        assert d["name"] == "test"

    def test_nested_resources_serialized(self):
        r = _Outer.from_dict({"inner": {"value": "nested"}})
        d = r.to_dict()
        assert isinstance(d["inner"], dict)
        assert d["inner"]["value"] == "nested"

    def test_none_fields_excluded(self):
        @dataclass(kw_only=True)
        class MyResource(Resource):
            present: Optional[str] = None
            absent: Optional[str] = None

        r = MyResource(present="yes", absent=None)
        d = r.to_dict()
        assert "present" in d
        assert "absent" not in d


class TestIdentifiableResource:
    def test_id_populated_from_dict(self):
        r = IdentifiableResource.from_dict({"id": "abc-123"})
        assert r.id == "abc-123"

    def test_id_default_none(self):
        r = IdentifiableResource.from_dict({})
        assert r.id is None


class TestCamundaResource:
    def test_fields_from_dict(self):
        r = CamundaResource.from_dict({
            "id": "abc",
            "tenantId": "tenant-1",
            "suspended": True,
            "caseInstanceId": "case-1",
        })
        assert r.id == "abc"
        assert r.tenant_id == "tenant-1"
        assert r.suspended is True
        assert r.case_instance_id == "case-1"

    def test_default_none(self):
        r = CamundaResource.from_dict({})
        assert r.tenant_id is None
        assert r.suspended is None
        assert r.case_instance_id is None
