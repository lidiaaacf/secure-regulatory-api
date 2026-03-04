import pytest
from pydantic import ValidationError
from app.schemas.transaction import TransactionDecision


def test_transaction_decision_valid():
    data = {
        "request_id": "123abc",
        "decision": "APPROVED",
        "risk_score": 85,
        "triggered_rules": ["rule1", "rule2"],
    }

    td = TransactionDecision(**data)

    assert td.request_id == data["request_id"]
    assert td.decision == data["decision"]
    assert td.risk_score == data["risk_score"]
    assert td.triggered_rules == data["triggered_rules"]


def test_transaction_decision_invalid_decision():
    data = {
        "request_id": "123abc",
        "decision": "INVALID",
        "risk_score": 50,
        "triggered_rules": [],
    }

    with pytest.raises(ValidationError) as exc:
        TransactionDecision(**data)

    assert "decision" in str(exc.value)


def test_transaction_decision_missing_field():
    data = {"request_id": "123abc", "decision": "REVIEW", "triggered_rules": []}

    with pytest.raises(ValidationError) as exc:
        TransactionDecision(**data)

    assert "risk_score" in str(exc.value)


def test_transaction_decision_wrong_type():
    data = {
        "request_id": "123abc",
        "decision": "REJECTED",
        "risk_score": "high",
        "triggered_rules": "rule1",
    }

    with pytest.raises(ValidationError) as exc:
        TransactionDecision(**data)

    assert "risk_score" in str(exc.value)
    assert "triggered_rules" in str(exc.value)
