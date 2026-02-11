"""Tests for serialization utility functions."""

from __future__ import annotations

import json
from dataclasses import dataclass

from camctl.api.camunda.common.resource import Resource
from camctl.utils.serialization import dumps_json, normalize


class TestNormalize:
    def test_resource(self):
        @dataclass(kw_only=True)
        class MyResource(Resource):
            name: str | None = None

        r = MyResource.from_dict({"name": "test"})
        result = normalize(r)
        assert isinstance(result, dict)
        assert result["name"] == "test"

    def test_nested_dataclass(self):
        @dataclass
        class Inner:
            value: int = 1

        @dataclass
        class Outer:
            inner: Inner | None = None

        result = normalize(Outer(inner=Inner(value=42)))
        assert result == {"inner": {"value": 42}}

    def test_plain_dict(self):
        result = normalize({"a": 1, "b": {"c": 2}})
        assert result == {"a": 1, "b": {"c": 2}}

    def test_list(self):
        result = normalize([1, 2, {"a": 3}])
        assert result == [1, 2, {"a": 3}]

    def test_tuple(self):
        result = normalize((1, 2, 3))
        assert result == [1, 2, 3]

    def test_scalar(self):
        assert normalize(42) == 42
        assert normalize("hello") == "hello"
        assert normalize(None) is None


class TestDumpsJson:
    def test_output_is_valid_json(self):
        result = dumps_json({"key": "value"})
        parsed = json.loads(result)
        assert parsed == {"key": "value"}

    def test_pretty_printed(self):
        result = dumps_json({"a": 1})
        assert "\n" in result

    def test_resource_serialization(self):
        @dataclass(kw_only=True)
        class MyResource(Resource):
            name: str | None = None

        r = MyResource.from_dict({"name": "test"})
        result = dumps_json(r)
        parsed = json.loads(result)
        assert parsed["name"] == "test"
