"""Tests for Variable, VariablePayload, and VariableModificationRequest."""

from __future__ import annotations

from camctl.api.camunda.common.variables import (
    Variable,
    VariableModificationRequest,
    VariablePayload,
    VariableValueInfo,
)


class TestVariable:
    def test_from_dict_basic(self):
        v = Variable.from_dict({"value": 42, "type": "Integer"})
        assert v.value == 42
        assert v.type == "Integer"

    def test_from_dict_with_value_info(self):
        v = Variable.from_dict({
            "value": "data",
            "type": "Object",
            "valueInfo": {
                "objectTypeName": "com.example.Foo",
                "serializationDataFormat": "application/json",
            },
        })
        assert isinstance(v.value_info, VariableValueInfo)
        assert v.value_info.object_type_name == "com.example.Foo"
        assert v.value_info.serialization_data_format == "application/json"

    def test_from_dict_empty(self):
        v = Variable.from_dict({})
        assert v.value is None
        assert v.type is None
        assert v.value_info is None


class TestVariableValueInfo:
    def test_from_dict(self):
        info = VariableValueInfo.from_dict({
            "objectTypeName": "com.example.Foo",
            "filename": "test.txt",
            "mimetype": "text/plain",
            "encoding": "utf-8",
            "transient": True,
        })
        assert info.object_type_name == "com.example.Foo"
        assert info.filename == "test.txt"
        assert info.mimetype == "text/plain"
        assert info.encoding == "utf-8"
        assert info.transient is True


class TestVariablePayload:
    def test_to_api_dict_basic(self):
        p = VariablePayload(value=42, type="Integer")
        d = p.to_api_dict()
        assert d == {"value": 42, "type": "Integer"}

    def test_to_api_dict_none_fields_omitted(self):
        p = VariablePayload(value="hello")
        d = p.to_api_dict()
        assert "type" not in d
        assert "valueInfo" not in d

    def test_serialize_field_mapping_value_info(self):
        p = VariablePayload(
            value="data",
            type="Object",
            value_info={"object_type_name": "Foo", "serialization_data_format": "json"},
        )
        d = p.to_api_dict()
        assert d["valueInfo"] == {
            "objectTypeName": "Foo",
            "serializationDataFormat": "json",
        }

    def test_serialize_field_resource_value_info(self):
        info = VariableValueInfo(object_type_name="Bar")
        p = VariablePayload(value="data", value_info=info)
        d = p.to_api_dict()
        assert "objectTypeName" in d["valueInfo"]


class TestVariableModificationRequest:
    def test_to_api_dict_with_modifications(self):
        mod = VariableModificationRequest(
            modifications={"var1": VariablePayload(value=1)},
            deletions=["var2"],
        )
        d = mod.to_api_dict()
        assert "modifications" in d
        assert isinstance(d["modifications"]["var1"], dict)
        assert d["modifications"]["var1"]["value"] == 1
        assert d["deletions"] == ["var2"]

    def test_to_api_dict_none_omitted(self):
        mod = VariableModificationRequest()
        d = mod.to_api_dict()
        assert "modifications" not in d
        assert "deletions" not in d
