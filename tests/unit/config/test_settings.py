"""Tests for settings loading and env interpolation."""

from __future__ import annotations

import pytest

from camctl.config.settings import Settings


class TestFromMapping:
    def test_defaults(self):
        s = Settings.from_mapping({})
        assert s.authority == "uat"
        assert s.scopes == []

    def test_direct_keys(self):
        s = Settings.from_mapping({"authority": "prod", "scopes": ["read", "write"]})
        assert s.authority == "prod"
        assert s.scopes == ["read", "write"]

    def test_nested_auth_key(self):
        s = Settings.from_mapping({
            "auth": {"authority": "staging", "scopes": "a,b,c"}
        })
        assert s.authority == "staging"
        assert s.scopes == ["a", "b", "c"]

    def test_scope_normalization_string(self):
        s = Settings.from_mapping({"scopes": "read, write , admin"})
        assert s.scopes == ["read", "write", "admin"]

    def test_scope_normalization_list(self):
        s = Settings.from_mapping({"scopes": ["read", "write"]})
        assert s.scopes == ["read", "write"]

    def test_scope_key_alias(self):
        s = Settings.from_mapping({"scope": "read,write"})
        assert s.scopes == ["read", "write"]

    def test_scope_invalid_type(self):
        with pytest.raises(TypeError, match="Scopes must be"):
            Settings.from_mapping({"scopes": 42})


class TestFromYaml:
    def test_basic_yaml(self, tmp_path):
        config = tmp_path / "config.yaml"
        config.write_text("authority: prod\nscopes:\n  - read\n  - write\n")
        s = Settings.from_yaml(config)
        assert s.authority == "prod"
        assert s.scopes == ["read", "write"]
        assert s.config_path == config

    def test_env_interpolation(self, tmp_path, monkeypatch):
        monkeypatch.setenv("MY_AUTHORITY", "staging")
        config = tmp_path / "config.yaml"
        config.write_text("authority: ${MY_AUTHORITY}\n")
        s = Settings.from_yaml(config)
        assert s.authority == "staging"

    def test_missing_env_var(self, tmp_path):
        config = tmp_path / "config.yaml"
        config.write_text("authority: ${NONEXISTENT_VAR_123}\n")
        with pytest.raises(ValueError, match="not set"):
            Settings.from_yaml(config)

    def test_non_mapping_yaml(self, tmp_path):
        config = tmp_path / "config.yaml"
        config.write_text("- item1\n- item2\n")
        with pytest.raises(ValueError, match="mapping"):
            Settings.from_yaml(config)

    def test_empty_yaml(self, tmp_path):
        config = tmp_path / "config.yaml"
        config.write_text("")
        s = Settings.from_yaml(config)
        assert s.authority == "uat"
