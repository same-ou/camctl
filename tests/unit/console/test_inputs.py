"""Tests for CLI input parsing helpers."""

from __future__ import annotations

import pytest

from camctl.console.inputs import (
    merge_mappings,
    parse_comma_list,
    parse_json_mapping,
    parse_key_value_pairs,
)


class TestParseJsonMapping:
    def test_from_string(self):
        result = parse_json_mapping('{"key": "value"}', None)
        assert result == {"key": "value"}

    def test_from_file(self, tmp_path):
        f = tmp_path / "data.json"
        f.write_text('{"a": 1}')
        result = parse_json_mapping(None, f)
        assert result == {"a": 1}

    def test_file_takes_precedence(self, tmp_path):
        f = tmp_path / "data.json"
        f.write_text('{"from": "file"}')
        result = parse_json_mapping('{"from": "string"}', f)
        assert result == {"from": "file"}

    def test_empty(self):
        result = parse_json_mapping(None, None)
        assert result == {}

    def test_invalid_json(self):
        with pytest.raises(ValueError, match="Invalid JSON"):
            parse_json_mapping("not json", None)

    def test_non_object_json(self):
        with pytest.raises(ValueError, match="must be an object"):
            parse_json_mapping("[1, 2, 3]", None)


class TestParseKeyValuePairs:
    def test_standard(self):
        result = parse_key_value_pairs(["name=John", "age=30"])
        assert result == {"name": "John", "age": 30}

    def test_json_values(self):
        result = parse_key_value_pairs(['data={"nested": true}', "flag=true"])
        assert result["data"] == {"nested": True}
        assert result["flag"] is True

    def test_missing_equals(self):
        with pytest.raises(ValueError, match="expected key=value"):
            parse_key_value_pairs(["invalid"])

    def test_empty_key(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            parse_key_value_pairs(["=value"])

    def test_value_with_equals(self):
        result = parse_key_value_pairs(["expr=a=b"])
        assert result == {"expr": "a=b"}

    def test_empty_value(self):
        result = parse_key_value_pairs(["key="])
        assert result == {"key": ""}


class TestMergeMappings:
    def test_override_order(self):
        result = merge_mappings({"a": 1, "b": 2}, {"b": 3, "c": 4})
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_empty(self):
        result = merge_mappings({}, {})
        assert result == {}

    def test_single(self):
        result = merge_mappings({"a": 1})
        assert result == {"a": 1}


class TestParseCommaList:
    def test_basic(self):
        result = parse_comma_list(["a,b,c"])
        assert result == ["a", "b", "c"]

    def test_deduplication(self):
        result = parse_comma_list(["a,b,a"])
        assert result == ["a", "b"]

    def test_none_input(self):
        assert parse_comma_list(None) is None

    def test_empty_strings(self):
        assert parse_comma_list([""]) is None

    def test_multiple_values(self):
        result = parse_comma_list(["a,b", "c,d"])
        assert result == ["a", "b", "c", "d"]

    def test_whitespace_stripped(self):
        result = parse_comma_list(["  a , b "])
        assert result == ["a", "b"]

    def test_empty_sequence(self):
        assert parse_comma_list([]) is None
