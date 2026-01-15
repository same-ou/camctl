"""Process-focused endpoints for the Camunda API."""

from __future__ import annotations

from camctl.api.http import Page
from camctl.api.camunda.models import Variable
from camctl.api.camunda.service import CamSubService

from .endpoints import ProcessEndpoint
from .models import (
    ProcessCancelResult,
    ProcessFilterParams,
    ProcessInstance,
    ProcessListParams,
)


class ProcessesAPI(CamSubService):
    """Wrapper around process-related Camunda endpoints."""

    URL_PREFIX = ""

    def get(self, process_id: str) -> ProcessInstance | None:
        """Fetch a single process instance by its identifier."""
        response = self._client.get(
            self._path(ProcessEndpoint.DETAIL.value.format(process_id=process_id)),
            allow_error=True,
        )
        if response.status_code == 404:
            return None
        self._client._raise_for_status(response)
        return ProcessInstance.from_dict(response.json())

    def list(self, *, params: ProcessListParams | None = None) -> Page[ProcessInstance]:
        """List process instances with optional query parameters."""
        response = self._client.get(
            self._path(ProcessEndpoint.LIST.value),
            params=params.to_params() if params else None,
        )
        payload = response.json()
        if isinstance(payload, list):
            items = [
                ProcessInstance.from_dict(item)
                for item in payload
                if isinstance(item, dict)
            ]
            return Page(raw={"items": payload}, items=items)
        if not isinstance(payload, dict):
            raise TypeError("Process list response must be a list or object.")
        return Page.from_dict(payload, item_parser=ProcessInstance.from_dict)

    def count(self, *, params: ProcessFilterParams | None = None) -> int:
        """Count process instances with optional query parameters."""
        response = self._client.get(
            self._path(ProcessEndpoint.COUNT.value),
            params=params.to_params() if params else None,
        )
        payload = response.json()
        if isinstance(payload, dict) and "count" in payload:
            return int(payload["count"])
        raise TypeError("Process count response must be an object with a count value.")

    def variables(
        self,
        process_id: str,
        *,
        deserialize_values: bool | None = None,
    ) -> dict[str, Variable] | None:
        """Fetch variables for a process instance."""
        params = {}
        if deserialize_values is not None:
            params["deserializeValues"] = deserialize_values
        response = self._client.get(
            self._path(ProcessEndpoint.VARIABLES.value.format(process_id=process_id)),
            params=params or None,
            allow_error=True,
        )
        if response.status_code == 404:
            return None
        self._client._raise_for_status(response)
        payload = response.json()
        if isinstance(payload, dict):
            variables: dict[str, Variable] = {}
            for name, value in payload.items():
                if isinstance(value, dict):
                    variables[name] = Variable.from_dict(value)
                else:
                    raise TypeError("Process variable payloads must be objects.")
            return variables
        raise TypeError("Variables response must be a JSON object.")


    def cancel(self, process_id: str) -> ProcessCancelResult | None:
        """Cancel a process instance by its identifier."""
        response = self._client.delete(
            self._path(ProcessEndpoint.CANCEL.value.format(process_id=process_id)),
            allow_error=True,
        )
        if response.status_code == 404:
            return None
        self._client._raise_for_status(response)
        if response.status_code == 204:
            return None
        return ProcessCancelResult.from_dict(response.json())
