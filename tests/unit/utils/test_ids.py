"""Tests for ID parsing utilities."""

from __future__ import annotations

import pytest

from camctl.utils.ids import load_id_file, parse_id_list


class TestParseIdList:
    def test_comma_separated(self):
        result = parse_id_list("a,b,c")
        assert result == ["a", "b", "c"]

    def test_newline_separated(self):
        result = parse_id_list("a\nb\nc")
        assert result == ["a", "b", "c"]

    def test_json_array(self):
        result = parse_id_list('["id1", "id2", "id3"]')
        assert result == ["id1", "id2", "id3"]

    def test_empty(self):
        assert parse_id_list("") == []

    def test_whitespace_only(self):
        assert parse_id_list("   ") == []

    def test_mixed_delimiters(self):
        result = parse_id_list("a,b\nc")
        assert result == ["a", "b", "c"]

    def test_strips_whitespace(self):
        result = parse_id_list("  a , b , c  ")
        assert result == ["a", "b", "c"]

    def test_json_with_null(self):
        result = parse_id_list('[null, "a", "b"]')
        assert result == ["a", "b"]


class TestLoadIdFile:
    def test_json_file(self, tmp_path):
        f = tmp_path / "ids.json"
        f.write_text('["id1", "id2"]')
        result = load_id_file(f)
        assert result == ["id1", "id2"]

    def test_delimiter_file(self, tmp_path):
        f = tmp_path / "ids.txt"
        f.write_text("id1,id2,id3")
        result = load_id_file(f)
        assert result == ["id1", "id2", "id3"]

    def test_newline_file(self, tmp_path):
        f = tmp_path / "ids.txt"
        f.write_text("id1\nid2\nid3")
        result = load_id_file(f)
        assert result == ["id1", "id2", "id3"]

    def test_empty_file(self, tmp_path):
        f = tmp_path / "ids.txt"
        f.write_text("")
        assert load_id_file(f) == []

    def test_invalid_json(self, tmp_path):
        f = tmp_path / "ids.json"
        f.write_text("[invalid json")
        with pytest.raises(ValueError, match="Invalid JSON"):
            load_id_file(f)
