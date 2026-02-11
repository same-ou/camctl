"""Tests for SubService._path building."""

from __future__ import annotations

from camctl.api.http.service import SubService


class TestSubServicePath:
    def test_no_prefix(self):
        svc = SubService.__new__(SubService)
        svc.URL_PREFIX = ""
        assert svc._path("task/123") == "task/123"

    def test_with_prefix(self):
        svc = SubService.__new__(SubService)
        svc.URL_PREFIX = "api/v1"
        assert svc._path("task/123") == "api/v1/task/123"

    def test_prefix_with_trailing_slash(self):
        svc = SubService.__new__(SubService)
        svc.URL_PREFIX = "api/v1/"
        assert svc._path("task/123") == "api/v1/task/123"

    def test_suffix_with_leading_slash(self):
        svc = SubService.__new__(SubService)
        svc.URL_PREFIX = "api/v1"
        assert svc._path("/task/123") == "api/v1/task/123"

    def test_both_slashes(self):
        svc = SubService.__new__(SubService)
        svc.URL_PREFIX = "api/v1/"
        assert svc._path("/task/123") == "api/v1/task/123"
