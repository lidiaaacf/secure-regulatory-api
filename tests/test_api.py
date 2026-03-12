import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.rules.engine import RulesEngine
from app.schemas.report import RuleResultSchema
from app.contexts.base import ValidationContextEnum


@pytest.fixture
def client():
    with TestClient(app) as c:
        engine = RulesEngine()

        class FakeContext:
            name = ValidationContextEnum.generic.value

            def evaluate(self, payload):
                return [
                    RuleResultSchema(rule="dummy_rule", status="passed", severity="low")
                ]

        engine.register_context(FakeContext())
        c.app.state.rules_engine = engine

        yield c


@pytest.fixture(autouse=True)
def setup_api_key(monkeypatch):
    monkeypatch.setattr(settings, "ALLOWED_API_KEYS", ["test-key"])


@pytest.fixture(autouse=True)
def disable_middlewares(monkeypatch):
    from app.core.middleware import (
        RateLimitMiddleware,
        SecurityMiddleware,
        InternalAPIMiddleware,
    )

    monkeypatch.setattr(
        RateLimitMiddleware,
        "dispatch",
        lambda self, request, call_next: call_next(request),
    )

    monkeypatch.setattr(
        SecurityMiddleware,
        "dispatch",
        lambda self, request, call_next: call_next(request),
    )

    monkeypatch.setattr(
        InternalAPIMiddleware,
        "dispatch",
        lambda self, request, call_next: call_next(request),
    )


def test_validate_endpoint_success(client):
    payload = {"payload": {"amount": 5000}}
    response = client.post(
        f"/validate/{ValidationContextEnum.generic.value}",
        json=payload,
        headers={"x-api-key": "test-key"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["overall_status"] == "success"
    assert data["summary"]["passed"] == 1


def test_validate_endpoint_failure(client):
    engine = RulesEngine()

    class FailContext:
        name = ValidationContextEnum.generic.value

        def evaluate(self, payload):
            return [
                RuleResultSchema(rule="dummy_rule", status="failed", severity="high")
            ]

    engine.register_context(FailContext())
    client.app.state.rules_engine = engine

    payload = {"payload": {"amount": 20000}}
    response = client.post(
        f"/validate/{ValidationContextEnum.generic.value}",
        json=payload,
        headers={"x-api-key": "test-key"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["overall_status"] == "failure"
    assert data["summary"]["failed"] == 1


def test_invalid_json(client):
    response = client.post(
        f"/validate/{ValidationContextEnum.generic.value}",
        content="not json",
        headers={"x-api-key": "test-key"},
    )
    assert response.status_code == 400


def test_invalid_api_key(client):
    response = client.post(
        f"/validate/{ValidationContextEnum.generic.value}",
        json={"payload": {"amount": 500}},
        headers={"x-api-key": "wrong-key"},
    )
    assert response.status_code == 401
