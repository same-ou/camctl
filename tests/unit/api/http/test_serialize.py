"""Tests for the serialization module."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from camctl.api.http.serialize import (
    IdentitySerializer,
    SerializeMixin,
    SnakeToCamelSerializer,
    _snake_to_camel,
    camel_to_snake,
)


# --- _snake_to_camel ---


class TestSnakeToCamel:
    def test_standard(self):
        assert _snake_to_camel("foo_bar") == "fooBar"

    def test_single_word(self):
        assert _snake_to_camel("foo") == "foo"

    def test_three_parts(self):
        assert _snake_to_camel("foo_bar_baz") == "fooBarBaz"

    def test_trailing_underscore(self):
        assert _snake_to_camel("foo_bar_") == "fooBar"

    def test_consecutive_underscores(self):
        assert _snake_to_camel("foo__bar") == "fooBar"

    def test_empty_string(self):
        assert _snake_to_camel("") == ""

    def test_leading_underscore(self):
        result = _snake_to_camel("_foo")
        assert result == "Foo"


# --- camel_to_snake ---


class TestCamelToSnake:
    def test_standard(self):
        assert camel_to_snake("fooBar") == "foo_bar"

    def test_acronym(self):
        assert camel_to_snake("HTTPClient") == "http_client"

    def test_hyphen(self):
        assert camel_to_snake("foo-bar") == "foo_bar"

    def test_trailing_colon(self):
        assert camel_to_snake("fooBar:") == "foo_bar"

    def test_single_word(self):
        assert camel_to_snake("foo") == "foo"

    def test_already_snake(self):
        assert camel_to_snake("foo_bar") == "foo_bar"

    def test_multiple_words(self):
        assert camel_to_snake("processDefinitionKey") == "process_definition_key"


# --- IdentitySerializer ---


class TestIdentitySerializer:
    def test_returns_unchanged(self):
        s = IdentitySerializer()
        data = {"foo_bar": 1, "nested": {"baz_qux": 2}}
        assert s.serialize(data) is data

    def test_none(self):
        assert IdentitySerializer().serialize(None) is None

    def test_list(self):
        items = [1, 2, 3]
        assert IdentitySerializer().serialize(items) is items


# --- SnakeToCamelSerializer ---


class TestSnakeToCamelSerializer:
    def test_none_passthrough(self):
        assert SnakeToCamelSerializer().serialize(None) is None

    def test_flat_dict(self):
        result = SnakeToCamelSerializer().serialize({"foo_bar": 1, "baz": 2})
        assert result == {"fooBar": 1, "baz": 2}

    def test_nested_dicts(self):
        result = SnakeToCamelSerializer().serialize(
            {"outer_key": {"inner_key": "value"}}
        )
        assert result == {"outerKey": {"innerKey": "value"}}

    def test_list_of_dicts(self):
        result = SnakeToCamelSerializer().serialize(
            [{"sort_by": "name"}, {"sort_by": "date"}]
        )
        assert result == [{"sortBy": "name"}, {"sortBy": "date"}]

    def test_dataclass(self):
        @dataclass
        class Params:
            sort_by: str = "name"
            max_results: int = 10

        result = SnakeToCamelSerializer().serialize(Params())
        assert result == {"sortBy": "name", "maxResults": 10}

    def test_scalar_passthrough(self):
        assert SnakeToCamelSerializer().serialize(42) == 42
        assert SnakeToCamelSerializer().serialize("hello") == "hello"


# --- SerializeMixin ---


class TestSerializeMixin:
    def test_basic_dataclass(self):
        @dataclass
        class Payload(SerializeMixin):
            sort_by: str = "name"
            max_results: int = 10

        result = Payload().to_api_dict()
        assert result == {"sortBy": "name", "maxResults": 10}

    def test_none_fields_skipped(self):
        @dataclass
        class Payload(SerializeMixin):
            required: str = "yes"
            optional: str | None = None

        result = Payload().to_api_dict()
        assert result == {"required": "yes"}
        assert "optional" not in result

    def test_nested_serialize_mixin(self):
        @dataclass
        class Inner(SerializeMixin):
            inner_key: str = "val"

        @dataclass
        class Outer(SerializeMixin):
            outer_key: str = "top"
            nested: Inner | None = None

        result = Outer(nested=Inner()).to_api_dict()
        assert result == {"outerKey": "top", "nested": {"innerKey": "val"}}

    def test_list_field(self):
        @dataclass
        class Payload(SerializeMixin):
            items: list[str] | None = None

        result = Payload(items=["a", "b"]).to_api_dict()
        assert result == {"items": ["a", "b"]}
