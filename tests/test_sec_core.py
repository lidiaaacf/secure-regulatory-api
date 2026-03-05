import pytest
from fastapi import HTTPException
from starlette.requests import Request

from app.core import security
from app.core.security import (
    validate_api_key,
    get_depth,
    count_keys,
    precheck_payload_structure,
    mask_sensitive_data,
)
from app.config import settings


@pytest.fixture(autouse=True)
def setup_api_keys(monkeypatch):
    monkeypatch.setattr(settings, "ALLOWED_API_KEYS", ["valid-key"])


def test_validate_api_key_valid(monkeypatch):
    scope = {"type": "http", "headers": [(b"x-api-key", b"valid-key")]}
    request = Request(scope)
    validate_api_key(request)


def test_validate_api_key_invalid(monkeypatch):
    scope = {"type": "http", "headers": [(b"x-api-key", b"wrong-key")]}
    request = Request(scope)

    with pytest.raises(HTTPException) as exc:
        validate_api_key(request)

    assert exc.value.status_code == 401


def test_validate_api_key_missing(monkeypatch):
    scope = {"type": "http", "headers": []}
    request = Request(scope)

    with pytest.raises(HTTPException):
        validate_api_key(request)


def test_get_depth_simple():
    assert get_depth({"a": 1}) == 1


def test_get_depth_nested():
    assert get_depth({"a": {"b": {"c": 1}}}) == 3


def test_get_depth_with_list():
    assert get_depth({"a": [{"b": 1}]}) == 3


def test_get_depth_empty_dict():
    assert get_depth({}) == 0


def test_get_depth_empty_list():
    assert get_depth([]) == 0


def test_count_keys_simple():
    assert count_keys({"a": 1, "b": 2}) == 2


def test_count_keys_nested():
    assert count_keys({"a": {"b": 1}}) == 2


def test_count_keys_list_nested():
    assert count_keys({"a": [{"b": 1}, {"c": 2}]}) == 3


def test_count_keys_empty():
    assert count_keys({}) == 0
    assert count_keys([]) == 0


def test_structural_checks_valid():
    assert precheck_payload_structure({"a": 1}) is None


def test_structural_checks_too_deep(monkeypatch):
    monkeypatch.setattr(security, "MAX_DEPTH", 1)
    payload = {"a": {"b": 1}}
    result = precheck_payload_structure(payload)
    assert result == "Payload nesting too deep"


def test_structural_checks_too_many_keys(monkeypatch):
    monkeypatch.setattr(security, "MAX_KEYS", 1)
    payload = {"a": 1, "b": 2}
    result = precheck_payload_structure(payload)
    assert result == "Payload too large"


def test_structural_checks_exact_limit(monkeypatch):
    monkeypatch.setattr(security, "MAX_DEPTH", 3)
    monkeypatch.setattr(security, "MAX_KEYS", 2)
    payload = {"a": {"b": 1}}
    assert precheck_payload_structure(payload) is None


def test_mask_sensitive_field():
    payload = {"password": "secret"}
    masked = mask_sensitive_data(payload, ["password"])
    assert masked["password"] == "***MASKED***"


def test_mask_sensitive_case_insensitive():
    payload = {"Password": "secret"}
    masked = mask_sensitive_data(payload, ["password"])
    assert masked["Password"] == "***MASKED***"


def test_mask_sensitive_nested():
    payload = {"user": {"password": "secret"}}
    masked = mask_sensitive_data(payload, ["password"])
    assert masked["user"]["password"] == "***MASKED***"


def test_mask_sensitive_in_list():
    payload = [{"password": "secret"}]
    masked = mask_sensitive_data(payload, ["password"])
    assert masked[0]["password"] == "***MASKED***"


def test_mask_sensitive_non_sensitive_untouched():
    payload = {"username": "john"}
    masked = mask_sensitive_data(payload, ["password"])
    assert masked["username"] == "john"


def test_mask_does_not_mutate_original():
    payload = {"password": "secret"}
    masked = mask_sensitive_data(payload, ["password"])
    assert payload["password"] == "secret"
    assert masked["password"] == "***MASKED***"
