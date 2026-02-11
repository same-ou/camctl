"""Tests for pagination models: SortInfo, PaginationInfo, Page."""

from __future__ import annotations

from camctl.api.camunda.common.pagination import Page, PaginationInfo, SortInfo
from camctl.api.camunda.common.resource import Resource


class TestSortInfo:
    def test_from_dict(self):
        s = SortInfo.from_dict({"field": "name", "direction": "asc"})
        assert s.field == "name"
        assert s.direction == "asc"

    def test_to_dict(self):
        s = SortInfo.from_dict({"field": "name", "direction": "asc"})
        d = s.to_dict()
        assert d["field"] == "name"
        assert d["direction"] == "asc"


class TestPaginationInfo:
    def test_from_dict_camel_case(self):
        p = PaginationInfo.from_dict({
            "page": 1,
            "size": 10,
            "total": 100,
            "totalPages": 10,
            "hasNext": True,
            "hasPrevious": False,
        })
        assert p.page == 1
        assert p.size == 10
        assert p.total == 100
        assert p.total_pages == 10
        assert p.has_next is True
        assert p.has_previous is False

    def test_from_dict_partial(self):
        p = PaginationInfo.from_dict({"page": 1})
        assert p.page == 1
        assert p.size is None


class TestPage:
    def test_from_dict_with_items_key(self):
        data = {
            "items": [{"name": "a"}, {"name": "b"}],
            "page": {"page": 1, "size": 10, "total": 2},
        }
        page = Page.from_dict(data, item_parser=Resource.from_dict)
        assert len(page.items) == 2
        assert page.pagination is not None
        assert page.pagination.total == 2

    def test_from_dict_with_data_key(self):
        data = {"data": [{"name": "a"}]}
        page = Page.from_dict(data, item_parser=Resource.from_dict)
        assert len(page.items) == 1

    def test_from_dict_with_sort(self):
        data = {
            "items": [],
            "sort": {"field": "name", "direction": "asc"},
        }
        page = Page.from_dict(data, item_parser=Resource.from_dict)
        assert page.sort is not None
        assert page.sort.field == "name"

    def test_from_dict_with_sorting_key(self):
        data = {
            "items": [],
            "sorting": {"field": "id", "direction": "desc"},
        }
        page = Page.from_dict(data, item_parser=Resource.from_dict)
        assert page.sort is not None
        assert page.sort.direction == "desc"

    def test_from_dict_with_pagination_key(self):
        data = {
            "items": [],
            "pagination": {"page": 2, "size": 5},
        }
        page = Page.from_dict(data, item_parser=Resource.from_dict)
        assert page.pagination is not None
        assert page.pagination.page == 2

    def test_from_dict_empty_items(self):
        data = {"items": []}
        page = Page.from_dict(data, item_parser=Resource.from_dict)
        assert len(page.items) == 0
        assert page.pagination is None
        assert page.sort is None

    def test_item_parser_applied(self):
        from dataclasses import dataclass

        @dataclass(kw_only=True)
        class NamedResource(Resource):
            name: str | None = None

        data = {"items": [{"name": "test"}]}
        page = Page.from_dict(data, item_parser=NamedResource.from_dict)
        assert isinstance(page.items[0], NamedResource)
        assert page.items[0].name == "test"

    def test_to_dict_items_serialized(self):
        from dataclasses import dataclass

        @dataclass(kw_only=True)
        class NamedResource(Resource):
            name: str | None = None

        data = {
            "items": [{"name": "test"}],
            "page": {"page": 1, "size": 10},
        }
        page = Page.from_dict(data, item_parser=NamedResource.from_dict)
        d = page.to_dict()
        assert isinstance(d["items"], list)
        assert d["items"][0]["name"] == "test"

    def test_from_dict_no_items_key(self):
        data = {}
        page = Page.from_dict(data, item_parser=Resource.from_dict)
        assert len(page.items) == 0
